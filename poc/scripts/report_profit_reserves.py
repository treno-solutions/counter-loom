"""Render the controlled comparison using matplotlib (optional reporting dependency)."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def euro(cents):
    return f'{cents/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'


def report(source, output):
    data=json.loads(Path(source).read_text())
    assert len(data['runs'])==2
    old,new=data['runs'];a,b=old['monthly'][-1],new['monthly'][-1]
    metrics=[('household_cash_cents','Haushalte · Kontoguthaben'),('firm_cash_cents','Unternehmen · Kontoguthaben'),
             ('consumption_cents','Tatsächliche Käufe · Euro pro Monat'),('government_cash_cents','Staat · Kassenbestand'),
             ('government_debt_cents','Staat · Bankschuld'),('public_wage_arrears_cents','Unbezahlte öffentliche Löhne · kumuliert')]
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','svg.hashsalt':'counterloom-profit-v12'})
    fig,axes=plt.subplots(3,2,figsize=(15,11),layout='constrained')
    for ax,(key,title) in zip(axes.flat,metrics):
        for run,color,style,label in [(old,'#8063a6','--','Bisherige Regel'),(new,'#012d3b','-','Zusätzliche Quartalsausschüttung')]:
            ax.plot([r['month'] for r in run['monthly']],[r[key]/100 for r in run['monthly']],color=color,linestyle=style,linewidth=1.2,label=label)
        ax.set_title(title,loc='left',fontweight='normal',color='#012d3b')
        ax.set_xlim(1,data['months']);ax.set_ylim(bottom=0)
        ax.grid(axis='y',color='#d9e2e6',linewidth=.7);ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:,.0f}'.replace(',','.')))
        ax.set_xlabel('Monat');ax.set_ylabel('Euro')
    fig.suptitle('Gewinnverwendung · identische Anfangswerte, 600 Monate, keine Schocks',fontsize=15,color='#012d3b')
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=2,fontsize=10,frameon=False)
    target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
    svg=target.with_suffix('.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(target.with_suffix('.png'),dpi=130,metadata={'Software':'Counterloom / Matplotlib'})
    plt.close(fig)
    lines=['# Gewinnrücklagen und zusätzliche Ausschüttungen · 600-Monats-Vergleich','',
           'Stand: 3. November 2026. Simulierte Befunde, keine empirische Kalibrierung oder Prognose. Zwei Läufe beginnen mit denselben elf Akteuren und Anfangsbilanzen. Es gibt keine äusseren Schocks. Nur das Regelpaket der Gewinnverwendung unterscheidet sich; Staats-, Steuer-, Preis-, Personal- und Kreditregeln bleiben gleich. Endogene Reaktionen dürfen sich unterscheiden.','',
           f'![Verlauf von Haushalts- und Firmenkonten, Konsum, Staatskasse, Bankschuld und öffentlichen Lohnrückständen]({target.with_suffix(".svg").name})','',
           '## Ergebnis nach 600 Monaten','',
           '| Kennzahl | Bisherige Regel | Neue Gewinnverwendung |','| --- | ---: | ---: |']
    for key,label in [('household_cash_cents','Haushaltsguthaben gesamt'),('firm_cash_cents','Firmenguthaben gesamt'),('consumption_cents','Tatsächliche Käufe im Monat 600'),('government_cash_cents','Staatskasse'),('government_debt_cents','Bankschuld des Staates'),('public_wage_arrears_cents','Unbezahlte öffentliche Löhne'),('government_interest_arrears_cents','Unbezahlte Staatszinsen')]:
        lines.append(f'| {label} | {euro(a[key])} | {euro(b[key])} |')
    lines+=['', 'Der zusätzliche Rückfluss begrenzt im geprüften Lauf die Ansammlung von Geld bei den Unternehmen deutlich. Die Firmen halten am Ende zusammen ungefähr ihren Anfangsbestand von 48.000 €; positive, nicht benötigte Gewinne fliessen regelmässig an ihre Eigentümer. Die neue Regel verteilt das Anfangskapital nicht automatisch aus.','',
            '**Die Staatsfinanzierung ist damit nicht gelöst.** Eine positive Restkasse ist kein Beleg für Zahlungsfähigkeit: Die neue Variante weist weiterhin unbezahlte öffentliche Löhne in Millionenhöhe aus. Die bestehende Staatsregel reduziert ihre Lohnversprechen bei fehlender Finanzierung nicht und zahlt ältere Lohnrückstände nicht automatisch nach. Der tatsächliche Haushaltssaldo erfasst bezahlte Ausgaben; ausbleibende Zahlungen können ihn scheinbar verbessern. Bankschuld, Kasse und offene Verpflichtungen müssen gemeinsam gelesen werden.','',
            '## Haushalte einzeln','', '| Haushalt | Guthaben bisher · M600 | Guthaben neu · M600 | Arbeitgeber neu · M600 |','| --- | ---: | ---: | --- |']
    names={'alltag':'Alltag & Versorgung','werkstatt':'Werkstatt & Technik','staat':'Staat',None:'ohne Arbeitsvertrag'}
    for h0,h1 in zip(a['households'],b['households']):
        lines.append(f'| {h0["id"]} | {euro(h0["cash_cents"])} | {euro(h1["cash_cents"])} | {names[h1["employer"]]} |')
    richest=sum(sorted(h['cash_cents'] for h in b['households'])[-2:])/b['household_cash_cents']*100
    poor=sum(h['cash_cents']<50000 for h in b['households'])
    lines+=['', f'Im neuen Lauf halten die zwei liquidesten Haushalte zusammen {richest:.1f} % des Haushaltsguthabens; {poor} Haushalte verbleiben unter 500 €. Der höhere Sektorsaldo bedeutet deshalb keine flächendeckende Absicherung.', '', 'Die Sektorsumme ersetzt keine Aussage über jeden Haushalt. Die sechs Modellhaushalte besitzen gleiche Unternehmensanteile, haben aber unterschiedliche Lohn- und Beschäftigungsverläufe. Ein Arbeitsvertrag beim Staat bedeutet bei ausgebliebener Finanzierung keine vollständige Lohnzahlung. Diese Eigentumsannahme ist keine repräsentative Vermögensverteilung.','',
            '## Kontrollierter Unterschied','',
            '- Referenz: maximal die Hälfte des positiven Monatsergebnisses wird bei bestehender Freigabe und oberhalb des bisherigen Betriebspuffers ausgeschüttet; keine zusätzliche Ausschüttung.','- Neue Regel: kumulierte Ergebnisse und Verluste begrenzen auch die reguläre Ausschüttung. Alle drei Monate wird der verbleibende positive Gewinnvortrag zusätzlich ausgezahlt, soweit tatsächliche Liquidität oberhalb von Betriebspuffer und gebundenen Maschinenmitteln vorhanden ist. Schliessungen, Rückstände und ein nicht regulär tragfähiger Folgeplan sperren die Zahlung.','- Ausschüttungen bleiben steuerfrei. Keine neue Dividendensteuer, staatliche Budgetregel oder zusätzliche Kreditmöglichkeit wurde zur Verbesserung des Ergebnisses eingeführt.','',
            f'Der Referenzzweig wurde in jedem der {data["months"]} Monate gegen den archivierten v11-Basislauf geprüft: Haushalts-, Firmen-, Staats- und Auslandskonten, Staatsschuld, tatsächliche Käufe, Produktion und Vertragszahl stimmen exakt überein. Die neue Buchführung allein verändert den Referenzpfad damit nicht.','',
            f'Über den gesamten neuen Lauf wurden {euro(new["cumulative_extra_cents"])} zusätzlich und {euro(new["cumulative_regular_cents"])} regulär ausgeschüttet. Das sind kumulierte Zahlungsflüsse; dasselbe Geld kann wiederholt für Käufe und Ausschüttungen verwendet werden. Die Summe ist keine neu geschaffene Geldmenge.','',
            '## Einordnung','',
            'Die Änderung behebt einen konkreten fehlenden Rückfluss im vorhandenen Regelwerk. Sie validiert weder das gesamte Wirtschaftsmodell noch eine reale Ausschüttungspolitik. Firmenreserven bleiben abhängig vom einfachen Folgeplan; allgemeine Investitionsplanung, Abschreibung, Insolvenz und rechtliche Ausschüttungsgrenzen fehlen weiterhin. Stillgelegte Betriebe liquidieren ihr Anfangskapital oder ihre Rücklagen nicht automatisch.','',
            'Der nächste getrennte Untersuchungsschritt ist eine staatliche Budget- und Rückstandsregel: bezahlte Ausgaben von laufenden Verpflichtungen trennen und auf dauerhaft fehlende Finanzierung reagieren. Die Parameter dürfen nicht lediglich so verändert werden, dass ein gewünschtes Gleichgewicht entsteht.','',
            '## Daten und Reproduktion','',
            f'[Vollständige Monatswerte, einzelne Haushalte, Firmenentscheidungen und Quellprüfsummen]({Path(source).name}). [Regeldefinition](../poc/PROFIT_POLICY.md).','',
            'Vom Repository-Stamm mit eingerichteter Python-Umgebung:','', '```sh',
            'poc/.venv/bin/python poc/scripts/compare_profit_reserves.py --months 600',
            '```','',
            'Die Standardausgabe liegt in `.framework-review/profit-reserves-comparison.json` und überschreibt den datierten Befund nicht. Der Batchlauf überspringt nur die Erstellung interaktiver Antworten; Rechenschritte und Kontrollen bleiben erhalten. Ein Gleichheitstest vergleicht Batch- und interaktive Zustände samt Journal.','',
            'Die Abbildung lässt sich mit einer separaten Python-Umgebung mit Matplotlib erneut erzeugen:', '', '```sh',
            f'python poc/scripts/report_profit_reserves.py --source {source} --output .framework-review/profit-v12-comparison', '```','']
    target.with_suffix('.md').write_text('\n'.join(lines))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',default='.framework-review/profit-reserves-comparison.json')
    parser.add_argument('--output',default='.framework-review/profit-v12-comparison')
    args=parser.parse_args();report(args.source,args.output)
