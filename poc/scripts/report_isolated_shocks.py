"""Compare sector responses to isolated shocks against the same control path."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SOURCE=Path('qa/isolated-shocks-v18-2026-11-03.json')
NAMES={'control':'Ungestörter Vergleich','rate':'Leitzins 2 auf 5 %','energy':'Energiekosten verdoppelt',
    'closure_no_support':'Schliessung ohne Ersatzleistung','closure_support60':'Schliessung mit 60 % Ersatzleistung'}
COLORS={'rate':'#526f89','energy':'#b18158','closure_no_support':'#9a5961','closure_support60':'#66895a'}


def euro(cents):
    v=0 if abs(cents)<.5 else cents
    return f'{v/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def decimal(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def ratio(value,base):
    assert base>0
    return (value/base-1)*100
def total(rows,key):return sum(r[key] for r in rows)
def by_id(rows,key,id):return next(r for r in rows[key] if r['id']==id)


def validate(data):
    for f,digest in data['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,f
    assert hashlib.sha256(Path(data['reference']).read_bytes()).hexdigest()==data['reference_sha256']
    assert [r['case'] for r in data['runs']]==list(NAMES)
    assert data['checks']['warmup_matches_all_reference_months']
    for run in data['runs']:
        assert run['initial']==data['anchor'] and len(run['monthly'])==60
        assert run['checks']['journal_reconstruction'] and run['checks']['base_state_unchanged']
        before=data['anchor'];ledger=iter(run['transactions']);tx=next(ledger,None)
        last_pre=data['pre_shock_monthly'][-1]
        accounts={h['id']:h['cash_cents'] for h in last_pre['households']}
        accounts.update({f['id']:f['cash_cents'] for f in last_pre['firms']})
        accounts.update(staat=before['stocks_cents']['government'],bank=before['stocks_cents']['bank'],ausland=before['stocks_cents']['external'])
        previous_cash=data['anchor']['household_cash_cents']
        for row in run['monthly']:
            while tx is not None and tx['month']==row['month']:
                assert accounts[tx['source']]==tx['source_before'] and accounts[tx['target']]==tx['target_before']
                if tx['ledger_effect']!='loan_creation':accounts[tx['source']]-=tx['amount_cents']
                if tx['ledger_effect']!='principal_repayment':accounts[tx['target']]+=tx['amount_cents']
                assert accounts[tx['source']]==tx['source_after'] and accounts[tx['target']]==tx['target_after']
                tx=next(ledger,None)
            assert row['stocks_cents']['government_net']-before['stocks_cents']['government_net']==row['government']['cash_balance_cents']
            for h in row['households']:
                assert h['cash_cents']-previous_cash[h['id']]==h['disposable_received_cents']-h['consumption_cents']
                assert accounts[h['id']]==h['cash_cents']
            for f in row['firms']:
                assert f['opening_inventory_units']+f['produced_units']-f['sold_units']==f['inventory_units']
                assert accounts[f['id']]==f['cash_cents']
            assert accounts['staat']==row['stocks_cents']['government']
            assert accounts['bank']==row['stocks_cents']['bank'] and accounts['ausland']==row['stocks_cents']['external']
            previous_cash=row['household_cash_cents'];before=row
        assert tx is None
    assert data['runs'][0]['checks']['control_matches_archive']


def statistics(run,control):
    rows=run['monthly'];base=control['monthly'];active=3 if run['case'].startswith('closure_') else 12
    r,b=rows[:active],base[:active]
    firm_stats=[];household_stats=[]
    for id in ('alltag','werkstatt'):
        change=lambda key:sum(by_id(x,'firms',id)[key]-by_id(y,'firms',id)[key] for x,y in zip(r,b))
        firm_stats.append(dict(id=id,sales_delta_cents=change('sales_cents'),profit_delta_cents=change('profit_before_tax_cents'),
            wages_delta_cents=change('wages_cents'),energy_delta_cents=change('energy_paid_cents'),interest_delta_cents=change('interest_paid_cents'),
            minimum_paid_fte_bps=min(by_id(x,'firms',id)['paid_fte_bps'] for x in rows),
            end_cash_delta_cents=by_id(rows[-1],'firms',id)['cash_cents']-by_id(base[-1],'firms',id)['cash_cents']))
    for id in ('h1','h2','h3','h4','h5','h6'):
        change=lambda key:sum(by_id(x,'households',id)[key]-by_id(y,'households',id)[key] for x,y in zip(r,b))
        household_stats.append(dict(id=id,income_delta_cents=change('disposable_received_cents'),
            nominal_consumption_delta_cents=change('consumption_cents'),
            base_price_consumption_delta_cents=change('consumption_base_price_cents'),
            end_cash_delta_cents=by_id(rows[-1],'households',id)['cash_cents']-by_id(base[-1],'households',id)['cash_cents'],
            minimum_cash_cents=min(by_id(x,'households',id)['cash_cents'] for x in rows)))
    state_change=lambda key:sum(x['government'][key]-y['government'][key] for x,y in zip(r,b))
    def bank_net_payout(branch):
        tx=branch['transactions'];amount=0
        for i,t in enumerate(tx):
            if t['kind']=='dividend' and r[0]['month']<=t['month']<=r[-1]['month']:
                tax=tx[i+1]['amount_cents'] if i+1<len(tx) and tx[i+1]['kind']=='distribution_tax' and tx[i+1]['source']==t['target'] else 0
                amount+=t['amount_cents']-tax
        return amount
    bank_delta=bank_net_payout(run)-bank_net_payout(control)
    owner_delta=sum(h['owner_payout_net_cents'] for x in r for h in x['households'])-sum(h['owner_payout_net_cents'] for x in b for h in x['households'])
    non_owner_delta=sum(h['income_before_owner_payout_cents'] for x in r for h in x['households'])-sum(h['income_before_owner_payout_cents'] for x in b for h in x['households'])
    assert non_owner_delta+owner_delta==total(r,'disposable_received_cents')-total(b,'disposable_received_cents')
    state_deltas=[x['stocks_cents']['government_net']-y['stocks_cents']['government_net'] for x,y in zip(rows,base)]
    return dict(case=run['case'],active_months=active,
        bank_net_payout_delta_cents=bank_delta,firm_net_payout_delta_cents=owner_delta-bank_delta,non_owner_income_delta_cents=non_owner_delta,
        income_delta_cents=total(r,'disposable_received_cents')-total(b,'disposable_received_cents'),
        real_consumption_delta_percent=ratio(total(r,'consumption_base_price_cents'),total(b,'consumption_base_price_cents')),
        nominal_consumption_delta_cents=total(r,'consumption_cents')-total(b,'consumption_cents'),
        profit_delta_cents=sum(f['profit_delta_cents'] for f in firm_stats),
        government_net_delta_active_cents=r[-1]['stocks_cents']['government_net']-b[-1]['stocks_cents']['government_net'],
        government_net_delta_60_cents=rows[-1]['stocks_cents']['government_net']-base[-1]['stocks_cents']['government_net'],
        minimum_government_net_delta_cents=min(state_deltas),minimum_government_net_relative_month=state_deltas.index(min(state_deltas))+1,
        minimum_government_closing_cash_cents=min(x['stocks_cents']['government'] for x in rows),
        taxes_delta_cents=state_change('taxes_cents'),short_time_delta_cents=state_change('short_time_paid_cents'),
        minimum_employment=min(x['employment'] for x in rows),minimum_paid_private_fte_bps=min(x['paid_private_fte_bps'] for x in rows),
        peak_price_index_bps=max(x['price_index_bps'] for x in rows),
        total_interest_delta_cents=sum(sum(f['interest_paid_cents'] for f in x['firms'])-sum(f['interest_paid_cents'] for f in y['firms']) for x,y in zip(rows,base)),
        end_real_consumption_delta_percent=ratio(total(rows[-12:],'consumption_base_price_cents'),total(base[-12:],'consumption_base_price_cents')),
        total_real_consumption_delta_percent=ratio(total(rows,'consumption_base_price_cents'),total(base,'consumption_base_price_cents')),
        social_unfunded_cents=sum(x['government']['social_unfunded_cents'] for x in rows),
        maximum_government_debt_cents=max(x['stocks_cents']['government_debt'] for x in rows),firms=firm_stats,households=household_stats)


def save_figure(fig,path):
    fig.savefig(path.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
    p=path.with_suffix('.svg');p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')
    fig.savefig(path.with_suffix('.png'),dpi=130);plt.close(fig)


def report():
    data=json.loads(SOURCE.read_text());validate(data)
    runs={r['case']:r for r in data['runs']};control=runs['control'];stats={k:statistics(v,control) for k,v in runs.items() if k!='control'}
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-isolated-v18'})
    fig,axes=plt.subplots(3,3,figsize=(14,11));fig.subplots_adjust(top=.90,bottom=.07,hspace=.36,wspace=.34)
    fig.suptitle('Counterloom · einzelne Schocks gegenüber derselben ungestörten Wirtschaft',fontsize=14)
    fig.text(.5,.94,'Unverändertes Modell v18 · gemeinsamer Zustand nach M1440 · 60 Monate Beobachtung · alle Linien zeigen Abweichungen',ha='center',fontsize=9)
    groups=[('Zins · 2 auf 5 % für 12 Monate',['rate'],12),('Energiekosten ×2 für 12 Monate',['energy'],12),('Alltag schliesst für 3 Monate',['closure_no_support','closure_support60'],3)]
    for col,(title,cases,duration) in enumerate(groups):
        for case in cases:
            rows=runs[case]['monthly'];base=control['monthly'];x=[0]+[r['relative_month'] for r in rows]
            values=[[0]+[ratio(r['consumption_base_price_cents'],b['consumption_base_price_cents']) for r,b in zip(rows,base)],
                [0]+[(sum(f['profit_before_tax_cents'] for f in r['firms'])-sum(f['profit_before_tax_cents'] for f in b['firms']))/100 for r,b in zip(rows,base)],
                [0]+[(r['stocks_cents']['government_net']-b['stocks_cents']['government_net'])/100 for r,b in zip(rows,base)]]
            for row in range(3):axes[row,col].plot(x,values[row],label=NAMES[case],color=COLORS[case],lw=1.5)
        for row in range(3):
            ax=axes[row,col];ax.axhline(0,color='#777',lw=.6);ax.axvspan(.5,duration+.5,color='#999',alpha=.1);ax.grid(alpha=.18);ax.set_xlim(0,60)
            ax.set_ylabel(['Käufe zu Startpreisen · Δ %','Firmengewinn vor Steuer · Δ € / Monat','Staat: Kasse minus Schuld · Δ €'][row])
            ax.ticklabel_format(axis='y',style='plain',useOffset=False)
            if row==0:ax.set_title(title,fontsize=10,loc='left')
            if row==2:ax.set_xlabel('Monate nach dem gemeinsamen Ausgangsstand')
        if col==2:axes[0,col].legend(frameon=False,fontsize=7,loc='lower right')
    save_figure(fig,Path('qa/isolated-shocks-v18-overview'))
    fig,axes=plt.subplots(2,2,figsize=(12,8));fig.subplots_adjust(top=.88,bottom=.08,hspace=.45,wspace=.27)
    fig.suptitle('Übertragung und betroffene Haushalte',fontsize=14)
    rows=runs['rate']['monthly'];x=[r['relative_month'] for r in rows]
    for key,label,color in [('policy_rate_bps','Leitzins','#526f89'),('variable_rate_bps','Variabler Betriebskredit','#66895a'),('fixed_rate_bps','Fester Altvertrag','#b18158')]:axes[0,0].step([0]+x,[2]+[r[key]/100 for r in rows],where='post',label=label,color=color)
    axes[0,0].set_title('Zinsen: Vertragsbindung und Verzögerung',loc='left');axes[0,0].set_ylabel('% jährlich');axes[0,0].legend(frameon=False,fontsize=8)
    rows=runs['energy']['monthly']
    axes[0,1].plot(x,[r['price_index_bps']/100-100 for r in rows],color=COLORS['energy'])
    axes[0,1].set_title('Energieschock: Warenkorbpreis über Ausgangswert',loc='left');axes[0,1].set_ylabel('% Preisänderung')
    for case,ls in [('closure_no_support','-'),('closure_support60','--')]:
        rows=runs[case]['monthly'];base=control['monthly']
        income=[sum(by_id(r,'households',h)['disposable_received_cents']-by_id(b,'households',h)['disposable_received_cents'] for h in ('h1','h2'))/100 for r,b in zip(rows,base)]
        axes[1,0].plot(x,income,label=NAMES[case],color=COLORS[case],ls=ls)
    axes[1,0].set_title('Haushalte 1 und 2: erhaltenes Nettoeinkommen',loc='left');axes[1,0].set_ylabel('Δ € / Monat');axes[1,0].legend(frameon=False,fontsize=8)
    rows=runs['closure_no_support']['monthly']
    axes[1,1].plot(x,[by_id(r,'firms','alltag')['staff_at_production'] for r in rows],label='Erhaltene Verträge',color='#526f89')
    axes[1,1].plot(x,[by_id(r,'firms','alltag')['paid_fte_bps']/10000 for r in rows],label='Bezahlte Vollzeitäquivalente',color='#66895a')
    axes[1,1].set_title('Geschlossener Betrieb: Verträge und bezahlte Arbeit',loc='left');axes[1,1].set_ylabel('Verträge / Vollzeitäquivalente');axes[1,1].legend(frameon=False,fontsize=8)
    for ax in axes.flat:ax.grid(alpha=.18);ax.set_xlabel('Monate nach Eingriff');ax.set_xlim(0,60)
    save_figure(fig,Path('qa/isolated-shocks-v18-channels'))
    lines=['# Reaktionen auf einzelne Schocks','',
        'Stand: 3. November 2026. Eigene simulierte Befunde im unveränderten Modell v18; keine Prognose realer Haushalte oder Volkswirtschaften.','',
        'Fünf getrennte Fortsetzungen starten aus demselben vollständig berechneten Zustand nach M1440: ein ungestörter Kontrollverlauf, höhere Leitzinsen, höhere Energiekosten und dieselbe Betriebsschliessung mit beziehungsweise ohne Kurzarbeitsleistung. Vorlauf und Kontrolle reproduzieren die wirtschaftlichen Vergleichsfelder des archivierten Referenzlaufs.','',
        f'Die Energiekosten belasten Gewinne, Arbeitszeit und Kaufmengen deutlich; die zu Startpreisen bewerteten Käufe liegen während der zwölf Eingriffsmonate {decimal(abs(stats["energy"]["real_consumption_delta_percent"]))} % unter der Kontrolle. Die Schliessung trifft den Konsum kurzfristig noch stärker. Die Ersatzleistung mindert den Einkommensausfall, kann aber die fehlende Ware nicht ersetzen. Der Zinsschock bleibt klein und leicht konsumsteigernd; der unten ausgewiesene Ausschüttungsweg der Bank ist dabei ein wichtiger Gegenimpuls.','',
        '![Abweichungen der Haushalte Unternehmen und Staatsfinanzen](isolated-shocks-v18-overview.svg)','',
        '## Eingriffe und unmittelbare Folgen','',
        '| Eingriff | Eingriffsmonate | Erhaltenes Nettohaushaltseinkommen kumuliert Δ | Käufe zu Startpreisen Δ | Firmengewinn vor Steuer kumuliert Δ | Staat netto am Ende des Eingriffs Δ |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for case,z in stats.items():lines.append(f'| {NAMES[case]} | {z["active_months"]} | {euro(z["income_delta_cents"])} | {decimal(z["real_consumption_delta_percent"])} % | {euro(z["profit_delta_cents"])} | {euro(z["government_net_delta_active_cents"])} |')
    lines+=['','Alle Abweichungen beziehen sich auf denselben Kalendermonat der Modellkontrolle. Zins und Energie werden nach zwölf Monaten zurückgenommen; der Betrieb öffnet nach drei Monaten. Summierte Flüsse über drei und zwölf Monate sind deshalb keine gleich langen Belastungen. Käufe zu unveränderten Startpreisen sind ein Mengenindikator für die zwei Modellwaren, kein amtlicher realer Konsum.','',
        '## Haushalte','',
        'Nettoeinkommen bedeutet hier tatsächlich erhaltene Löhne und Transfers nach Lohnsteuer plus aktuelle Netto-Eigentümerausschüttungen. Der Kaufplan verwendet dagegen die seit der vorherigen Kaufrunde verfügbaren Ausschüttungen. Diese zeitliche Trennung erklärt, warum Einkommensänderung und Käufe nicht im selben Monat gleich reagieren müssen.','',
        '| Schock und Haushalt | Nettoeinkommen während Eingriff Δ | Käufe zu Startpreisen während Eingriff Δ | Kontostand nach 60 Monaten Δ | Niedrigster Kontostand |','| --- | ---: | ---: | ---: | ---: |']
    for case,z in stats.items():
        for h in z['households']:lines.append(f'| {NAMES[case]} · {h["id"]} | {euro(h["income_delta_cents"])} | {euro(h["base_price_consumption_delta_cents"])} | {euro(h["end_cash_delta_cents"])} | {euro(h["minimum_cash_cents"])} |')
    lines+=['','Haushalte 1 und 2 arbeiten vor dem Eingriff bei Alltag & Versorgung, 3 und 4 bei Werkstatt & Technik, 5 und 6 beim Staat. Alle sechs besitzen im bestehenden Modell gleiche Firmenanteile. Ausschüttungen können deshalb auch nicht unmittelbar betroffene Haushalte erreichen.','',
        '## Unternehmen','',
        '| Schock und Betrieb | Erlöse während Eingriff Δ | Gewinn vor Steuer Δ | Lohnzahlungen Δ | Energiezahlungen Δ | Zinszahlungen Δ |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for case,z in stats.items():
        for f in z['firms']:lines.append(f'| {NAMES[case]} · {f["id"]} | {euro(f["sales_delta_cents"])} | {euro(f["profit_delta_cents"])} | {euro(f["wages_delta_cents"])} | {euro(f["energy_delta_cents"])} | {euro(f["interest_delta_cents"])} |')
    lines+=['',
        'Eine angeordnete Schliessung erhält zunächst Verträge. Die betroffene Firma zahlt währenddessen keine Arbeitslöhne und produziert beziehungsweise verkauft keine Ware. Erhaltungsenergie und Schuldendienst laufen weiter. Ein unveränderter Vertragsbestand bedeutet daher keine unveränderte Arbeit oder Einkommenslage.','',
        '![Zinsbindung Preisreaktion Einkommen und bezahlte Arbeit](isolated-shocks-v18-channels.svg)','',
        '## Staat und verbleibende Folgen','',
        '| Eingriff | Steuereinnahmen während Eingriff Δ | Kurzarbeitszahlungen während Eingriff Δ | Staat netto nach 60 Monaten Δ | Käufe zu Startpreisen über 60 Monate Δ | Käufe in den letzten zwölf Monaten Δ | Höchste Staatsschuld |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for case,z in stats.items():lines.append(f'| {NAMES[case]} | {euro(z["taxes_delta_cents"])} | {euro(z["short_time_delta_cents"])} | {euro(z["government_net_delta_60_cents"])} | {decimal(z["total_real_consumption_delta_percent"])} % | {decimal(z["end_real_consumption_delta_percent"])} % | {euro(z["maximum_government_debt_cents"])} |')
    lines+=['','Kasse minus Schuld wird gemeinsam beurteilt. Ein Schock kann die vorhandene Staatskasse belasten, ohne sofort neue Staatsschulden auszulösen. Die Differenz zur Kontrolle nach 60 Monaten zeigt verbleibende Bestandseffekte; sie ist kein über 60 Monate aufsummierter Bestand.','',
        f'In allen fünf Zweigen bleiben sechs Arbeitsverträge bestehen. Die bezahlte Arbeitszeit verändert sich trotzdem. Kein Zweig nimmt neuen Staatskredit auf; die Belastungen werden aus vorhandener Kasse getragen. Im Kurzarbeitszweig beträgt der niedrigste monatliche Kassenabschluss {euro(stats["closure_support60"]["minimum_government_closing_cash_cents"])}.','',
        f'Der grösste Abstand der staatlichen Nettoposition zur Kontrolle tritt im Kurzarbeitszweig erst in Monat {stats["closure_support60"]["minimum_government_net_relative_month"]} nach Eingriff auf: {euro(stats["closure_support60"]["minimum_government_net_delta_cents"])}. Das ist eine Abweichung vom Vergleich, kein negativer absoluter Kontostand. Steuer- und Nachfragereaktionen laufen nach Wiederöffnung weiter.','',
        '## Aussagegrenzen der drei Übertragungswege','',
        f'Der Zinsschock erhöht allein die Zinszahlung auf den variablen Betriebskredit von 12.000 Euro rechnerisch um 30 Euro je belastetem Monat. Der feste Altvertrag bleibt bei 2 %. Über die gesamte Nachbeobachtung betragen die zusätzlichen tatsächlich gezahlten Firmenzinsen {euro(stats["rate"]["total_interest_delta_cents"])}. Haushaltskredite und verzinste Sparguthaben fehlen. Eine kleine gesamtwirtschaftliche Reaktion ist deshalb eine Grenze dieses Modellausschnitts, kein Beleg für eine generell geringe Wirkung realer Leitzinsen.','',
        f'Während der zwölf Leitzinsmonate verändern sich die Netto-Bankausschüttungen um {euro(stats["rate"]["bank_net_payout_delta_cents"])}, Netto-Firmenausschüttungen um {euro(stats["rate"]["firm_net_payout_delta_cents"])} und die übrigen Nettoeinkünfte um {euro(stats["rate"]["non_owner_income_delta_cents"])}. Diese drei tatsächlich gebuchten Komponenten erklären die Einkommensänderung. Die Bank schüttet ihre vereinnahmten Zinsen im bestehenden Modell an dieselben sechs Haushalte aus; höhere Zinskosten sind deshalb nicht nur ein Geldabfluss aus deren Wirtschaftskreislauf.','',
        f'Beim Energieschock erreicht der Modell-Warenkorbpreisindex höchstens {decimal(stats["energy"]["peak_price_index_bps"]/100)} gegenüber 100 im Ausgangszustand. Die bestehende Regel gibt nur einen Teil der Mehrkosten verzögert weiter. Nominale Ausgaben, reale Warenmengen und Gewinne werden deshalb getrennt betrachtet.','',
        'Bei der Schliessung bleibt ein Teil der gewünschten Käufe mangels Ware unausgeführt. Dieses Geld bleibt auf den Konten und kann nach Wiederöffnung zusätzliche Nachfrage auslösen. Es gibt weder freie Umschichtung des gesamten Kaufbudgets auf die andere Ware noch separat modellierte unvermeidbare Haushaltsmieten und Versicherungen. Die Kontoreaktion bildet daher nicht jede reale Notlage nach; ein Wohlfahrtsverlust zeitlich ausgefallener Käufe wird nicht bewertet. 60 % Kurzarbeitsleistung beziehen sich auf den beim Schliessungsbeginn eingefrorenen Referenz-Nettoarbeitslohn, nicht auf sämtliche Haushaltseinkünfte.','',
        'Der gewählte Schliessungseingriff zerstört keine Anlagen und beendet keine Verträge. Die beobachtete Annäherung an den Kontrollverlauf nach Rücknahme ist deshalb kein Nachweis, dass reale Krisenschäden vollständig nachgeholt werden. Es wird kein empirischer Fiskalmultiplikator aus diesen Versuchen abgeleitet.','',
        '## Nachweise und Reproduktion','',
        '[Vorab festgelegter Versuchsplan](isolated-shocks-v18-plan.md) · [Monatsdaten und kompakter Zahlungsnachweis](isolated-shocks-v18-2026-11-03.json) · [Prüfprotokoll](isolated-shocks-v18-verification.json).','',
        'Fünf neue Tests prüfen Beobachtungsneutralität, die identische Kontrollfortsetzung, isolierte Zustandskopien sowie Zins-, Energie- und Schliessungsgrenzen. Jede der 1.500 Fortsetzungsphasen behält die Kernprüfungen und eine zusätzliche unabhängige Rekonstruktion aller neuen Buchungen. Der gemeinsame Vorlauf umfasst 7.200 weitere geprüfte Phasen. Haushaltseinkommen minus Käufe wird zusätzlich mit der Kontoveränderung abgeglichen; beim Staat entspricht die Änderung von Kasse minus Schuld dem tatsächlichen Budgetsaldo.','',
        '```sh','python -m unittest discover -s poc -p test_isolated_shocks.py -v','python poc/scripts/isolated_shocks.py','python poc/scripts/report_isolated_shocks.py','```','',
        'Das Diagramm benötigt Matplotlib. Vor der Berichtserzeugung werden Quell- und Referenzprüfsummen, alle fünf Zweige und sämtliche neuen Gegenbuchungen geprüft. Die laufende Oberfläche und ihre Regeln wurden für diese Offlineversuche nicht verändert.','']
    Path('qa/isolated-shocks-v18-report.md').write_text('\n'.join(lines))
    verification=dict(date='2026-11-03',model=data['model'],model_rules_changed=False,anchor_month=data['anchor_month'],
        anchor_sha256=data['anchor_sha256'],common_state_replayed=True,control_matches_archive=True,branches=5,
        warmup_phases_checked=data['checks']['warmup_phases_checked'],branch_phases_checked=1500,
        new_tests_passed=5,full_python_suite_passed=199,source_hashes_verified=True,independent_ledger_and_income_reconciliation=True,
        source_data_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),statistics=stats)
    Path('qa/isolated-shocks-v18-verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':report()
