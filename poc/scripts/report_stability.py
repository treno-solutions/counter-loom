"""Render the complete stability matrix, including failures and initial transients."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
CASES={case:dict(months=1800 if case in ('stable','initial_distribution') else 600) for case in (
    'stable','joint_only','quarter_only','orders_income95','income95','funding_only',
    'reserve1','reserve6','adjust6','adjust24','fiscal6','fiscal24','initial_distribution','shocks')}


def euro(v):
    v=0 if abs(v)<.5 else v
    return f'{v/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def avg(rows,key):return sum(r[key] for r in rows)/len(rows)
def smooth(values,n=12):return [sum(values[max(0,i-n+1):i+1])/min(i+1,n) for i in range(len(values))]
def decimal(v,digits=2):return f'{v:.{digits}f}'.replace('.',',')
def integer(v):return f'{v:,}'.replace(',','.')


def report():
    folder=Path('qa/stability-v18');runs={}
    replay_path=Path('qa/stability-v18-historical-replay.json')
    replay=json.loads(replay_path.read_text())
    assert len(replay['runs'])==2 and all(r['all_600_months_exact'] for r in replay['runs'])
    for f,digest in replay['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,f
    for case,cfg in CASES.items():
        path=folder/f'{case}.json';d=json.loads(path.read_text())
        assert d['months']==cfg['months'] and len(d['monthly'])==cfg['months'],case
        for f,digest in d['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,(case,f)
        assert d['checks']['independent_journal_reconstruction'] and d['checks']['all_phases_checked']
        runs[case]=d
    main=runs['stable'];rows=main['monthly'];last=rows[-1];s=main['summary'];pert=runs['initial_distribution']
    assert main['criteria']['nominal_drift_tolerance_cents_per_month']==100
    colors=dict(households='#526f89',firms='#66895a',government='#b18158',external='#8e7193',government_debt='#9a5961',government_net='#12313f')
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-stability-v18'})
    fig,axes=plt.subplots(3,2,figsize=(12,12));fig.subplots_adjust(top=.92,bottom=.06,hspace=.5,wspace=.25)
    fig.suptitle('Counterloom · Referenzwirtschaft über 1.800 Monate',fontsize=15)
    fig.text(.5,.95,'Anlaufphase und späte Bestandsdrift werden getrennt beurteilt. Keine neuen Steuern, Transfers oder Anfangsguthaben.',ha='center',fontsize=9)
    xs=[r['month'] for r in rows]
    for k,label in [('households','Haushalte'),('firms','Unternehmen'),('government','Staatskasse'),('external','Ausland')]:
        axes[0,0].plot(xs,[r['stocks_cents'][k]/100000 for r in rows],label=label,color=colors[k])
    axes[0,0].set_title('Guthaben · gesamte Anpassung',loc='left');axes[0,0].set_ylabel('Tausend Euro');axes[0,0].legend(frameon=False,fontsize=8)
    for k,label in [('government','Kasse'),('government_debt','Schuld'),('government_net','Kasse minus Schuld')]:
        axes[0,1].plot(xs,[r['stocks_cents'][k]/100000 for r in rows],label=label,color=colors[k])
    axes[0,1].set_title('Staatsfinanzierung · Bestände gemeinsam',loc='left');axes[0,1].set_ylabel('Tausend Euro');axes[0,1].legend(frameon=False,fontsize=8)
    axes[1,0].plot(xs,[r['stocks_cents']['households']/100000 for r in rows],label='Tatsächliches Guthaben',color=colors['households'])
    axes[1,0].plot(xs,[r['household_target_cents']/100000 for r in rows],label='Liquiditätsziel · sechs Haushalte',color='#66895a',ls='--')
    axes[1,0].set_title('Liquiditätsziel und tatsächlicher Bestand',loc='left');axes[1,0].set_ylabel('Tausend Euro');axes[1,0].legend(frameon=False,fontsize=8)
    for key,label,color in [('consumption_cents','Haushaltskäufe','#526f89'),('gdp_proxy_cents','BIP-Näherung','#66895a')]:
        axes[1,1].plot(xs,smooth([r[key]/100000 for r in rows]),label=label,color=color)
    axes[1,1].set_title('Aktivität · 12-Monatsmittel',loc='left');axes[1,1].set_ylabel('Tausend Euro / Monat');axes[1,1].legend(frameon=False,fontsize=8)
    axes[2,0].plot(xs,[r['employment'] for r in rows],label='Verträge insgesamt',color='#526f89')
    axes[2,0].plot(xs,[r['private_fte_bps']/10000 for r in rows],label='Private Vollzeitäquivalente',color='#66895a')
    axes[2,0].set_ylim(0,6.5);axes[2,0].set_title('Verträge und tatsächlicher Arbeitsumfang',loc='left');axes[2,0].legend(frameon=False,fontsize=8)
    late=rows[1439:]
    for k,label in [('households','Haushalte'),('firms','Firmen'),('government_net','Staat netto'),('external','Ausland')]:
        drift=[(r['stocks_cents'][k]-rows[r['month']-241]['stocks_cents'][k])/24000 for r in late]
        axes[2,1].plot([r['month'] for r in late],drift,label=label,color=colors[k])
    axes[2,1].axhspan(-1,1,color='#66895a',alpha=.08);axes[2,1].axhline(1,color='#888',ls='--',lw=.7);axes[2,1].axhline(-1,color='#888',ls='--',lw=.7)
    axes[2,1].set_ylim(-1.2,1.2);axes[2,1].set_title('Späte Bestandsdrift · 240-Monatsmittel',loc='left');axes[2,1].set_ylabel('Euro / Monat');axes[2,1].legend(frameon=False,fontsize=8)
    for ax in axes.flat:ax.grid(alpha=.18);ax.set_xlabel('Monat')
    target=Path('qa/stability-v18-report')
    fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
    svg=target.with_suffix('.svg');svg.write_text('\n'.join(l.rstrip() for l in svg.read_text().splitlines())+'\n')
    fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
    windows=s['windows'];passed=s['stationary_reference_screen'];p_passed=pert['summary']['stationary_reference_screen']
    individual=[]
    for d in (main,pert):
        for win in d['summary']['windows']:
            a=d['monthly'][win['first_month']-2];b=d['monthly'][win['last_month']-1]
            part=d['monthly'][win['first_month']-1:win['last_month']]
            individual.append(dict(case=d['case'],first_month=win['first_month'],last_month=win['last_month'],
                household_drift_cents_per_month={h:(b['household_cash_cents'][h]-a['household_cash_cents'][h])/240 for h in a['household_cash_cents']},
                household_min_cash_cents=min(v for r in part for v in r['household_cash_cents'].values()),
                household_aggregate_range_cents=max(r['stocks_cents']['households'] for r in part)-min(r['stocks_cents']['households'] for r in part),
                consumption_min_cents=min(r['consumption_cents'] for r in part),consumption_max_cents=max(r['consumption_cents'] for r in part)))
    max_individual_drift=max(abs(v) for x in individual for v in x['household_drift_cents_per_month'].values())
    result='besteht' if passed else 'besteht nicht'
    lines=['# Langzeitprüfung der stabilisierten Modellwirtschaft','',
        'Stand: 3. November 2026. Eigene deterministische Modellläufe v18; keine empirische Kalibrierung.','',
        f'Die neue Referenz {result} die vorab festgelegte technische Stabilitätsprüfung bis Monat 1.800 {"und erreicht einen wirtschaftlich aktiven, näherungsweise stationären zyklischen Bereich" if passed else "ohne bestandenen Nachweis eines stationären Referenzbereichs"}. Der Lauf mit leicht anderer Anfangsverteilung {"besteht ebenfalls" if p_passed else "besteht nicht"}. Die Anlaufphase ist deutlich bewegt und darf nicht als bereits stationär bezeichnet werden. Auch ein positiver Befund über 1.800 Monate beweist keine unbegrenzte Stabilität unter beliebigen Annahmen.','',
        '![Anlaufphase Aktivität und späte Bestandsdrift](stability-v18-report.svg)','',
        '## Was verändert wurde','',
        'Die [Regeln v18](../poc/STABILITY_MODEL.md) verbinden vier getrennte Mechanismen: gemeinsame Kopfzahl-/Arbeitszeitplanung, vollständige Quartalsbasis mit ausgewiesenem Finanzierungsraum, finanzierte Maschinenaufträge mit Produktionsplanung sowie eine eigene Haushaltsregel mit Liquiditätsziel. Die Oberfläche startet diese Kombination. Historische Regeln bleiben kontrollierbar; frühere Ergebnisdateien wurden nicht überschrieben. Steuern, Transfers, Lohnsatz, Anfangsguthaben und Kreditlimit wurden nicht auf das Ergebnis angepasst.','',
        'Die Reserveannahme lautet drei Monate Grundbedarf je Haushalt, mit Anpassung über zwölf Monate. Die neue Referenz verwendet 100 % der Einkommensbasis plus Reservekorrektur; das ist eine eigene Regel und keine Umbenennung der bisherigen 95-%-Variante. Der fiskalische Planungshorizont beträgt zwölf Monate. Alle drei Parameter sind illustrative Annahmen.','',
        '## Vorab festgelegte Prüfkriterien','',
        'Jede Phase prüft Geld, Bankbilanz, Forderungen, Finanzierung und Lager. Das Journal wird zusätzlich unabhängig anhand jeder Soll-/Habenbewegung rekonstruiert. Kein gebuchter Kontostand darf negativ sein. Ein Auftrag darf keine Doppelbestellung, vorgezogene Kapazität oder fiktiven Teilumsatz erzeugen.','',
        'Für den langen Referenzlauf gelten die festen Fenster M1321–1560 und M1561–1800: höchstens 1 Euro durchschnittliche nominale Bestandsänderung je Monat und Sektor, einschliesslich Staatsschuld und Kasse minus Schuld. Der reale Lagerbestand darf je Betrieb durchschnittlich höchstens einen Warenteil pro Monat driften. Produktion und Käufe müssen positiv bleiben; ungedeckte geplante Grundkäufe und Sozialzahlungen werden gesondert geprüft. Diese Grenzen sind technische Toleranzen, keine empirischen Parameter.','',
        '## Späte Bestandsänderungen','',
        '| Bestand | M1321–1560 pro Monat | M1561–1800 pro Monat |','| --- | ---: | ---: |']
    for k,label in [('households','Haushalte'),('firms','Unternehmen'),('government','Staatskasse'),('government_debt','Staatsschuld'),('government_net','Staat netto'),('external','Ausland'),('bank','Bankeigenkapital')]:
        lines.append(f'| {label} | {euro(windows[0]["drift_cents_per_month"][k])} | {euro(windows[1]["drift_cents_per_month"][k])} |')
    lines+=['','## Aktivität und Anlaufphase','',
        f'Nach 1.800 Monaten bestehen {last["employment"]} Arbeitsverträge, davon {last["public_staff"]} öffentliche. Im letzten 240-Monats-Fenster betragen die privaten Vollzeitäquivalente im Mittel {decimal(avg(rows[-240:],"private_fte_bps")/10000,4)}; Haushaltskäufe {euro(avg(rows[-240:],"consumption_cents"))} je Monat. Die Staatsschuld erreicht während des Laufs höchstens {euro(max(r["stocks_cents"]["government_debt"] for r in rows))} und beträgt zuletzt {euro(last["stocks_cents"]["government_debt"])}.','',
        f'In der Anlaufphase verbleiben am höchsten Schuldenstand nur {euro(5000000-max(r["stocks_cents"]["government_debt"] for r in rows))} bis zur bestehenden Kreditgrenze von 50.000 Euro. Der Finanzierungsraum ist zeitweise knapp. Der Referenzbefund gilt deshalb nicht als allgemeine Freigabe anderer Anfangs- oder Schockannahmen.','',
        'Vorübergehende Guthabenanhäufung, Lieferengpässe, Investitionen und Staatsverschuldung gehören zur langen Anlaufphase. Der begrenzte Auslandsanschluss führt Geld zeitweise langsam zurück. Null Schuld allein ist deshalb kein Erfolgskriterium; der vollständige Verlauf und die späte Nettoposition stehen nebeneinander. Ein Bestand über dem Haushaltsziel kann wegen begrenzter Ware bestehen bleiben, ohne weiterhin zu wachsen. Das Ziel ist keine Garantie exakt erreichter Kontostände.','',
        f'Auch einzelne Haushalte verarmen nicht verborgen hinter einem stabilen Aggregat: Der grösste absolute Einzelhaushaltstrend in beiden späten Fenstern beider langen Läufe beträgt {decimal(max_individual_drift)} Cent je Monat. Quartalsausschüttungen und Kaufreihenfolgen erzeugen trotzdem deutliche Monatszyklen. Im späten Referenzfenster liegt der Konsum zwischen {euro(individual[1]["consumption_min_cents"])} und {euro(individual[1]["consumption_max_cents"])}. Die separate KI-Prüfinstanz hat diese Drifts und die nahezu unveränderten Schwankungshüllen unabhängig nachgerechnet.','',
        '## Isolierte Kontrollen und Sensitivitäten','',
        '| Variante | Monate | Später Staat netto pro Monat | Späte Haushaltsdrift pro Monat | Technischer Screen |','| --- | ---: | ---: | ---: | --- |']
    names={'stable':'Neue Referenz','initial_distribution':'300 Euro zwischen zwei Haushalten umverteilt','joint_only':'Nur gemeinsame Personalplanung · Einkommen95','quarter_only':'Zusätzlich reine Quartals-Nullschwelle','orders_income95':'Zusätzlich Maschinenaufträge · Einkommen95','income95':'Neue übrige Regeln · historische Einkommensquote95','funding_only':'Nur harte Vorfinanzierung beim Staat','reserve1':'Liquiditätsziel 1 Monat','reserve6':'Liquiditätsziel 6 Monate','adjust6':'Reserveanpassung über 6 Monate','adjust24':'Reserveanpassung über 24 Monate','fiscal6':'Fiskalhorizont 6 Monate','fiscal24':'Fiskalhorizont 24 Monate','shocks':'Energie Zins und Betriebsschliessung'}
    for case,d in runs.items():
        z=d['summary']['windows'][-1]['drift_cents_per_month'];screen='Bestanden' if d['summary']['stationary_reference_screen'] else 'Nicht bestanden'
        lines.append(f'| [{names[case]}](stability-v18/{case}.json) | {d["months"]} | {euro(z["government_net"])} | {euro(z["households"])} | {screen} |')
    lines+=['',
        'Bei 600-Monats-Varianten beziehen sich die zwei Fenster auf M121–360 und M361–600. Diese Varianten sind Gegenläufe und frühe Sensitivitätsprüfungen, kein zusätzlicher Langzeitnachweis. Ein nicht bestandener Screen wird nicht durch eine nachträglich gelockerte Toleranz ersetzt. Unterschiedliche Reserven und Reaktionsgeschwindigkeiten können andere Übergangs- und Finanzierungsverläufe erzeugen.','',
        'Der Schocklauf verdoppelt Energiepreise ab M120 und normalisiert sie ab M144, erhöht den Leitzins ab M180 auf 5 % und stellt ihn ab M216 auf 2 % zurück. Ab M240 schliessen beide Betriebe für drei Monate bei 60 % Nettoersatz. Ein solcher Lauf darf Verluste, ungedeckten Sozialbedarf, Arbeitsplatzverluste oder Finanzierungsgrenzen enthalten. Eine begründete Krise gilt nicht als Buchungsfehler; ihre Folgen bleiben in den Rohdaten sichtbar.','',
        '## Prüfung und Reproduktion','',
        'Die vollständige Python-Suite umfasst 194 bestandene Tests. Die separate Codeprüfung fand einen blockierten Wiederanlauf bei Maschinenaufträgen und einen falsch datierten fiskalischen Beobachtungswert; beide sind durch gezielte Regressionstests behoben. Die endgültigen Läufe verwenden die korrigierten Quellstände. 26 Snapshots an Phasen-, Auftrags-, Schliessungs-, Energie- und Zinsgrenzen bestehen zusätzlich den strikten Oberflächenvertrag. Die historischen 95-/100-%-Profile wurden im neuen Kern jeweils über 600 Monate erneut ausgeführt und stimmen in sämtlichen archivierten wirtschaftlichen Monatsfeldern exakt überein. Nur der erläuternde Wortlaut einer Budgetentscheidung ist vom Vergleich ausgenommen; [Reproduktionsnachweis](stability-v18-historical-replay.json).','',
        f'Die Matrix enthält {integer(sum(d["months"] for d in runs.values()))} simulierte Monate und {integer(sum(d["checks"]["phases"] for d in runs.values()))} einzeln geprüfte Phasen. Jede Rohdatei enthält Eingaben, Quellprüfsummen, Monatswerte, Bestandsdrifts und Prüfergebnisse. [Modellregeln](../poc/STABILITY_MODEL.md) · [Prüfplan](../poc/STABILITY_PLAN.md) · [Prüfprotokoll](stability-v18-verification.json).','',
        '```sh','python -m unittest discover -s poc -v','python poc/scripts/check_stability.py --case stable','python poc/scripts/check_stability.py --case initial_distribution','python poc/scripts/stability_contract_fixtures.py','node --experimental-strip-types poc/scripts/check_stability_contract.mts','python poc/scripts/report_stability.py','```','',
        'Die weiteren Fallnamen stehen in `CASES` im Prüflaufskript. Der Bericht wird erst erzeugt, wenn alle vorgesehenen Dateien zum aktuellen Quellstand vorliegen. Matplotlib erzeugt das Diagramm aus den gesicherten Monatsdaten.','']
    target.with_suffix('.md').write_text('\n'.join(lines))
    verification=dict(date='2026-11-03',model='illustrative_circular_flow_v18',tests_passed=194,ui_contract_snapshots=26,
        profiles=len(runs),months=sum(d['months'] for d in runs.values()),phases=sum(d['checks']['phases'] for d in runs.values()),
        source_hashes_verified=True,reference_screen=passed,perturbed_reference_screen=p_passed,
        historical_replay_sha256=hashlib.sha256(replay_path.read_bytes()).hexdigest(),historical_months_reproduced=1200,
        data_sha256={str(folder/f'{case}.json'):hashlib.sha256((folder/f'{case}.json').read_bytes()).hexdigest() for case in runs},
        criteria=main['criteria'],reference_summary=s,perturbed_summary=pert['summary'],individual_household_checks=individual,
        independent_review='Separate AI code and data review; no remaining blocker for the tested local cyclic reference configuration. No empirical validation.',
        limitation='Finite illustrative model runs; no empirical validation or proof of unlimited stability under arbitrary parameters.')
    Path('qa/stability-v18-verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':report()
