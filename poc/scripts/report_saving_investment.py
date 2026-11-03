"""Report observed saving, investment gates and firm responses; no interventions."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def euro(cents):
    return f'{cents / 100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' €'


def mean(rows, fn):
    return sum(fn(r) for r in rows) / len(rows)


def report(source, output):
    data = json.loads(Path(source).read_text())
    reference = Path(data['reference'])
    assert hashlib.sha256(reference.read_bytes()).hexdigest() == data['reference_sha256']
    old = json.loads(reference.read_text())
    assert data['months'] == 600 and len(data['runs']) == 2
    for path, digest in data['source_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
    for path, digest in old['source_sha256'].items():
        if path in data['source_sha256']:
            assert data['source_sha256'][path] == digest, path
    traces_path = Path('qa/firm-reactions-v16-traces-2026-11-03.json')
    traces = json.loads(traces_path.read_text())
    stats = []
    for run, original, traced in zip(data['runs'], old['runs'], traces['runs']):
        quota = run['consumption_percent']
        assert quota == original['consumption_percent'] == traced['consumption_percent']
        rows = run['monthly']
        assert len(rows) == 600 and run['reference_exact_monthly_match']
        gates = [r['investment_gate'] for r in rows]
        late = rows[-120:]
        ref_late = original['monthly'][-120:]
        flow = lambda r, kinds: sum(f['amount_cents'] for f in r['flows'] if f['kind'] in kinds and f['target'] == 'households')
        current_dividends = [flow(r, ('company_dividend', 'company_extra_dividend', 'dividend'))
            - sum(f['amount_cents'] for f in r['flows'] if f['kind'] == 'distribution_tax' and f['source'] == 'households')
            for r in rows]
        for i, (row, base) in enumerate(zip(rows, original['monthly'])):
            gaps = base['purchase_totals']
            prior = current_dividends[i - 1] if i else 0
            # Distinguish saving intention, unfilled purchases and payout timing.
            expected = row['planned_retention_cents'] + sum(gaps[k] for k in ('funding_gap_cents', 'stock_gap_cents', 'unit_remainder_cents')) + current_dividends[i] - prior
            assert expected == row['household_saving_cents'], (quota, i + 1)
            cash = row['cash_change_cents']
            ref_prev = original['monthly'][i - 1]['government_debt_cents'] if i else 0
            assert sum(cash.values()) == base['government_debt_cents'] - ref_prev
        s = dict(quota=quota,
            shortage_gate_months=sum(g['checks']['repeated_shortage'] for g in gates),
            stock_gate_months=sum(g['checks']['stock'] for g in gates),
            shortage_and_stock_months=sum(g['checks']['repeated_shortage'] and g['checks']['stock'] for g in gates),
            cash_gate_months=sum(g['checks']['cash'] for g in gates),
            invested_cents=sum(g['executed_investment_cents'] for g in gates),
            shortage_gate_details=[dict(month=g['month'],supplier_free_units=g['supplier_free_units'],machine_units=g['machine_units']) for g in gates if g['checks']['repeated_shortage']],
            average_private_fte=mean(ref_late, lambda r: r['macro']['private_fte_bps']) / 10000,
            average_retention_cents=mean(late, lambda r:r['planned_retention_cents']),
            average_saving_cents=mean(late, lambda r:r['household_saving_cents']),
            average_inventory_change_cents=mean(late, lambda r:r['inventory_change_cents']),
            average_sector_cash_changes={k:mean(late, lambda r:r['cash_change_cents'][k]) for k in late[0]['cash_change_cents']},
            average_debt_change_cents=(original['monthly'][-1]['government_debt_cents']-original['monthly'][479]['government_debt_cents'])/120,
            average_dividend_timing_cents=(current_dividends[-1]-current_dividends[479])/120,
            average_stock_gap_cents=mean(ref_late,lambda r:r['purchase_totals']['stock_gap_cents']),
            average_unit_remainder_cents=mean(ref_late,lambda r:r['purchase_totals']['unit_remainder_cents']),
            shortage_months={k:sum(next(f for f in r['firms'] if f['id']==k)['unmet_units']>0 for r in traced['monthly']) for k in ('alltag','werkstatt')})
        assert s['invested_cents'] == sum(r['macro']['components']['investment_cents'] for r in original['monthly'])
        stats.append(s)
    target = Path(output)
    target.parent.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-saving-investment-v16'})
    fig, axes = plt.subplots(2,2,figsize=(12,9))
    fig.subplots_adjust(top=.89,bottom=.08,hspace=.44,wspace=.27)
    fig.suptitle('Counterloom · Sparen, Kapazität und Investitionen',fontsize=15)
    fig.text(.5,.94,'Bestehendes Modell v16 · zwei beobachtete 600-Monats-Läufe · unveränderte Regeln',ha='center')
    colors = ['#526f89','#66895a']
    for s, r, color in zip(stats,old['runs'],colors):
        rows=r['monthly']; xs=[m['month'] for m in rows]
        values=[m['macro']['private_fte_bps']/10000 for m in rows]
        smooth=[sum(values[max(0,i-11):i+1])/min(i+1,12) for i in range(len(values))]
        axes[0,0].plot(xs,smooth,color=color,label=f'{s["quota"]} % Konsumquote')
    axes[0,0].set_title('Private Arbeitszeit · 12-Monatsmittel',loc='left')
    axes[0,0].set_ylabel('Vollzeitäquivalente');axes[0,0].set_xlabel('Monat');axes[0,0].set_ylim(0,4.3)
    axes[0,0].legend(frameon=False)
    labels=['2 vorherige\nEngpassmonate','Genug\nWerkstattlager','Beides\ngleichzeitig']
    for i,(s,color) in enumerate(zip(stats,colors)):
        bars=axes[0,1].bar([v+(i-.5)*.32 for v in range(3)],[s[k] for k in ('shortage_gate_months','stock_gate_months','shortage_and_stock_months')],width=.32,color=color,label=f'{s["quota"]} %')
        axes[0,1].bar_label(bars,padding=3)
    axes[0,1].set_xticks(range(3),labels);axes[0,1].set_ylabel('Monate von 600')
    axes[0,1].set_ylim(0,max(s['shortage_gate_months'] for s in stats)*1.16)
    axes[0,1].set_title('Zwei Kaufbedingungen treffen nie zusammen',loc='left');axes[0,1].legend(frameon=False)
    labels=['Geplantes\nZurückbehalten','Guthaben-\nzuwachs','Maschinen-\nkäufe','Lagerwert-\nänderung']
    for i,(s,color) in enumerate(zip(stats,colors)):
        axes[1,0].bar([v+(i-.5)*.32 for v in range(4)],[s['average_retention_cents']/100,s['average_saving_cents']/100,s['invested_cents']/60000,s['average_inventory_change_cents']/100],width=.32,color=color)
    axes[1,0].set_xticks(range(4),labels);axes[1,0].set_ylabel('Euro / Monat')
    axes[1,0].set_title('M481–600 · Haushaltssparen und Investitionen',loc='left')
    rows=old['runs'][0]['monthly']
    for k,label,color in [('household_cash_cents','Haushalte','#526f89'),('firm_cash_cents','Firmen','#66895a'),('government_cash_cents','Staatskasse','#b18158'),('government_debt_cents','Staatsschuld','#9a5961')]:
        axes[1,1].plot([r['month'] for r in rows],[r[k]/100000 for r in rows],label=label,color=color,linestyle='--' if k=='government_debt_cents' else '-')
    axes[1,1].set_title('95 % · Guthaben und Staatsschuld',loc='left')
    axes[1,1].set_ylabel('Tausend Euro');axes[1,1].set_xlabel('Monat');axes[1,1].legend(frameon=False,fontsize=8)
    for ax in axes.flat:ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
    svg=target.with_suffix('.svg');svg.write_text('\n'.join(l.rstrip() for l in svg.read_text().splitlines())+'\n')
    fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
    a,b=stats
    lines=['# Firmenreaktionen Sparen und Investitionen','',
        'Stand: 3. November 2026. Eigener simulierter Befund des bestehenden Modells v16. Alle Verhaltensregeln und Anfangswerte bleiben unverändert; nur die bereits archivierten Konsumquoten 95 und 100 % unterscheiden sich.','',
        'Die 95-%-Variante leidet langfristig überwiegend unter fehlender Nachfrage, nicht unter zu geringer Maschinenkapazität. Gleichzeitig verstärken getrennte Personal- und Arbeitszeitregeln sowie harte staatliche Defizitschwellen den Rückgang. Der Investitionspfad hat eine zusätzliche Beschränkung: Auch bei Engpässen wird nur aus dem nach den übrigen Käufen verbliebenen Werkstattlager investiert. In beiden Varianten kommt über 600 Monate kein Maschinenkauf zustande.','',
        f'![Firmenkapazität Investitionsbedingungen und Geldbestände]({target.name}.svg)','',
        '## Kapazität und tatsächliche Investitionen','',
        '| Kennzahl | 95 % | 100 % |','| --- | ---: | ---: |',
        f'| Private Vollzeitäquivalente im Mittel M481–600 | {a["average_private_fte"]:.4f} | {b["average_private_fte"]:.4f} |',
        f'| Monate mit unerfüllten Alltagsbestellungen | {a["shortage_months"]["alltag"]} | {b["shortage_months"]["alltag"]} |',
        f'| Monate mit unerfüllten Werkstattbestellungen | {a["shortage_months"]["werkstatt"]} | {b["shortage_months"]["werkstatt"]} |',
        f'| Maschinenkäufe insgesamt | {euro(a["invested_cents"])} | {euro(b["invested_cents"])} |',
        f'| Lagerwertänderung im Mittel M481–600 | {euro(a["average_inventory_change_cents"])} | {euro(b["average_inventory_change_cents"])} |','',
        'Vier private Vollzeitkräfte sind der Ausgangsbestand. Rund zwei Vollzeitäquivalente bei 95 % zeigen im langfristigen Mittel freie Arbeitszeit. Die Betriebe passen sich durch niedrigere Stunden an die geringeren Bestellungen an. Zusätzliche Maschinen wären damit kein belegter Ausgleich für das Sparen; bei gleichem Absatz könnten sie auch die benötigte Arbeit verringern. Dies ist ein möglicher Gegenmechanismus, kein ausgeführter Investitionsgegenlauf. Lagerwertänderungen sind reale Bestandsinvestitionen in der BIP-Näherung und werden deshalb getrennt von Maschinenkäufen ausgewiesen.','',
        '## Die bestehende Maschinenregel blockiert auch bei hoher Nachfrage','',
        'Nur Alltag & Versorgung kann autonom eine Maschine von Werkstatt & Technik kaufen. Der Kauf erfordert zwei vorherige aufeinanderfolgende Monate mit unerfüllten finanzierbaren Bestellungen, drei Monate Abstand zum letzten Kauf, Geld oberhalb des Betriebspuffers und acht ursprüngliche Werkstatteinheiten als freie Ware. Bei der aktuellen Stückelung sind das 800 Teile für anfangs 1.200 Euro. Der separate Bankkredit wird nur auf ausdrückliche Anfrage ausgelöst; die beiden Baselines enthalten keine Anfrage.','',
        '| Beobachtete Kaufbedingung | 95 % | 100 % |','| --- | ---: | ---: |',
        f'| Zwei vorherige Engpassmonate | {a["shortage_gate_months"]} | {b["shortage_gate_months"]} |',
        f'| Ausreichendes freies Werkstattlager | {a["stock_gate_months"]} | {b["stock_gate_months"]} |',
        f'| Beide Bedingungen gleichzeitig | {a["shortage_and_stock_months"]} | {b["shortage_and_stock_months"]} |',
        f'| Geld einschließlich Betriebspuffer vorhanden | {a["cash_gate_months"]} | {b["cash_gate_months"]} |','',
        'Bei 95 % ist die Engpassbedingung nur in M6–8 erfüllt; dort verbleiben 148, 0 und 274 Werkstattteile. Bei 100 % ist sie deutlich häufiger erfüllt, trifft aber ebenfalls nie auf mindestens 800 freie Teile. Haushalte, öffentliche Beschaffung und Exporte kaufen vor der Investitionsphase. Es gibt weder eine Maschinenvorbestellung noch eine dafür geplante Produktion; die Werkstatt kann ihrerseits nicht investieren. Die Beobachtung belegt eine Beschränkung des bestehenden Investitionskanals. Wie stark eine andere Bestellreihenfolge oder Auftragsproduktion den Gesamtverlauf verändern würde, ist hier nicht isoliert gemessen.','',
        'Der Kanal bildet ausschliesslich Kapazitätserweiterung nach Absatzengpässen ab. Anlagen verschleissen nicht; Ersatzinvestitionen, eigenständig bewertete Modernisierungsprojekte und ein öffentlicher Kapitalstock fehlen. Staatliche Warenkäufe gelten in der bestehenden BIP-Näherung als öffentliche Güternachfrage, nicht als Aufbau produktiver Anlagen. Damit enthält das Modell keinen gesonderten Investitionszyklus, der unabhängig von aktuellen Lieferengpässen Nachfrage erzeugt. Das ist eine Modellgrenze und kein Beleg dafür, dass jeder Konsumverzicht durch Investitionen ausgeglichen werden müsste.','',
        '## Haushalte sparen mehr als der Kaufplan zurückhält','',
        'Die Konsumquote bezieht sich auf Nettoeinkommen einschließlich im Folgemonat verfügbarer Ausschüttungen. Ein Mindestbedarf kann vorhandenes Guthaben beanspruchen. Nicht erhältliche Ware und Rundung lassen zusätzlich Geld auf den Konten. Ausschüttungen nach der Kaufphase verändern den Monatsbestand, werden aber erst im nächsten Kaufplan berücksichtigt.','',
        '| Monatlicher Betrag M481–600 | 95 % | 100 % |','| --- | ---: | ---: |']
    for label,key in [('Vom Kaufplan zurückbehalten','average_retention_cents'),('Wegen fehlender Ware nicht ausgegeben','average_stock_gap_cents'),('Rest durch Gütereinheiten','average_unit_remainder_cents'),('Unterschied aktueller und vorheriger Ausschüttungen','average_dividend_timing_cents'),('Tatsächlicher Haushaltsguthabenzuwachs','average_saving_cents')]:
        lines.append(f'| {label} | {euro(a[key])} | {euro(b[key])} |')
    lines += ['',
        'Diese Bestandsgleichung wird für jeden Monat centgenau geprüft. 100 % Konsumquote bedeutet deshalb keine garantierte Nullersparnis. Bereits angesammeltes Vermögen führt über den Mindestbedarf hinaus zu keinem zusätzlichen Konsumplan. Ebenso gibt es keine eigenständige Vermögensanlage der Haushalte, die ihre Guthaben in zusätzliche Investitionsausgaben überführt. Eine solche Ausgabe müsste begründet modelliert werden; angespartes Geld allein löst sie nicht aus.','',
        '## Wo die Gegenbuchung zum Guthabenzuwachs liegt','',
        '| Monatliche Bestandsänderung M481–600 | 95 % | 100 % |','| --- | ---: | ---: |']
    for sector,label in [('households','Haushaltsguthaben'),('firms','Firmenguthaben'),('government','Staatsguthaben'),('external','Auslandsguthaben'),('bank','Bankeigenkapital')]:
        lines.append(f'| {label} | {euro(a["average_sector_cash_changes"][sector])} | {euro(b["average_sector_cash_changes"][sector])} |')
    lines += [f'| Staatsschuld | {euro(a["average_debt_change_cents"])} | {euro(b["average_debt_change_cents"])} |','',
        'Im 95-%-Lauf wächst die Staatsschuld langfristig nahezu im Umfang des Haushaltsguthabenzuwachses; Firmen, Ausland und Staatskasse erklären die Differenz. Das ist ein beobachteter Finanzierungspfad, kein Naturgesetz zugunsten staatlicher Schulden oder Inflation. Die Konten verschwinden nicht aus der Bilanz. Ein dauerhafter privater Geldüberschuss benötigt in dieser Modellgrenze eine Gegenposition. Haushaltsguthabenzuwachs ist zudem nicht die volkswirtschaftliche Gesamtersparnis; der Vergleich mit Maschinenkäufen ist keine Prüfung der gesamtwirtschaftlichen Identität von Sparen und Investieren.','',
        '## Welche Firmenreaktion bisher nicht plausibel genug ist','',
        'Die [vorherige Personaldiagnose](firm-reactions-v16-diagnosis.md) zeigt 63 Entlassungen und 63 Wiedereinstellungen der Werkstatt bei 95 %, alle Entlassungen bei positivem Monatsgewinn. In M34 sinkt die gesamte geplante Arbeitszeit durch den Kopfzahlwechsel von 0,9266 auf 0,7133 Vollzeitäquivalente. Eine finanzierbare Zwei-Personen-Option mit je 51,28 % wäre verfügbar. Die Personalzahl nutzt eine andere Bedarfsgleichung als die Produktions- und Lagerplanung. Im Modell fehlen zugleich fixe Kosten je Beschäftigtem, die einen Kopfzahlabbau bei gleicher Gesamtarbeitszeit wirtschaftlich begründen könnten.','',
        'Die staatliche Dreimonatsschwelle vergrössert den Unterschied bereits vorher: In M9 stehen −34,17 Euro bei 95 % einem Überschuss von 21,70 Euro bei 100 % gegenüber. Nur die erste Variante löst eine zusätzliche Beschaffungskürzung von 600 Euro aus. Später fallen dort die öffentlichen Stellen weg. Niedrigere Einkommen und Steuern sowie höhere Transfers verstärken die Nachfragerückwirkung. Der feste Transfer von 1.000 Euro kann bei niedriger Teilzeit sogar über dem vorherigen Nettolohn liegen. Diese bereits belegten Regelwirkungen bleiben unverändert.','',
        '## Schlussfolgerung für die nächste Prüfung','',
        'Ein Rückgang von Bestellungen und Arbeitszeit ist nachvollziehbar. Die Grösse des Einbruchs und die wiederholten Kopfzahlwechsel sind durch die bestehenden Schwellen nicht hinreichend plausibilisiert. Fehlende Maschineninvestitionen sind bei 95 % langfristig kein nachgewiesener Kapazitätsmangel, bei 100 % aber ein sichtbarer Engpass des Investitionsablaufs. Beide Probleme müssen getrennt werden.','',
        'Zuerst sollte ein isolierter Gegenlauf gemeinsame Personal- und Arbeitszeitplanung prüfen, mit unveränderter Staats- und Investitionslogik. Danach lässt sich der Maschinenpfad gezielt auf Vorbestellung und Lieferfähigkeit prüfen. Zusätzliche Investitionsnachfrage, Inflation oder Wachstum als pauschaler Ausgleich würden die hier beobachteten Ursachen nicht einzeln prüfen. Kein solcher Eingriff wurde für diese Diagnose vorgenommen.','',
        '## Reproduktion','',
        f'[Beobachtete Kaufbedingungen und sektorale Buchungen]({Path(source).name}) · [ursprünglicher Konsumvergleich](consumption-v16-comparison.md) · [Prüfprotokoll]({target.name}-verification.json).','',
        '```sh',
        f'python poc/scripts/diagnose_saving_investment.py --output {source}',
        f'python poc/scripts/report_saving_investment.py --source {source} --output {output}',
        'python -m unittest discover -s poc -p test_saving_investment_diagnosis.py -v',
        '```','',
        'Beide 600-Monats-Verläufe reproduzieren die archivierten Monatskonten, Käufe, Beschäftigung, Staatsbudget, Staatsschuld, Steuern und Makrokomponenten exakt. Die Regeln bleiben v16. Eine zusätzliche Gleichheitsprüfung vergleicht Journal und ökonomische Geschichte einer unveränderten und einer beobachteten Welt über 45 Monate. Die Diagnose beschreibt diese Modellwelt und ist keine empirische Kalibrierung einer realen Volkswirtschaft.','']
    target.with_suffix('.md').write_text('\n'.join(lines))
    verification=dict(date='2026-11-03', model=data['model'], rules_changed=False,
        months_each=600,profiles=[95,100],reference_exact_monthly_match=True,
        sector_cash_reconciliations=1200,household_saving_decompositions=1200,
        investment_decisions_checked=1200,tests_passed=3,source_hashes_verified=True,
        test_command='python -m unittest discover -s poc -p test_saving_investment_diagnosis.py -v',
        original_reference_sha256=data['reference_sha256'],
        investment_trace_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        staffing_trace_sha256=hashlib.sha256(traces_path.read_bytes()).hexdigest(),
        statistics=stats,
        limitations=['No causal intervention isolates total outcome contributions',
            'Household cash saving differs from national saving',
            'Rule-based illustrative model; no empirical calibration'])
    target.with_name(target.name+'-verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',default='qa/saving-investment-v16-traces-2026-11-03.json')
    p.add_argument('--output',default='qa/saving-investment-v16-diagnosis')
    a=p.parse_args();report(a.source,a.output)
