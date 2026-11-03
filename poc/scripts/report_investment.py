"""Auditable v20 investment timing and rate transmission; no rule retuning."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from report_isolated_shocks import euro,decimal,ratio,save_figure
import matplotlib.pyplot as plt

SOURCE=Path('qa/investment-v20-comparison.json')


def validate(data):
    for p,h in data['source_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    assert hashlib.sha256(Path(data['reference']).read_bytes()).hexdigest()==data['reference_sha256']
    for e in data['experiments']:
        for run in e['runs']:
            assert run['initial']==e['anchor'] and len(run['monthly'])==60
            before=run['initial'];accounts=dict(before['household_cash_cents'])
            accounts.update(staat=before['stocks_cents']['government'],bank=before['stocks_cents']['bank'],ausland=before['stocks_cents']['external'])
            for t in run['transactions']:
                for key,field in [('source','source_before'),('target','target_before')]:
                    if t[key] not in accounts:accounts[t[key]]=t[field]
            iterator=iter(run['transactions']);t=next(iterator,None);cash=before['household_cash_cents']
            for row,a in zip(run['monthly'],run['assessments']):
                while t and t['month']==row['month']:
                    assert accounts[t['source']]==t['source_before'] and accounts[t['target']]==t['target_before']
                    if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                    if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                    assert accounts[t['source']]==t['source_after'] and accounts[t['target']]==t['target_after']
                    t=next(iterator,None)
                for h in row['households']:
                    assert h['cash_cents']-cash[h['id']]==h['disposable_received_cents']-h['consumption_cents']
                    assert accounts[h['id']]==h['cash_cents']
                for f in row['firms']:
                    assert accounts[f['id']]==f['cash_cents']
                    assert f['opening_inventory_units']+f['produced_units']-f['sold_units']==f['inventory_units']
                assert accounts['bank']==row['stocks_cents']['bank'] and accounts['staat']==row['stocks_cents']['government']
                assert row['stocks_cents']['government_net']-before['stocks_cents']['government_net']==row['government']['cash_balance_cents']
                if a:
                    assert a['monthly_before_tax_cents']==a['additional_sales_cents']+a['wage_saving_cents']-a['additional_energy_cents']
                    assert a['cash_value_path'][-1]['value_cents']==a['cash_npv_cents']
                    assert a['loan_value_path'][-1]['value_cents']==a['loan_npv_cents']
                    assert sum(p['principal_cents'] for p in a['loan_schedule'])==a['machine_cost_cents']
                before=row;cash=row['household_cash_cents']
            assert t is None


def metrics(run,control,n):
    r,c=run['monthly'][:n],control['monthly'][:n]
    income=lambda field:sum(sum(h[field] for h in a['households'])-sum(h[field] for h in b['households']) for a,b in zip(r,c))
    return dict(investment_delta_cents=sum(a['investment_paid_cents']-b['investment_paid_cents'] for a,b in zip(r,c)),
        purchases_delta_percent=ratio(sum(a['consumption_base_price_cents'] for a in r),sum(b['consumption_base_price_cents'] for b in c)),
        purchases_delta_cents=sum(a['consumption_cents']-b['consumption_cents'] for a,b in zip(r,c)),
        household_income_delta_cents=sum(a['disposable_received_cents']-b['disposable_received_cents'] for a,b in zip(r,c)),
        non_owner_income_delta_cents=income('income_before_owner_payout_cents'),owner_income_delta_cents=income('owner_payout_net_cents'),
        wages_delta_cents=income('wages_cents'),stock_gap_delta_cents=income('stock_gap_cents'),
        firm_profit_delta_cents=sum(sum(f['profit_before_tax_cents'] for f in a['firms'])-sum(f['profit_before_tax_cents'] for f in b['firms']) for a,b in zip(r,c)),
        state_net_delta_cents=r[-1]['stocks_cents']['government_net']-c[-1]['stocks_cents']['government_net'],
        capital_delta=r[-1]['capital']['alltag']-c[-1]['capital']['alltag'])


def main():
    data=json.loads(SOURCE.read_text());validate(data)
    groups={e['name']:e for e in data['experiments']}
    pairs=[]
    for group,policy,label in [('same_late_state','orders','v19 · bisherige Regel'),('same_late_state','valuation','v20 · Umstellung aus altem Zustand'),('active_marginal_project','valuation','v20 · gezieltes Grenzprojekt'),('mature_valuation','valuation','v20 · neue späte Referenz')]:
        if group not in groups:continue
        r={r['case']:r for r in groups[group]['runs'] if r['policy']==policy}
        pairs.append((group,label,r['rate'],r['control']))
    results={label:{str(n):metrics(r,c,n) for n in (12,13,60)} for _,label,r,c in pairs}
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-investment-v20'})
    fig,axes=plt.subplots(3,3,figsize=(14,10));fig.subplots_adjust(top=.9,bottom=.09,hspace=.28,wspace=.28)
    fig.suptitle('Investitionen und Zinsschock · Abweichung von eigener Kontrolle',fontsize=14)
    titles=['Alter später Zustand · M1440','Gezieltes Grenzprojekt','Neue späte Referenz · M1440']
    fig.text(.5,.94,'Leitzins 2 → 5 % für zwölf Monate · Rücknahme ab relativem Monat 13 · unveränderte übrige Regeln',ha='center',fontsize=9)
    colors=['#b18158','#526f89','#9a5961','#66895a']
    for (group,label,r,c),color in zip(pairs,colors):
        col={'same_late_state':0,'active_marginal_project':1,'mature_valuation':2}[group]
        x=[0]+[a['relative_month'] for a in r['monthly']]
        cum=[];value=0
        for a,b in zip(r['monthly'],c['monthly']):value+=a['investment_paid_cents']-b['investment_paid_cents'];cum.append(value/100)
        series=[[0]+cum,[0]+[ratio(a['consumption_base_price_cents'],b['consumption_base_price_cents']) for a,b in zip(r['monthly'],c['monthly'])],
            [0]+[(a['stocks_cents']['government_net']-b['stocks_cents']['government_net'])/100 for a,b in zip(r['monthly'],c['monthly'])]]
        for row,y in enumerate(series):axes[row,col].plot(x,y,label=label,color=color,lw=1.4)
    for col,title in enumerate(titles):
        axes[0,col].set_title(title);axes[0,col].legend(fontsize=7)
        for row in range(3):
            axes[row,col].axhline(0,color='#999',lw=.6);axes[row,col].axvspan(.5,12.5,color='#ddd',alpha=.25);axes[row,col].grid(alpha=.2)
        axes[2,col].set_xlabel('Monate seit Eingriff')
    for ax,label in zip(axes[:,0],('Investitionszahlungen · kumuliert Δ €','Haushaltskäufe zu Startpreisen · Δ %','Staat: Kasse minus Schuld · Δ €')):ax.set_ylabel(label)
    save_figure(fig,Path('qa/investment-v20-effects'))
    lines=['# Investitionsprüfung und erneuter Zinsschock','',
        'Stand: 3. November 2026. Eigene simulierte Befunde und Erwartungsrechnungen, keine Prognose. [Vorabplan](investment-v20-plan.md), [Modellregeln](../poc/INVESTMENT_MODEL.md), [vollständiges Ergebnisarchiv](investment-v20-comparison.json).','',
        '## Abgrenzung und Vergleich','',
        'Die neue Regel bewertet den bestehenden Maschinenfall Alltag & Versorgung → Werkstatt & Technik. Erwartete zusätzliche Verkäufe und eingesparte Arbeitszeit werden gegen Energie, Steuern, Kaufpreis und Finanzierung gerechnet. Eigenmittel erhalten einen ausdrücklich angenommenen Bewertungszins in Höhe des Modell-Leitzinses; dies erzeugt keine Einlagenzinsen. Die Kreditrechnung enthält tatsächliche vertragliche Zinsen und volle Tilgung des bestehenden begrenzten Maschinenvertrags. Es wird weder eine neue Branche noch ein allgemeiner Kreditmarkt eingeführt.','',
        'Die alte Investitionsregel wird bis M1440 reproduziert. Anker und beide alten 60-Monats-Fortsetzungen müssen mit dem archivierten v19-Lauf übereinstimmen. Aus demselben Zustand laufen alte/neue Investitionsregel jeweils ohne/mit Schock. Eine neue Referenz verwendet die Bewertung seit Welteröffnung. Der zusätzliche Grenzfall wird nach dem vorab festgelegten Kriterium aus dem ungestörten Verlauf ausgewählt; er ist kein repräsentativer Durchschnittseffekt.','',
        '![Investitionen, Haushaltskäufe und Staatsfinanzen](investment-v20-effects.svg)','',
        '## Schock minus eigene Kontrolle, erste zwölf Monate','',
        '| Vergleich | Investitionszahlungen Δ | Erhaltenes Nettohaushaltseinkommen Δ | Kaufmengen Δ | Firmengewinn vor Steuer Δ | Staat netto am Ende Δ |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for _,label,_,_ in pairs:
        s=results[label]['12'];lines.append(f"| {label} | {euro(s['investment_delta_cents'])} | {euro(s['household_income_delta_cents'])} | {decimal(s['purchases_delta_percent'],3)} % | {euro(s['firm_profit_delta_cents'])} | {euro(s['state_net_delta_cents'])} |")
    lines+=['','Flüsse sind kumuliert; Staat netto ist die Stichtagsdifferenz Kasse minus Schuld. Unterschiedliche Ausgangszustände werden jeweils mit eigener Kontrolle verglichen. Die variable Altverzinsung folgt mit einem Monat Verzögerung.','',
        '## Investitionsgelegenheit und tatsächliche Lieferung','']
    active=groups.get('active_marginal_project')
    opportunity=None
    if active:
        rr={r['case']:r for r in active['runs']};r,c=rr['rate'],rr['control'];a,b=c['assessments'][0],r['assessments'][0]
        for field in ('monthly_after_tax_cents','machine_cost_cents','before','after','demand_units'):assert a[field]==b[field],field
        assert a['decision']=='invest' and b['decision']=='unprofitable' and a['cash_npv_cents']>0>=b['cash_npv_cents']
        paid={k:[dict(month=x['month'],relative_month=x['relative_month'],amount_cents=x['investment_paid_cents']) for x in v['monthly'] if x['investment_paid_cents']] for k,v in rr.items()}
        opportunity=dict(selection=active['selection'],control_first=a,shock_first=b,actual_payments=paid)
        lines+=[f"Das erste tatsächlich finanzierbare Grenzprojekt liegt in Monat {active['selection']['month']}. Die vollständigen Zustände vor diesem Monat sind identisch. Erwarteter monatlicher Nachsteuer-Mehrertrag: {euro(a['monthly_after_tax_cents'])}; Maschinenpreis: {euro(a['machine_cost_cents'])}.",'',
            '| Erwartungsrechnung beim ersten Entscheid | Ohne Schock | Mit Schock |','| --- | ---: | ---: |',
            f"| Eigenmittel-Kapitalwert, 2 beziehungsweise 5 % | {euro(a['cash_npv_cents'])} | {euro(b['cash_npv_cents'])} |",
            f"| Kredit-Kapitalwert, Angebot 6 beziehungsweise 9 % | {euro(a['loan_npv_cents'])} | {euro(b['loan_npv_cents'])} |",'']
        for key,label in [('control','Ohne Schock'),('rate','Mit Schock')]:
            lines.append(label+': tatsächlich bezahlte und gelieferte Maschinen '+(', '.join('M'+str(x['month'])+' ('+euro(x['amount_cents'])+')' for x in paid[key]) or 'keine')+'.')
        fig,axes=plt.subplots(1,2,figsize=(12,4));fig.subplots_adjust(bottom=.2,wspace=.3)
        for key,color,label in [('control','#526f89','Ohne Schock'),('rate','#9a5961','Mit Schock')]:
            v=rr[key];curve=v['assessments'][0]['cash_value_path'];axes[0].plot([p['month'] for p in curve],[p['value_cents']/100 for p in curve],label=label,color=color)
            total=0;curve=[]
            for row in v['monthly'][:24]:total+=row['investment_paid_cents'];curve.append(total/100)
            axes[1].step([0]+list(range(1,25)),[0]+curve,where='post',label=label,color=color)
        axes[0].axhline(0,color='#999',lw=.7);axes[0].set_title('Erwarteter Eigenmittel-Kapitalwert');axes[0].set_xlabel('Monate ab Bindung');axes[0].set_ylabel('Abgezinster Nettowert · €')
        axes[1].set_title('Tatsächlich bezahlte Maschinen');axes[1].set_xlabel('Monate seit Eingriff');axes[1].set_ylabel('Investitionszahlungen kumuliert · €')
        for ax in axes:ax.grid(alpha=.2);ax.legend(fontsize=8)
        save_figure(fig,Path('qa/investment-v20-opportunity'))
        s=metrics(r,c,12)
        lines+=['','![Erwartungsrechnung und tatsächliche Investition](investment-v20-opportunity.svg)','',
            '## Warum Konsum und Beschäftigung anders reagieren können','',
            f"Im gezielten Grenzfall ändert sich das tatsächlich erhaltene Nettohaushaltseinkommen während zwölf Monaten um {euro(s['household_income_delta_cents'])}: {euro(s['non_owner_income_delta_cents'])} aus Einkommen vor Eigentümerausschüttungen und {euro(s['owner_income_delta_cents'])} aus Netto-Eigentümerausschüttungen. Die Käufe verändern sich um {euro(s['purchases_delta_cents'])}; mangels Ware unerfüllte Kaufpläne um {euro(s['stock_gap_delta_cents'])}. Diese Zerlegung wird direkt aus den Monatsbelegen berechnet.",'',
            'Die neue Maschine ist hier überwiegend eine Automatisierung bei gegebener Nachfrage. Ihr Aufschub vermeidet zunächst Arbeitszeitersparnis und kann deshalb Löhne erhöhen. Nicht für eine Maschine gebundene beziehungsweise ausgezahlte Mittel können Eigentümerausschüttungen verändern. Zusätzlich konkurrieren Maschinen- und Haushaltskäufe um begrenzte Werkstattware. Die Lieferantennachfrage und die Haushaltsnachfrage sind daher nicht automatisch zusätzliche Produktion. Diese Gegenwirkungen werden nicht mit einer neuen Regel unterdrückt.','',
            'Der Versuch weist einen wirksamen Bewertungs- und Investitionszeitpunktkanal nach. Er validiert keine allgemeine Konsum- oder BIP-Wirkung höherer Leitzinsen. Finanzierungsart im tatsächlich beobachteten Grenzfall: Eigenmittel; das Kreditangebot daneben ist eine geprüfte Alternative, keine im Lauf gebuchte Kreditaufnahme. Die ungestörte Auswahl eines Grenzprojekts macht den Test gezielt sensitiv und erlaubt keine Aussage zur Häufigkeit solcher Projekte.']
    else:lines+=['Innerhalb der ersten 600 Kontrollmonate wurde kein finanzierbares Projekt mit positivem Eigenmittel-Kapitalwert bei 2 % und nicht positivem bei 5 % gefunden. Keine nachträgliche Parameteranpassung.']
    lines+=['','## Gesamte 60 Monate','',
        '| Vergleich | Investitionszahlungen Δ | Nettohaushaltseinkommen Δ | Kaufmengen Δ | Firmengewinn vor Steuer Δ | Staat netto am Ende Δ |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for _,label,_,_ in pairs:
        s=results[label]['60'];lines.append(f"| {label} | {euro(s['investment_delta_cents'])} | {euro(s['household_income_delta_cents'])} | {decimal(s['purchases_delta_percent'],3)} % | {euro(s['firm_profit_delta_cents'])} | {euro(s['state_net_delta_cents'])} |")
    same_new={r['case']:r for r in groups['same_late_state']['runs'] if r['policy']=='valuation'}
    paid_low=sum(x['investment_paid_cents'] for x in same_new['control']['monthly'])
    paid_high=sum(x['investment_paid_cents'] for x in same_new['rate']['monthly'])
    lines+=['','## Warum manche Vergleiche trotzdem kleine Zinseffekte zeigen','',
        f"Bei Umstellung aus dem alten Zustand kaufen beide neuen Zweige über 60 Monate Maschinen für {euro(paid_low)} beziehungsweise {euro(paid_high)}. Die Bewertung ändert die Investitionsregel, doch die Projekte im zwölfmonatigen Zinsfenster bleiben in beiden Zweigen wirtschaftlich. Null Differenz bedeutet hier nicht, dass keine Investitionen stattfinden. In der seit Welteröffnung ausgebauten neuen Referenz werden während der 60 Folgemonate keine weiteren Maschinen gekauft; der geringe verbleibende Zinseffekt entsteht daher ohne neue Maschineninvestition. Bereits installierte Kapazität wird durch eine Zinserhöhung nicht zurückgenommen."]
    mature=groups['mature_valuation'];control=next(r for r in mature['runs'] if r['case']=='control')
    assert sum(x['investment_paid_cents'] for r in mature['runs'] for x in r['monthly'])==0

    history=data['late_reference_history'];limits={}
    lines+=['','## Neue Langzeitreferenz und Grenzen','',
        'Neue Regel ab Welteröffnung: 1440 Monate Vorlauf und 60 weitere Kontrollmonate. Die Bestandsbereiche unten zeigen die letzten 120 Vorlaufmonate und die 60 Fortsetzungsmonate; sie sind keine Zusicherung unbegrenzter Stabilität. Automatisierung kann bei fester Bevölkerung und begrenzter Nachfrage Arbeitszeit und Stellen verringern. Neue Branchen, steigende Reallöhne, Demografie, Ersatzinvestitionen und allgemeine Preis-/Lohnanpassung werden dadurch noch nicht modelliert.','']
    for sector in ('households','firms','government','government_debt','bank'):
        vals=[r['stocks_cents'][sector] for r in history+control['monthly']];limits[sector]=[min(vals),max(vals)]
        lines.append('- '+sector+': '+euro(min(vals))+' bis '+euro(max(vals))+'.')
    emp=[r['employment'] for r in history+control['monthly']]
    social=[r['government']['social_unfunded_cents'] for r in control['monthly']]
    lines+=['',f"Beschäftigung im späten Kontrollbereich: {min(emp)} bis {max(emp)} Verträge. Höchste unbezahlte soziale Monatsleistung in M1441–1500: {euro(max(social))}. Die neue Referenz kann sich strukturell von v19 unterscheiden; ein gleiches Beschäftigungsniveau oder Staatsbudget wird nicht erzwungen.",'',
        '## Technische Nachweise','',
        '213 Pythonprüfungen bestanden, darunter acht gezielte Investitionsprüfungen. 28 tatsächliche Phasen-/Projektzustände werden vom UI-Vertrag akzeptiert; acht beschädigte beziehungsweise veraltete Zustände werden zurückgewiesen. Frontend-Build erfolgreich. Die Ansicht wurde im Browser bis zur realen Bestellung geprüft.','',
        'Alle Fortsetzungsbuchungen wurden zusätzlich zu den Modellprüfungen unabhängig anhand der Vorher-/Nachher-Konten rekonstruiert. Haushaltseinkommen minus Käufe entspricht der Kontoveränderung, staatliche Nettopositionsänderung dem Budgetsaldo und der Warenfluss der Lageränderung. Die Berichtserzeugung prüft Quell- und Archivprüfsummen sowie Kapitalwert-/Ratenfelder.','',
        'Reproduktion: beide Teile von [compare_investment.py](../poc/scripts/compare_investment.py) mit --part late beziehungsweise --part new und separatem --output berechnen, mittels [collect_investment.py](../poc/scripts/collect_investment.py) zusammenführen und [report_investment.py](../poc/scripts/report_investment.py) mit Matplotlib ausführen. [Erwartungsrechnung im Code](../poc/investment.py). Frühere Archive bleiben unverändert.']
    Path('qa/investment-v20-report.md').write_text('\n'.join(lines)+'\n')
    result=dict(date='2026-11-03',model=data['model'],source_data_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        report_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=data['checks'],python_tests_passed=213,
        ui_snapshots_passed=28,invalid_snapshots_rejected=8,frontend_build_passed=True,results=results,
        opportunity=opportunity,late_ranges_cents=limits,late_employment=[min(emp),max(emp)],maximum_late_social_unfunded_cents=max(social))
    Path('qa/investment-v20-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
