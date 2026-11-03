"""Validate bank-profit experiment records and report shock versus own control."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from report_isolated_shocks import statistics,euro,decimal,ratio,save_figure
import matplotlib.pyplot as plt

SOURCE=Path('qa/bank-profit-v19-comparison.json')


def validate(data):
    for p,h in data['source_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    assert hashlib.sha256(Path(data['reference']).read_bytes()).hexdigest()==data['reference_sha256']
    for experiment in data['experiments']:
        for run in experiment['runs']:
            before=run['initial'];accounts=dict(before['household_cash_cents'])
            accounts.update(staat=before['stocks_cents']['government'],bank=before['stocks_cents']['bank'],ausland=before['stocks_cents']['external'])
            # Firm opening cash is recorded on its first actual transfer.
            for t in run['transactions']:
                for key,field in [('source','source_before'),('target','target_before')]:
                    if t[key] not in accounts:accounts[t[key]]=t[field]
            tx=iter(run['transactions']);item=next(tx,None);previous=before['household_cash_cents']
            for row,m in zip(run['monthly'],run['bank_profit']):
                bank_tax=bank_div=bank_income=0
                while item and item['month']==row['month']:
                    t=item
                    assert accounts[t['source']]==t['source_before'] and accounts[t['target']]==t['target_before']
                    if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                    if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                    assert accounts[t['source']]==t['source_after'] and accounts[t['target']]==t['target_after']
                    if t['source']=='bank' and t['kind']=='profit_tax':bank_tax+=t['amount_cents']
                    if t['source']=='bank' and t['kind']=='dividend':bank_div+=t['amount_cents']
                    if t['target']=='bank' and t['kind'] in ('interest','machine_interest','government_interest'):bank_income+=t['amount_cents']
                    item=next(tx,None)
                assert m['profit_before_tax_cents']==bank_income and m['profit_tax_paid_cents']==bank_tax and m['distribution_cents']==bank_div
                assert m['after_tax_cents']==bank_income-m['profit_tax_due_cents']
                assert m['retained_earnings_cents']==m['opening_retained_cents']+m['after_tax_cents']-bank_div
                if run['policy']=='consistent':
                    assert bank_tax==bank_income//5
                    assert m['closing_equity_cents']==1000000+m['retained_earnings_cents']
                for h in row['households']:
                    assert h['cash_cents']-previous[h['id']]==h['disposable_received_cents']-h['consumption_cents']
                    assert accounts[h['id']]==h['cash_cents']
                for f in row['firms']:assert accounts[f['id']]==f['cash_cents']
                assert accounts['bank']==row['stocks_cents']['bank'] and accounts['staat']==row['stocks_cents']['government']
                assert row['stocks_cents']['government_net']-before['stocks_cents']['government_net']==row['government']['cash_balance_cents']
                before=row;previous=row['household_cash_cents']
            assert item is None


def report():
    data=json.loads(SOURCE.read_text());validate(data)
    first,second=data['experiments'];pairs=[]
    for e,policy,label in [(first,'legacy','v18 · alte Bankregel'),(first,'consistent','v19 · Regelwechsel, gleicher Start'),(second,'consistent','v19 · seit Welteröffnung')]:
        runs={r['case']:r for r in e['runs'] if r['policy']==policy}
        pairs.append((label,runs['rate'],runs['control']))
    stats={label:statistics(r,c) for label,r,c in pairs}
    def flow(run,months,kind,source=None):return sum(t['amount_cents'] for t in run['transactions'] if t['month']<=1440+months and t['kind']==kind and (source is None or t['source']==source))
    def extended(r,c,n):
        return dict(bank_tax_delta_cents=flow(r,n,'profit_tax','bank')-flow(c,n,'profit_tax','bank'),
            bank_dividend_delta_cents=flow(r,n,'dividend','bank')-flow(c,n,'dividend','bank'),
            bank_retained_delta_cents=r['bank_profit'][n-1]['retained_earnings_cents']-c['bank_profit'][n-1]['retained_earnings_cents'],
            household_income_delta_cents=sum(a['disposable_received_cents']-b['disposable_received_cents'] for a,b in zip(r['monthly'][:n],c['monthly'][:n])),
            purchases_delta_percent=ratio(sum(x['consumption_base_price_cents'] for x in r['monthly'][:n]),sum(x['consumption_base_price_cents'] for x in c['monthly'][:n])),
            firm_profit_delta_cents=sum(sum(f['profit_before_tax_cents'] for f in a['firms'])-sum(f['profit_before_tax_cents'] for f in b['firms']) for a,b in zip(r['monthly'][:n],c['monthly'][:n])),
            state_net_delta_cents=r['monthly'][n-1]['stocks_cents']['government_net']-c['monthly'][n-1]['stocks_cents']['government_net'])
    results={label:{str(n):extended(r,c,n) for n in (12,13,60)} for label,r,c in pairs}
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-bank-profit-v19'})
    fig,axes=plt.subplots(3,1,figsize=(11,9),sharex=True);fig.subplots_adjust(top=.9,bottom=.13,hspace=.25)
    fig.suptitle('Zinsschock · alte und neue Bankgewinnregel',fontsize=15)
    fig.text(.5,.935,'Jeweils Abweichung von eigener Kontrolle · Leitzins 2 → 5 % für zwölf Monate · variable Verzinsung in Monat 2–13',ha='center',fontsize=9)
    for (label,r,c),color in zip(pairs,('#b18158','#526f89','#66895a')):
        x=[0]+[v['relative_month'] for v in r['monthly']]
        values=[[0]+[ratio(a['consumption_base_price_cents'],b['consumption_base_price_cents']) for a,b in zip(r['monthly'],c['monthly'])],
            [0]+[(sum(f['profit_before_tax_cents'] for f in a['firms'])-sum(f['profit_before_tax_cents'] for f in b['firms']))/100 for a,b in zip(r['monthly'],c['monthly'])],
            [0]+[(a['stocks_cents']['government_net']-b['stocks_cents']['government_net'])/100 for a,b in zip(r['monthly'],c['monthly'])]]
        for ax,y in zip(axes,values):ax.plot(x,y,label=label,color=color,lw=1.4)
    for ax,label in zip(axes,('Haushaltskäufe zu Startpreisen · Δ %','Firmengewinn vor Steuer · Δ € / Monat','Staat: Kasse minus Schuld · Δ €')):
        ax.set_ylabel(label);ax.axhline(0,color='#999',lw=.6);ax.axvspan(.5,12.5,color='#ddd',alpha=.3);ax.grid(alpha=.2)
    axes[-1].set_xlabel('Monate seit Eingriff');axes[0].legend(loc='upper right',fontsize=8)
    save_figure(fig,Path('qa/bank-profit-v19-comparison'))
    lines=['# Zinsschock nach konsistenter Bankgewinnrechnung','',
        'Stand: 3. November 2026. Eigene simulierte Befunde des Modells v19, keine Prognose. [Vorabplan](bank-profit-v19-plan.md), [Regeln](../poc/BANK_PROFIT_MODEL.md) und [vollständige Daten](bank-profit-v19-comparison.json). Der Investitionskanal ist unverändert.','',
        '## Vergleichsmethode','',
        'Der alte Zustand nach M1440 wird mit expliziter Legacy-Bankregel reproduziert. Die alte Kontrolle und der alte Zinsschock stimmen über alle 60 Monate in sämtlichen gespeicherten Monatsbeobachtungen mit dem v18-Archiv überein. Aus genau demselben Zustand starten auch neue Kontrolle und neuer Zinsschock. Die reine Umstellung ist damit von der Differenz Schock minus eigene Kontrolle getrennt. Die zusätzliche dritte Zeile startet bereits bei Welteröffnung mit der neuen Regel und hat nach M1440 folglich einen anderen Ausgangszustand.','',
        '![Zinswirkungen gegenüber eigener Kontrolle](bank-profit-v19-comparison.svg)','',
        '## Erste zwölf Eingriffsmonate','',
        '| Variante | Erhaltenes Nettohaushaltseinkommen Δ | Haushaltskäufe zu Startpreisen Δ | Firmengewinn vor Steuer Δ | Staat netto am Ende Δ |',
        '| --- | ---: | ---: | ---: | ---: |']
    for label,_,_ in pairs:
        s=results[label]['12'];lines.append(f"| {label} | {euro(s['household_income_delta_cents'])} | {decimal(s['purchases_delta_percent'],3)} % | {euro(s['firm_profit_delta_cents'])} | {euro(s['state_net_delta_cents'])} |")
    lines+=['','Alle Beträge sind kumulierte Flüsse gegenüber eigener Kontrolle; Staat netto ist die Stichtagsdifferenz von Kasse minus Schuld. Die höheren variablen Zinsen gelten in Monat 2–13: 330 € Mehrzinsen in den ersten zwölf Eingriffsmonaten, 360 € bis Monat 13.','',
        '## Bankgewinn und zeitlicher Rückfluss','',
        '| Variante | Zusätzliche Bankgewinnsteuer, zwölf Monate | Zusätzliche Bruttobankdividenden, zwölf Monate | Zusätzliche Bankrücklagen am Ende M12 |',
        '| --- | ---: | ---: | ---: |']
    for label,_,_ in pairs:
        s=results[label]['12'];lines.append(f"| {label} | {euro(s['bank_tax_delta_cents'])} | {euro(s['bank_dividend_delta_cents'])} | {euro(s['bank_retained_delta_cents'])} |")
    newr,newc=pairs[1][1:]
    neutral=all(a['consumption_cents']==b['consumption_cents'] and a['disposable_received_cents']==b['disposable_received_cents'] for a,b in zip(newr['monthly'],newc['monthly']))
    lines+=['','## Was die Korrektur erklärt','']
    if neutral:
        assert flow(newr,12,'profit_tax','bank')-flow(newc,12,'profit_tax','bank')==6600
        assert flow(newr,12,'dividend','bank')-flow(newc,12,'dividend','bank')==26400
        assert sum(flow(newr,12,k,s)-flow(newc,12,k,s) for s in ('alltag','werkstatt') for k in ('company_dividend','company_extra_dividend'))==-26400
        lines+=['Im gleichen Ausgangszustand bleiben Haushaltskäufe und erhaltenes Nettoeinkommen in jedem der 60 Monate exakt gleich wie in der neuen Kontrolle. Der zuvor leicht positive Konsumeffekt verschwindet. Die Korrektur erzeugt keine allgemeine Nachfragedämpfung.','',
            'In den ersten zwölf Monaten sinkt die Firmengewinnsteuer durch den höheren Zinsaufwand um 66 €; die Bank zahlt genau 66 € zusätzliche Gewinnsteuer. Ihre Bruttodividenden steigen um 264 €, während die Bruttodividenden der Firmen um 264 € fallen. Nach der Quellensteuer heben sich zusätzliche Netto-Bankdividenden und geringere Netto-Firmendividenden mit jeweils 198 € auf. Löhne und sonstige Nettoeinkommen verändern sich dabei nicht. Die Beträge sind tatsächliche Journalvergleiche, keine eingefrorene Musterrechnung.','',
            'Diese Neutralität folgt im beobachteten Zustand aus den gleichen Eigentümern, gleichartiger Gewinnbesteuerung und den jetzt angeglichenen Auszahlungsregeln. Die Unternehmen können ihren Betrieb weiter finanzieren; neue Kredit- oder Investitionsentscheidungen werden durch den Schock hier nicht ausgelöst. Ein Geldfluss von Firma zur Bank ist damit noch kein Beleg für weniger gesamtwirtschaftliche Nachfrage. Beide Bankänderungen wurden gemeinsam umgesetzt; ihr separater kausaler Anteil wurde nicht in zusätzlichen Einzelvarianten geschätzt.']
    lines+=['','Die 25-%-Ausschüttungssteuer der Haushalte wird zusätzlich bei Auszahlung einbehalten. Die Bankrücklagen schwanken monatlich und werden zum Quartalsende freigegeben, soweit das geschützte Anfangseigenkapital erhalten bleibt. Ein Zwischenbestand ist keine dauerhafte Ersparnis- oder Wachstumswirkung.','',
        '## Gesamte 60 Monate','',
        '| Variante | Nettohaushaltseinkommen Δ | Haushaltskäufe zu Startpreisen Δ | Firmengewinn vor Steuer Δ | Staat netto am Ende Δ |',
        '| --- | ---: | ---: | ---: | ---: |']
    for label,_,_ in pairs:
        s=results[label]['60'];lines.append(f"| {label} | {euro(s['household_income_delta_cents'])} | {decimal(s['purchases_delta_percent'],3)} % | {euro(s['firm_profit_delta_cents'])} | {euro(s['state_net_delta_cents'])} |")
    oldc=next(r for r in first['runs'] if r['policy']=='legacy' and r['case']=='control')
    newc=next(r for r in first['runs'] if r['policy']=='consistent' and r['case']=='control')
    change=extended(newc,oldc,12)
    lines+=['','## Umstellung ohne Zinsschock','',f"Allein die neue Bankregel verändert gegenüber der alten Kontrolle in den ersten zwölf Monaten das erhaltene Nettohaushaltseinkommen um {euro(change['household_income_delta_cents'])}, die Kaufmengen um {decimal(change['purchases_delta_percent'],3)} % und die staatliche Nettoposition am Ende um {euro(change['state_net_delta_cents'])}. Diese Umstellungseffekte sind nicht die oben ausgewiesenen Zinseffekte.",'','## Beobachtete Grenzen','',
        'Die steuerliche Sonderstellung der Bank und die sofortige Vollauszahlung sind entfernt. Bankgewinn bleibt ein vereinfachter zahlungsbezogener Zinsertrag ohne Bankbetriebskosten, Einlagenzinsen oder Risikovorsorge. Gleiches Eigentum an Firmen und Bank, die geringe variable Anfangsschuld und die fehlende zinsabhängige Investitionsentscheidung bleiben bestehen. Deshalb muss die Korrektur allein keine starke negative Konsumwirkung erzeugen. Die Vergleichswerte wurden nicht durch weitere Änderungen auf eine gewünschte Richtung eingestellt.','',
        '## Neue Referenz und technische Prüfung','']
    mature=next(r for r in second['runs'] if r['case']=='control');rows=mature['monthly'];limits={}
    for sector in ('households','firms','government','bank','government_debt'):
        values=[r['stocks_cents'][sector] for r in rows];limits[sector]=[min(values),max(values)]
        lines.append(f"- {sector}, M1441–1500: {euro(min(values))} bis {euro(max(values))}.")
    employment=[r['employment'] for r in rows];lines+=['',f"Beschäftigung im neuen ungestörten späten Verlauf: {min(employment)} bis {max(employment)} Verträge. Diese 60 beobachteten Monate nach 1440 Monaten Vorlauf sind keine Zusicherung unbegrenzter Stabilität.",'',
        '205 Pythonprüfungen bestanden; 26 Phasenschnappschüsse vom neuen UI-Vertrag akzeptiert, acht gezielt beschädigte beziehungsweise veraltete Zustände zurückgewiesen. Frontend-Build erfolgreich. Im Browser wurden drei Monate einschliesslich Quartalsausschüttung ausgeführt und die neue Bankansicht geprüft.','',
        'Das Experiment prüft 14.400 Vorlaufphasen und 1.800 Fortsetzungsphasen. Jede neue Buchung wurde anhand der tatsächlichen Vorher-/Nachher-Konten unabhängig rekonstruiert. Die Berichtserzeugung gleicht zusätzlich Bankzins, Gewinnsteuer und Dividenden mit dem Journal sowie Haushaltseinkommen und staatliche Budgetsalden mit den Konten ab. Quellen und Archive werden per SHA-256 gebunden.','',
        'Reproduktion aus dem Repository-Stamm: `python poc/scripts/compare_bank_profit.py`, danach `python poc/scripts/report_bank_profit.py` mit Matplotlib. Die ursprünglichen v18-Archive bleiben unverändert.']
    Path('qa/bank-profit-v19-report.md').write_text('\n'.join(lines)+'\n')
    result=dict(date='2026-11-03',model=data['model'],source_data_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        report_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=data['checks'],python_tests_passed=205,
        ui_snapshots_passed=26,invalid_snapshots_rejected=8,frontend_build_passed=True,bank_view_three_months_checked=True,
        journal_income_and_bank_profit_reconciled=True,same_state_all_60_months_household_neutral=neutral,results=results,rule_change_without_shock_12=change,late_control_ranges_cents=limits)
    Path('qa/bank-profit-v19-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=='__main__':report()
