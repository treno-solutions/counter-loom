"""Reproducible distribution-tax comparison figure and report (optional Matplotlib)."""
import argparse,json
from pathlib import Path
from itertools import accumulate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def euro(c):return f'{c/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def report(source,output):
 data=json.loads(Path(source).read_text());assert data['months']==600
 old,new=data['runs'];a,b=old['monthly'][-1],new['monthly'][-1]
 target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
 plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-tax-v14'})
 fig,axes=plt.subplots(4,2,figsize=(12,13));fig.subplots_adjust(top=.91,bottom=.08,hspace=.44,wspace=.25)
 fig.suptitle('Counterloom · Ausschüttungssteuer im 600-Monats-Vergleich',fontsize=15)
 fig.text(.5,.94,'Nur der Einbehalt unterscheidet sich: 0 % gegenüber 25 %. Gleiche anpassende Budgetregel; keine Schocks.',ha='center',fontsize=9)
 panels=[('government_debt_cents','Staatsschuld · Bestand'),('government_cash_cents','Staatskasse · Bestand'),('household_cash_cents','Haushaltsguthaben · zusammen'),('firm_cash_cents','Firmenguthaben · zusammen'),('purchases','Haushaltskäufe · kumulierter Zahlungsfluss'),('taxes','Alle Steuern · kumulierter Zahlungsfluss'),('social','Ungedeckter Sozial-Referenzbedarf · kumuliert'),('jobs','Genehmigte öffentliche Stellen')]
 for ax,(key,title) in zip(axes.flat,panels):
  for run,color,label in [(old,'#526f89','Ohne Ausschüttungssteuer'),(new,'#66895a','Mit 25 % Ausschüttungssteuer')]:
   rows=run['monthly']
   if key in ('purchases','taxes','social'):
    vals=list(accumulate((r['consumption_cents'] if key=='purchases' else r['taxes_cents'] if key=='taxes' else r['public_budget']['social_unfunded_cents'])/100 for r in rows))
   elif key=='jobs':vals=[r['public_budget']['approved_staff'] for r in rows]
   else:vals=[r[key]/100 for r in rows]
   ax.plot([r['month'] for r in rows],vals,color=color,label=label,lw=1.5)
  ax.set_title(title,loc='left',fontsize=10);ax.set_xlabel('Monat');ax.set_xlim(1,600);ax.grid(alpha=.2)
  if key=='jobs':ax.set_yticks([0,1,2]);ax.set_ylabel('Stellen')
  else:ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f'{x/1000:g}'));ax.set_ylabel('Tsd. Euro')
 handles,labels=axes.flat[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2,frameon=False)
 fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
 p=target.with_suffix('.svg');p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')
 fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
 def total(run,key):return sum(r[key] for r in run['monthly'])
 gap=lambda run:sum(r['public_budget']['social_unfunded_cents'] for r in run['monthly'])
 tax=sum(r['distribution']['tax_cents'] for r in new['monthly'])
 change=(total(new,'consumption_cents')/total(old,'consumption_cents')-1)*100
 lines=['# Ausschüttungssteuer · kontrollierter 600-Monats-Vergleich','', 'Stand: 3. November 2026 · Modell v14. Eigene illustrative Simulation, keine Prognose, empirische Kalibrierung oder Bewertung einer realen Steuerpolitik.','',
 f'Der zusätzliche Einbehalt bringt über 600 Monate {euro(tax)} tatsächlich gezahlte Ausschüttungssteuer. Die Staatskreditgrenze wird statt in Monat {old["first_thresholds"]["credit_limit_reached"]} in Monat {new["first_thresholds"]["credit_limit_reached"]} erreicht. Die bezahlten Haushaltskäufe liegen über den gesamten Lauf um {str(round(change,1)).replace('.',',')} % höher. Die Finanzierungsgrenze verschwindet nicht.','',
 '## Versuchsaufbau','', 'Beide Läufe verwenden dieselben Anfangsbestände, Firmenregeln, quartalsweisen Zusatzausschüttungen, anpassenden öffentlichen Ausgaben und Kreditgrenzen. Nur die Ausschüttungssteuer unterscheidet sich: 0 gegenüber 25 %. Lohnsteuer (30 %) und Gewinnsteuer (20 %) bleiben unverändert. Es gibt keine externen Schocks, Zufallsziehungen oder LLM-Aufrufe.','',
 'Bruttoausschüttungen vermindern den Gewinnvortrag der Firma. Der Einbehalt ist eine Steuer der Eigentümerhaushalte und kein weiterer Firmenaufwand. Erfasst werden reguläre und zusätzliche Firmenausschüttungen sowie tatsächliche Zinsausschüttungen der Bank. Jeder Haushalt versteuert seine über den Monat kumulierten Bruttobeträge; Cent-Rundung erfolgt auf dieser Summe. Nur Nettozahlungen gehen in die nächste Kaufrunde ein.','',
 'Der Nullsteuerzweig stimmt in jedem der 600 Monate bei Haushalts-, Firmen-, Staats- und Auslandsguthaben, Staatsschuld, Konsum, Produktion, Beschäftigung und offenen öffentlichen Löhnen exakt mit dem archivierten anpassenden v13-Lauf überein. Dieser historische Befund bleibt unverändert.','',
 f'![Verläufe beider Varianten]({target.name}.svg)','', '## Grenzen und Endbestände','', '| Grösse | Ohne Einbehalt | Mit 25 % Einbehalt |','| --- | ---: | ---: |']
 for title,key in [('Haushaltsguthaben · M600','household_cash_cents'),('Firmenguthaben · M600','firm_cash_cents'),('Staatskasse · M600','government_cash_cents'),('Staatsschuld · M600','government_debt_cents'),('Haushaltskäufe · nur M600','consumption_cents'),('Offene öffentliche Löhne · M600','public_wage_arrears_cents')]:lines.append(f'| {title} | {euro(a[key])} | {euro(b[key])} |')
 for title,key in [('Staatskreditgrenze erreicht','credit_limit_reached'),('Erster ungedeckter Sozialbedarf','social_funding_gap'),('Erste Reduktion öffentlicher Stellen','public_job_reduction')]:lines.append(f'| {title} | M{old["first_thresholds"][key]} | M{new["first_thresholds"][key]} |')
 lines+=['','## Zahlungsflüsse über alle 600 Monate','', '| Grösse | Ohne Einbehalt | Mit 25 % Einbehalt |','| --- | ---: | ---: |']
 for title,va,vb in [('Alle Steuereingänge',total(old,'taxes_cents'),total(new,'taxes_cents')),('Davon Ausschüttungssteuer',0,tax),('Bezahlte Haushaltskäufe',total(old,'consumption_cents'),total(new,'consumption_cents')),('Ungedeckter Sozial-Referenzbedarf',gap(old),gap(new)),('Tatsächlich ausgezahlte Sozialleistungen',sum(r['public_budget']['social_paid_cents'] for r in old['monthly']),sum(r['public_budget']['social_paid_cents'] for r in new['monthly']))]:lines.append(f'| {title} | {euro(va)} | {euro(vb)} |')
 lines+=['', 'Geld kann mehrfach als Kauf und Steuerzahlung umlaufen. Kumulierte Steuer- oder Konsumflüsse sind deshalb keine zusätzlichen Geldbestände. Die Differenz aller Steuereinnahmen ist grösser als die neue Ausschüttungssteuer allein: veränderte Käufe beeinflussen Umsätze, Gewinne und damit weitere Steuerzahlungen.','',
 '## Interpretation','',
 'Die breitere Steuerbasis verschiebt Geld von Eigentümerhaushalten in die Staatskasse. Im Modell kann der Staat dadurch länger Zahlungen leisten. Das verändert Nachfrage, Firmenentscheidungen und spätere Ausschüttungen. Ein niedrigeres verfügbares Ausschüttungseinkommen bedeutet hier daher nicht automatisch niedrigere Käufe über den gesamten Lauf.','',
 'Beide Varianten genehmigen insgesamt 33 öffentliche Stellenmonate; die zusätzliche Steuer verhindert in diesem Parametersatz den Abbau öffentlicher Stellen nicht. Beide erreichen den Kreditdeckel von 50.000 €. Der ungedeckte Sozialbedarf bleibt erheblich. Die Steuer verbessert die Liquiditätsverwendung unter diesen Regeln, liefert aber keinen Nachweis einer langfristig tragfähigen Modellwirtschaft.','',
 'Die sechs Haushalte besitzen gleiche Unternehmensanteile, haben jedoch unterschiedliche Beschäftigungsverläufe. Die Vermögensverteilung bleibt ungleich; ein ähnlicher Gesamtbestand allein beschreibt weder individuelle Lebenslagen noch Wohlfahrt. Öffentliche Dienstleistungen, Vermögensprüfungen, Freibeträge, Steuervermeidung, Insolvenz und ein Anleihemarkt sind nicht ergänzt worden.','',
 '## Haushalte einzeln · M600','', '| Haushalt | Guthaben ohne Steuer | Guthaben mit Steuer | Arbeitgeber mit Steuer |','| --- | ---: | ---: | --- |']
 for h0,h1 in zip(a['households'],b['households']):lines.append(f'| {h0["id"]} | {euro(h0["cash_cents"])} | {euro(h1["cash_cents"])} | {h1["employer"] or "ohne Arbeitsvertrag"} |')
 lines+=['', '## Nachvollziehbarkeit und Reproduktion','',f'[Monatsdaten, Steuerarten und Quellprüfsummen]({Path(source).name}) · [Modellregeln](../poc/DISTRIBUTION_TAX_MODEL.md) · [Historischer v13-Vergleich](fiscal-v13-comparison.md).','',
 'Vom Repository-Stamm mit der eingerichteten Python-Umgebung:','', '```sh','poc/.venv/bin/python poc/scripts/compare_distribution_tax.py --months 600','python poc/scripts/report_distribution_tax.py --source .framework-review/distribution-tax-comparison.json --output .framework-review/tax-v14-comparison','```','', 'Matplotlib wird nur für die Abbildung benötigt. Die datierten archivierten Befunde werden von diesen Standardbefehlen nicht überschrieben.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',default='.framework-review/distribution-tax-comparison.json');p.add_argument('--output',default='.framework-review/tax-v14-comparison');args=p.parse_args();report(args.source,args.output)
