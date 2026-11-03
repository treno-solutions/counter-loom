"""Render the fiscal-policy comparison; matplotlib is an optional reporting dependency."""
import argparse
import json
from itertools import accumulate
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def euro(c):
    return f'{c/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'


def report(source,output):
    data=json.loads(Path(source).read_text());assert len(data['runs'])==2
    if data['months']!=600:raise ValueError('This dated report requires a complete 600-month comparison.')
    old,new=data['runs'];a,b=old['monthly'][-1],new['monthly'][-1]
    def series(run,key):
        if key=='social_gap':return list(accumulate(r['public_budget']['social_unfunded_cents']/100 for r in run['monthly']))
        if key=='jobs':return [r['public_budget']['approved_staff'] for r in run['monthly']]
        if key=='procurement':return [r['public_budget']['procurement_paid_cents']/100 for r in run['monthly']]
        return [r[key]/100 for r in run['monthly']]
    panels=[('public_wage_arrears_cents','Offene öffentliche Löhne','Euro'),('social_gap','Ungedeckter Sozial-Referenzbedarf · kumuliert','Euro'),
            ('government_debt_cents','Bankschuld des Staates','Euro'),('jobs','Öffentliche Arbeitsverträge · nicht zwingend bezahlt','Verträge'),
            ('household_cash_cents','Haushaltsguthaben gesamt','Euro'),('consumption_cents','Tatsächliche Käufe je Monat','Euro'),
            ('government_cash_cents','Staatskasse','Euro'),('procurement','Tatsächlich bezahlte öffentliche Aufträge je Monat','Euro')]
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','svg.hashsalt':'counterloom-fiscal-v13'})
    fig,axes=plt.subplots(4,2,figsize=(15,14),layout='constrained')
    for ax,(key,title,unit) in zip(axes.flat,panels):
        for run,color,style,label in [(old,'#8063a6','--','Bisherige Staatsregel'),(new,'#012d3b','-','Anpassendes Staatsbudget')]:
            ax.plot([r['month'] for r in run['monthly']],series(run,key),color=color,linestyle=style,linewidth=1.2,label=label)
        ax.set_title(title,loc='left',color='#012d3b');ax.set_xlim(1,data['months']);ax.set_ylim(bottom=0)
        ax.grid(axis='y',color='#d9e2e6',linewidth=.7);ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:,.0f}'.replace(',','.')))
        ax.set_xlabel('Monat');ax.set_ylabel(unit)
        if key=='jobs':ax.set_yticks([0,1,2]);ax.set_ylim(0,2.2)
    fig.suptitle('Staatsbudget · gleiche Gewinnverwendung, 600 Monate, keine Schocks',fontsize=15,color='#012d3b')
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=2,frameon=False)
    target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
    svg=target.with_suffix('.svg');svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(target.with_suffix('.png'),dpi=120,metadata={'Software':'Counterloom / Matplotlib'});plt.close(fig)
    lines=['# Anpassendes Staatsbudget · 600-Monats-Vergleich','',
           'Stand: 3. November 2026. Simulierte Befunde aus einer kleinen illustrativen Modellwirtschaft, keine empirische Kalibrierung oder wirtschaftspolitische Empfehlung. Beide Varianten verwenden dieselben Anfangsbilanzen und dieselbe Gewinnverwendung mit zusätzlichen Quartalsausschüttungen. Steuersätze, Steuerbasis, Kreditrahmen, private Unternehmensregeln und Preise werden nicht zur Verbesserung des Ergebnisses geändert. Es gibt keine äusseren Schocks.','',
           f'![Offene Löhne, Sozialbedarfslücken, Bankschuld, öffentliche Arbeitsverträge, Haushaltsguthaben, Konsum, Staatskasse und Beschaffung]({target.with_suffix(".svg").name})','',
           '## Hauptbefund','',
           '**Die Regel verhindert neue unbezahlte öffentliche Löhne, saniert aber die Modellwirtschaft nicht.** Der Staat reagiert auf Defizite mit geringerer Beschaffung und schliesslich ohne öffentliche Arbeitsverträge. Dadurch entstehen weniger Lohnversprechen. Gleichzeitig steigen ungedeckte Sozialbedarfe; die Kreditgrenze wird später dennoch erreicht. Das ist keine kostenlose Beseitigung eines Defizits.','',
           '## Vergleich am Monatsende 600','',
           '| Kennzahl | Bisherige Staatsregel | Anpassendes Budget |','| --- | ---: | ---: |']
    for key,title in [('public_wage_arrears_cents','Offene öffentliche Lohnansprüche'),('government_interest_arrears_cents','Offene Staatszinsen'),('government_debt_cents','Bankschuld des Staates'),('government_cash_cents','Staatskasse'),('household_cash_cents','Haushaltsguthaben gesamt'),('consumption_cents','Tatsächliche Käufe · Monat 600')]:lines.append(f'| {title} | {euro(a[key])} | {euro(b[key])} |')
    for key,title in [('approved_staff','Öffentliche Arbeitsverträge'),('wages_paid_cents','Aktuelle öffentliche Löhne bezahlt · Monat 600'),('social_need_cents','Sozial-Referenzbedarf · Monat 600'),('social_paid_cents','Sozialleistungen tatsächlich bezahlt · Monat 600'),('social_unfunded_cents','Sozial-Referenzbedarf ungedeckt · Monat 600')]:
        va,vb=a['public_budget'][key],b['public_budget'][key]
        lines.append(f'| {title} | {va if key=="approved_staff" else euro(va)} | {vb if key=="approved_staff" else euro(vb)} |')
    lines += [f'| Kumulierte ungedeckte Sozialbedarfe · keine gebuchte Schuld | {euro(old["cumulative_social_gap_cents"])} | {euro(new["cumulative_social_gap_cents"])} |',
              f'| Kreditgrenze erstmals erreicht | M{old["first_thresholds"].get("credit_limit_reached","–")} | M{new["first_thresholds"].get("credit_limit_reached","–")} |','',
              'Der Bedarfssaldo bleibt in der neuen Variante negativ, wenn der Staat seine laufenden Sozial-Referenzbeträge nicht finanzieren kann. Ausgebliebene Zahlungen machen die Planung nicht künstlich tragfähig. Die alte reine Zahlungsrechnung konnte ein kleines Plus zeigen, während Lohnansprüche weiter anwuchsen.','',
              'Die Soziallücke ist bewusst keine zusätzliche Schuldposition: Der Arbeitslosentransfer ist im Modell ein Referenzbedarf, fehlende Kurzarbeitsleistung bleibt dagegen ein Anspruch. Der Arbeitsstatus und damit die Zahl der transferberechtigten Haushalte unterscheiden sich zwischen den Varianten. Kumulierte Soziallücken und offene Lohnforderungen sind deshalb nicht dieselbe Grösse und dürfen nicht als identische Wohlfahrts- oder Schuldenmasse behandelt werden.','',
              '## Wann der Staat reagiert','', '| Abschluss | Entscheidung | Ab Monat | Stellenziel | Beschaffungsquote |','| --- | --- | ---: | ---: | ---: |']
    names={'cut_procurement':'Beschaffung reduzieren','cut_staff':'Öffentliche Stelle abbauen','restore_staff':'Öffentliche Stelle wieder finanzieren','restore_procurement':'Beschaffung erhöhen','funding_cut':'Unmittelbare Finanzierungsgrenze'}
    for row in new['monthly']:
        m=row['public_budget']
        if m['decision']!='hold':lines.append(f'| M{row["month"]} | {names[m["decision"]]} | {m["decision_effective_month"]} | {m["next_target_staff"]} | {m["next_procurement_bps"]/100:g} % |')
    lines+=['', '## Gesamter Verlauf statt nur Endmonat', '', '| Tatsächlich bezahlter Fluss über 600 Monate | Bisherige Staatsregel | Anpassendes Budget |', '| --- | ---: | ---: |']
    totals=[('Haushaltskäufe',sum(r['consumption_cents'] for r in old['monthly']),sum(r['consumption_cents'] for r in new['monthly'])),
            ('Aktuelle öffentliche Löhne',sum(r['public_budget']['wages_paid_cents'] for r in old['monthly']),sum(r['public_budget']['wages_paid_cents'] for r in new['monthly'])),
            ('Sozialleistungen',sum(r['public_budget']['social_paid_cents'] for r in old['monthly']),sum(r['public_budget']['social_paid_cents'] for r in new['monthly'])),
            ('Öffentliche Warenaufträge',old['cumulative_procurement_paid_cents'],new['cumulative_procurement_paid_cents'])]
    for title,va,vb in totals:lines.append(f'| {title} | {euro(va)} | {euro(vb)} |')
    change=(totals[0][2]/totals[0][1]-1)*100
    lines+=['', f'Über den gesamten Lauf liegen die tatsächlichen Haushaltskäufe in der neuen Variante um {change:.1f} % höher, obwohl der einzelne Monat 600 niedrigere Käufe zeigt. Die frühere Begrenzung öffentlicher Ausgaben verschiebt verfügbare Mittel zu Sozialzahlungen und verändert die Nachfrageverläufe. Das ist eine Veränderung der Geldverwendung und des Umsatzes, keine zusätzliche Geldschöpfung.', '', 'Diese kumulierten Werte sind Zahlungsflüsse: Dasselbe Geld kann mehrfach ausgegeben werden. Haushaltskäufe sind zudem weder die gesamte Güternachfrage noch ein Wohlfahrtsmass; öffentliche Warenaufträge und der bisher nicht modellierte Nutzen öffentlicher Arbeit fehlen darin.', '', 'Die vorab festgelegte Regel kürzt nach drei Defizitabschlüssen zuerst die Beschaffungsquote um 25 Prozentpunkte. Bei bereits ausgesetzter Beschaffung kann nach drei weiteren Defizitabschlüssen eine öffentliche Stelle entfallen. Tatsächliche Monatsarbeit benötigt unabhängig davon vorab bestätigte Finanzierung. Wiederaufbau braucht drei positive Abschlüsse, wiederkehrende Deckung, Liquidität und gegebenenfalls freie Arbeitskräfte; er wird nicht erzwungen.','',
            'Im geprüften neuen Lauf entfallen die öffentlichen Stellen bereits vor einer vollständigen Erschöpfung der Staatskasse. Der Staat versucht also frühzeitig, strukturelle Defizite zu begrenzen. Die dadurch veränderten Einkommen und Aufträge schwächen aber auch Nachfrage und Steuereinnahmen. Reine Ausgabenkürzung löst die unzureichende Deckung hier nicht dauerhaft.','',
            '## Haushalte einzeln','', '| Haushalt | Guthaben bisher | Guthaben neu | Arbeitgeber neu | Sozialzahlung neu · M600 |','| --- | ---: | ---: | --- | ---: |']
    employers={'alltag':'Alltag & Versorgung','werkstatt':'Werkstatt & Technik','staat':'Staat',None:'ohne Arbeitsvertrag'}
    for h0,h1 in zip(a['households'],b['households']):lines.append(f'| {h0["id"]} | {euro(h0["cash_cents"])} | {euro(h1["cash_cents"])} | {employers[h1["employer"]]} | {euro(h1["transfers_cents"])} |')
    lines+=['', 'Ein annähernd gleiches Haushaltsguthaben insgesamt bedeutet keine ähnliche Lage aller Haushalte. Die neue anteilige Verteilung erreicht mehrere Haushalte, während die bisherige Reihenfolge bei knappen Mitteln einzelne zuerst bediente. Arbeitsplätze, laufende Einkommen und Guthaben bleiben jedoch stark ungleich verteilt. Gleiche Unternehmensanteile und die einfache Transferberechtigung ohne Vermögensprüfung sind weiterhin Modellannahmen.','',
            '## Was umgesetzt und geprüft wurde','',
            '- Defizitbestätigung und verzögerte Änderungen an Monatsgrenzen.','- Vollständig bestätigte Lohnfinanzierung vor aktueller öffentlicher Arbeit; kein neuer Lohnrückstand in jedem der 600 neuen Abschlüsse.','- Beendete Verträge statt verdeckter unbezahlter Arbeit. Neue private Beschäftigung entsteht nur aus den vorhandenen Firmenentscheidungen.','- Anteilige Sozialzahlungen und explizite ungedeckte Referenzbeträge.','- Alte Lohnansprüche bleiben bestehen und werden nur durch echte Überweisungen, einschliesslich Modellsteuer, reduziert.','- Der Referenzzweig stimmt in jedem Monat bei Haushalts-, Firmen-, Staats- und Auslandskonten, Bankschuld, Konsum, Produktion, Vertragszahl und offenen öffentlichen Löhnen exakt mit dem archivierten v12-Lauf überein.','',
            '## Grenzen und nächster Untersuchungsschritt','',
            'Die neue Regel ist ein nachvollziehbares Ausgaben- und Finanzierungsverhalten. Das Ende neuer Lohnrückstände ist als Software- und Buchungsziel erreicht, nicht als Nachweis einer gesunden Volkswirtschaft. Entfallene öffentliche Arbeit wird noch nicht in Dienstleistungen oder gesellschaftlichem Nutzen bewertet. Ein Rückgang öffentlicher Stellen darf daher nicht als Produktivitätsgewinn gelesen werden.','',
            'Für eine tragfähigere Staatsfinanzierung muss als nächster getrennter Gegenlauf die Einnahmen- beziehungsweise Verteilungsseite geprüft werden. Die derzeitige Steuerbasis erfasst Löhne und Firmengewinne, lässt Ausschüttungen steuerfrei und reagiert nur indirekt auf die Vermögenskonzentration. Eine breitere Steuerbasis wäre eine zusätzliche, ausdrücklich zu dokumentierende Modellannahme. Die bestehenden Regeln dürfen nicht einfach so nachjustiert werden, dass ein gewünschtes Gleichgewicht entsteht.','',
            '## Daten und Reproduktion','',
            f'[Alle Monatswerte, Haushaltseinzelwerte, Budgetentscheidungen und Quellprüfsummen]({Path(source).name}). [Regeldefinition](../poc/PUBLIC_BUDGET_MODEL.md).','',
            'Vom Repository-Stamm mit eingerichteter Python-Umgebung:','', '```sh',
            'poc/.venv/bin/python poc/scripts/compare_public_budget.py --months 600', '```','',
            'Die Standardausgabe wird in `.framework-review/public-budget-comparison.json` geschrieben; der veröffentlichte datierte Befund wird nicht überschrieben. Der Batchlauf überspringt nur die Erstellung interaktiver Antworten, nicht Rechenschritte oder Kontrollen.','',
            'Abbildung erneut erzeugen, mit einer separaten Python-Umgebung mit Matplotlib:','', '```sh',
            f'python poc/scripts/report_public_budget.py --source {source} --output .framework-review/fiscal-v13-comparison', '```','']
    target.with_suffix('.md').write_text('\n'.join(lines))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',default='.framework-review/public-budget-comparison.json');parser.add_argument('--output',default='.framework-review/fiscal-v13-comparison')
    args=parser.parse_args();report(args.source,args.output)
