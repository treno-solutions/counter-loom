"""Report the controlled goods-resolution experiment; optional Matplotlib dependency."""
import argparse,json
from itertools import accumulate
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def euro(c):return f'{c/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def mean(rows,fn):return sum(fn(r) for r in rows)/len(rows)
def rolling(values):return [sum(values[max(0,i-11):i+1])/min(i+1,12) for i in range(len(values))]
def report(source,output):
 data=json.loads(Path(source).read_text());assert data['months']==600 and [r['goods_unit_scale'] for r in data['runs']]==[1,100]
 old,new=data['runs'];a,b=old['monthly'][-1],new['monthly'][-1];target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
 plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-goods-granularity'})
 fig,axes=plt.subplots(4,2,figsize=(12,13));fig.subplots_adjust(top=.91,bottom=.08,hspace=.44,wspace=.25)
 fig.suptitle('Counterloom · Kleinere Gütereinheiten über 600 Monate',fontsize=15)
 fig.text(.5,.94,'100 Teile je bisheriger Einheit. Gleiche reale Anfangskapazitäten und Preise; gleiche Steuer- und Verhaltensregeln.',ha='center',fontsize=9)
 panels=[('rounding','Nicht ausgegeben durch Stückelung · Monatsmittel'),('purchases','Haushaltskäufe · kumulierter Zahlungsfluss'),('government_debt_cents','Staatsschuld · Bestand'),('government_cash_cents','Staatskasse · Bestand'),('employment','Arbeitsverträge · Monatsende'),('social','Ungedeckter Sozialbedarf · kumuliert'),('household_cash_cents','Haushaltsguthaben · zusammen'),('balance','Steuern minus voller Ausgabenbedarf · Monatsmittel')]
 for ax,(key,title) in zip(axes.flat,panels):
  for run,color,label in [(old,'#526f89','Bisherige Einheiten (100 / 150 €)'),(new,'#66895a','Hundertstel (1 / 1,50 €)')]:
   rows=run['monthly']
   if key=='rounding':vals=rolling([r['purchase_totals']['unit_remainder_cents']/100 for r in rows])
   elif key=='balance':vals=rolling([r['public_budget']['commitment_balance_cents']/100 for r in rows])
   elif key=='purchases':vals=list(accumulate(r['consumption_cents']/100 for r in rows))
   elif key=='social':vals=list(accumulate(r['public_budget']['social_unfunded_cents']/100 for r in rows))
   elif key=='employment':vals=[r[key] for r in rows]
   else:vals=[r[key]/100 for r in rows]
   ax.plot([r['month'] for r in rows],vals,color=color,label=label,lw=1.5)
  ax.set_title(title,loc='left',fontsize=10);ax.set_xlabel('Monat');ax.set_xlim(1,600);ax.grid(alpha=.2)
  if key=='employment':ax.set_ylabel('Verträge');ax.set_ylim(0,6.5);ax.set_yticks([0,2,4,6])
  elif key in ('rounding','balance'):ax.set_ylabel('Euro / Monat');ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:g}'))
  else:ax.set_ylabel('Tsd. Euro');ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v/1000:g}'))
  if key=='balance':ax.axhline(0,color='#888',lw=.7)
 fig.legend(*axes.flat[0].get_legend_handles_labels(),loc='lower center',ncol=2,frameon=False)
 fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'})
 svg=target.with_suffix('.svg');svg.write_text('\n'.join(l.rstrip() for l in svg.read_text().splitlines())+'\n')
 fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
 def total(run,fn):return sum(fn(r) for r in run['monthly'])
 def threshold(run,key):return f'Monat {run["first_thresholds"][key]}' if key in run['first_thresholds'] else 'bis Monat 600 nicht erreicht'
 before=mean(old['monthly'][-120:],lambda r:r['purchase_totals']['unit_remainder_cents']);after=mean(new['monthly'][-120:],lambda r:r['purchase_totals']['unit_remainder_cents'])
 change=(total(new,lambda r:r['consumption_cents'])/total(old,lambda r:r['consumption_cents'])-1)*100
 lines=['# Kleinere Gütereinheiten im Vergleich über 600 Monate','', 'Stand: 3. November 2026. Simulierter Befund innerhalb der illustrativen Modellwirtschaft v14.','',
 f'Mit Hundertsteln der bisherigen Gütereinheiten erreicht der Staat bis Monat 600 weder seine Kreditgrenze noch einen ungedeckten Sozialbedarf. Die Staatsschuld beträgt am Ende {euro(b["government_debt_cents"])} statt {euro(a["government_debt_cents"])}. Im Mittel der letzten 120 Monate verbleibt ein Defizit auf vollständiger Bedarfsbasis; eine dauerhaft ausgeglichene Wirtschaft ist damit nicht belegt.','',
 '## Vergleich und unveränderte Annahmen','',
 'Je eine bisherige Einheit wird durch 100 kleinere Einheiten ersetzt. Stückpreise werden von 100 beziehungsweise 150 Euro auf 1 beziehungsweise 1,50 Euro geteilt. Energie je Teil kostet ein Hundertstel; Arbeitsproduktivität, Anfangsabsatzpläne, Exportbestellungen, Maschinenmaterialbedarf und Maschinenkapazität werden mit 100 multipliziert. Ein Maschinenkauf kostet weiterhin 1.200 Euro und erhöht die ursprüngliche Kapazität um vier Einheiten. Geldbeträge werden weiterhin in ganzen Cent verbucht.','',
 'Anfangsguthaben, Kredite, Zinssätze, 30 % Lohnsteuer, 20 % Gewinnsteuer, 25 % Ausschüttungssteuer, Löhne, 1.000 Euro Transfer-Referenzbedarf, 95 % Konsumquote, Firmenentscheidungen und anpassende Staatsregel bleiben unverändert. Es gibt keine zusätzlichen Schocks oder LLM-Aufrufe. Beide Varianten durchlaufen 600 Monate mit jeweils fünf Phasen. Der normale Start behält die bisherige Stückelung.','',
 'Die geänderte Auflösung betrifft alle Warenkäufe sowie die Rundung von Absatzplänen, Produktion und Lager. Sie misst den Gesamteffekt feinerer Gütereinheiten. Der Anteil der Haushalts-Kaufrundung allein wird damit nicht separat identifiziert. Preise pro ursprünglicher Gütermenge und reale Anfangskapazitäten bleiben gleich; die späteren Mengen und Entscheidungen dürfen auf die geänderten Verkäufe reagieren.','',
 f'![Verlauf beider Stückelungen]({target.name}.svg)','', '## Ergebnisse nach 600 Monaten','', '| Grösse | Bisherige Einheiten | Hundertstel |','| --- | ---: | ---: |']
 for title,key in [('Staatsschuld','government_debt_cents'),('Staatskasse','government_cash_cents'),('Haushaltsguthaben zusammen','household_cash_cents'),('Firmenguthaben zusammen','firm_cash_cents'),('Haushaltskäufe nur in Monat 600','consumption_cents')]:lines.append(f'| {title} | {euro(a[key])} | {euro(b[key])} |')
 lines += [f'| Arbeitsverträge am Monatsende | {a["employment"]} | {b["employment"]} |',f'| Staatskreditgrenze | {threshold(old,"credit_limit_reached")} | {threshold(new,"credit_limit_reached")} |',f'| Erster ungedeckter Sozialbedarf | {threshold(old,"social_funding_gap")} | {threshold(new,"social_funding_gap")} |','', '## Zahlungsflüsse und Rundungsreste','', '| Über alle 600 Monate | Bisherige Einheiten | Hundertstel |','| --- | ---: | ---: |']
 for title,fn in [('Bezahlte Haushaltskäufe',lambda r:r['consumption_cents']),('Nicht ausgegeben durch Güterstückelung',lambda r:r['purchase_totals']['unit_remainder_cents']),('Ungedeckter Sozial-Referenzbedarf',lambda r:r['public_budget']['social_unfunded_cents']),('Tatsächlich gezahlte Steuern',lambda r:r['taxes_cents'])]:lines.append(f'| {title} | {euro(total(old,fn))} | {euro(total(new,fn))} |')
 lines+=['',f'Die bezahlten Haushaltskäufe liegen insgesamt um {str(round(change,1)).replace(".",",")} % höher. Der monatliche Stückelungsrest sinkt im Mittel von Monat 481 bis 600 von {euro(before)} auf {euro(after)}. Bereits im ersten Monat fällt er von 1.176 auf 12 Euro bei identischem finanzierbarem Kaufbudget.','',
 'Rundungsreste sind vorhandenes Geld, das aus einem finanzierbaren Kaufbudget nicht ausgegeben wird. Sie sind weder verschwundenes Geld noch automatisch ein gleich hoher Steuerausfall. Bei kumulierten Werten kann dasselbe Geld mehrfach als ungenutztes Budget auftauchen. Die Differenz der Restbeträge ist deshalb keine direkte Messung der vermiedenen Staatsschuld.','',
 '## Verbleibendes Defizit','', '| Monatsmittel von 481 bis 600 | Bisherige Einheiten | Hundertstel |','| --- | ---: | ---: |']
 for title,fn in [('Steuereinnahmen',lambda r:r['taxes_cents']),('Vollständiger laufender Ausgabenbedarf',lambda r:r['public_budget']['committed_spending_cents']),('Saldo auf vollständiger Bedarfsbasis',lambda r:r['public_budget']['commitment_balance_cents'])]:lines.append(f'| {title} | {euro(mean(old["monthly"][-120:],fn))} | {euro(mean(new["monthly"][-120:],fn))} |')
 lines+=['', 'Im feinen Lauf werden alle Sozial-Referenzbeträge finanziert. Im groben Lauf sind die tatsächlich geleisteten Zahlungen begrenzt; ein annähernd ausgeglichener Zahlungssaldo dort ist keine Deckung des vollständigen Bedarfs. Im feinen Lauf bleibt die Kreditaufnahme zur Finanzierung fortlaufender Defizite erforderlich. Aus dem Befund bis Monat 600 folgt keine unbegrenzte Tragfähigkeit.','',
 '## Wirkung innerhalb des Modells','',
 'Das erste Kaufbudget ist in beiden Varianten gleich. Der feinere Verkauf lässt davon mehr als Umsatz bei den Unternehmen ankommen. Nachfolgende Absatz-, Arbeitszeit-, Personal- und Steuerentscheidungen reagieren nach denselben bestehenden Formeln auf andere Zahlungseingänge. Im feinen Lauf sinkt die Zahl öffentlicher Stellen erstmals in Monat 22 statt 16; am Ende gibt es in beiden Varianten keine öffentlichen Stellen. Die vier Arbeitsverträge im feinen Endmonat liegen im privaten Sektor.','',
 'Die grobe Stückelung beeinflusst den bisherigen Krisenverlauf damit erheblich. Sie erklärt jedoch nicht das gesamte verbleibende Defizit. Das Ergebnis rechtfertigt weitere Prüfung der vorhandenen Annahmen und ihrer Auflösung, ohne zusätzliche fiskalische Regeln einzubauen. Es ist ein kontrollierter Softwarebefund innerhalb dieser Modellwirtschaft, kein empirischer Nachweis realer Wirtschaftswirkungen.','',
 '## Reproduktion und Belege','',
 f'[Alle Monatswerte mit Haushaltsbudgets und Firmenplänen]({Path(source).name}) · [Ausgangslauf mit Ausschüttungssteuer](tax-v14-comparison.md) · [Einheiten und Prüfregeln](../poc/GOODS_GRANULARITY_EXPERIMENT.md).','',
 'Der Referenzlauf reproduziert alle 600 archivierten Monatsabschlüsse bei Geldbeständen, Staatsschuld, Konsum, Produktion, Beschäftigung, Steuereinnahmen und Budgetentscheidungen exakt. Die Rohdaten enthalten Quellprüfsummen und die Prüfsumme des verwendeten Referenzarchivs.','',
 '```sh','poc/.venv/bin/python poc/scripts/compare_goods_granularity.py --months 600','python poc/scripts/report_goods_granularity.py --source .framework-review/goods-granularity-comparison.json --output .framework-review/goods-granularity-comparison','```','',
 'Matplotlib wird nur für die Abbildung benötigt. Standardausgaben liegen unter `.framework-review`; archivierte Befunde werden nicht überschrieben. Die beiden Glättungskurven verwenden zwölf zurückliegende Monatswerte, am Laufanfang entsprechend weniger.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',default='.framework-review/goods-granularity-comparison.json');p.add_argument('--output',default='.framework-review/goods-granularity-comparison');a=p.parse_args();report(a.source,a.output)
