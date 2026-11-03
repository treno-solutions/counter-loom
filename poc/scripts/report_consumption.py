"""Reproducible controlled-consumption comparison and macro time series."""
import argparse,json
from pathlib import Path
from itertools import accumulate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def euro(v):return f'{v/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def rolling(v):return [sum(v[max(0,i-11):i+1])/min(i+1,12) for i in range(len(v))]
def report(source,output):
 x=json.loads(Path(source).read_text());assert x['months']==600
 old,new=x['runs'];assert [r['consumption_percent'] for r in x['runs']]==[95,100]
 target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
 plt.rcParams.update({'font.size':9,'svg.fonttype':'none','svg.hashsalt':'counterloom-consumption-v16'})
 fig,axes=plt.subplots(3,2,figsize=(12,10));fig.subplots_adjust(top=.9,bottom=.09,hspace=.44,wspace=.25);fig.suptitle('Counterloom · Konsumquote 95 % und 100 % über 600 Monate',fontsize=15)
 fig.text(.5,.94,'Nur die Konsumquote ändert sich. Kleine Gütereinheiten, gleiche Anfangswerte und Wirtschaftsregeln; keine Schocks.',ha='center',fontsize=9)
 panels=[('debt','Staatsschuld','Tsd. Euro'),('employment','Arbeitsverträge am Monatsende','Verträge'),('purchases','Haushaltskäufe · kumulierter Zahlungsfluss','Tsd. Euro'),('budget','Steuern minus vollständiger Bedarf · 12-Monatsmittel','Euro / Monat'),('shortage','Finanzierbar, aber Ware fehlt · 12-Monatsmittel','Euro / Monat'),('gdp','BIP-Näherung nominal · 12-Monatsmittel','Tsd. Euro / Monat')]
 for ax,(key,title,unit) in zip(axes.flat,panels):
  for r,color,label in [(old,'#526f89','95 % Konsumquote'),(new,'#66895a','100 % Konsumquote')]:
   rows=r['monthly']
   if key=='debt':v=[m['government_debt_cents']/100000 for m in rows]
   elif key=='employment':v=[m['employment'] for m in rows]
   elif key=='purchases':v=list(accumulate(m['consumption_cents']/100000 for m in rows))
   elif key=='budget':v=rolling([m['public_budget']['commitment_balance_cents']/100 for m in rows])
   elif key=='shortage':v=rolling([m['purchase_totals']['stock_gap_cents']/100 for m in rows])
   else:v=rolling([m['macro']['gdp_proxy_cents']/100000 for m in rows])
   ax.plot([m['month'] for m in rows],v,color=color,lw=1.5,label=label)
  ax.set_title(title,loc='left',fontsize=10);ax.set_ylabel(unit);ax.set_xlabel('Monat');ax.set_xlim(1,600);ax.grid(alpha=.2)
  if key=='employment':ax.set_ylim(0,6.5);ax.set_yticks([0,2,4,6])
  if key=='budget':ax.axhline(0,color='#777',lw=.7)
 fig.legend(*axes.flat[0].get_legend_handles_labels(),loc='lower center',ncol=2,frameon=False)
 fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'});p=target.with_suffix('.svg');p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n');fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
 def avg(r,fn):return sum(fn(m) for m in r['monthly'][-120:])/120
 a,b=old['monthly'][-1],new['monthly'][-1]
 lines=['# Vergleich der Konsumquoten über 600 Monate','', 'Stand: 3. November 2026. Eigener simulierter Befund im Modell v16.','',
 f'Bei 100 % statt 95 % Konsumquote beträgt die Staatsschuld nach 600 Monaten {euro(b["government_debt_cents"])} statt {euro(a["government_debt_cents"])}. Am Ende bestehen {b["employment"]} statt {a["employment"]} Arbeitsverträge. In den letzten 120 Monaten beträgt der Bedarfssaldo bei 100 % durchschnittlich {euro(avg(new,lambda m:m["public_budget"]["commitment_balance_cents"]))}; bei 95 % liegt er bei {euro(avg(old,lambda m:m["public_budget"]["commitment_balance_cents"]))}.','',
 '## Kontrollierter Aufbau','', 'Beide Läufe starten mit identischen Guthaben, kleinen Gütereinheiten, Zinssätzen, Krediten, 25 % Ausschüttungssteuer, adaptivem Staatsbudget und denselben Firmenentscheidungen. Nur die Quote im einkommensabhängigen Haushalts-Kaufplan wird vor dem ersten Monat von 95 auf 100 gesetzt. Mindestbedarf, Lagergrenzen, Kaufreihenfolge und alle weiteren Regeln bleiben erhalten. Es gibt keine Schocks. Die normale Oberfläche behält 95 % als Ausgangsquote.','',
 '100 % bezieht sich auf die Einkommensbasis, nicht auf das gesamte Vermögen. Es ist ein diagnostischer Gegenlauf, keine behauptete realistische Konsumregel. Fehlende Ware und Stückelung können weiterhin Ausgaben verhindern. Der Mindestbedarf kann bei geringerem Einkommen vorhandene Rücklagen beanspruchen.','',
 f'![Geldströme und Makroverläufe beider Quoten]({target.name}.svg)','', '## Endbestände und gesamte Käufe','', '| Kennzahl | 95 % | 100 % |','| --- | ---: | ---: |']
 for title,key in [('Staatsschuld M600','government_debt_cents'),('Staatskasse M600','government_cash_cents'),('Haushaltsguthaben M600','household_cash_cents'),('Firmenguthaben M600','firm_cash_cents')]:lines.append(f'| {title} | {euro(a[key])} | {euro(b[key])} |')
 lines += [f'| Arbeitsverträge M600 | {a["employment"]} | {b["employment"]} |',f'| Davon öffentliche Stellen | {a["public_budget"]["approved_staff"]} | {b["public_budget"]["approved_staff"]} |',f'| Haushaltskäufe über alle Monate | {euro(sum(m["consumption_cents"] for m in old["monthly"]))} | {euro(sum(m["consumption_cents"] for m in new["monthly"]))} |','', '## Durchschnitt der Monate 481 bis 600','', '| Monatlicher Betrag | 95 % | 100 % |','| --- | ---: | ---: |']
 for title,fn in [('Steuereinnahmen',lambda m:m['taxes_cents']),('Vollständiger laufender Bedarf',lambda m:m['public_budget']['committed_spending_cents']),('Saldo vor Finanzierung',lambda m:m['public_budget']['commitment_balance_cents']),('Geplantes Zurückbehalten von Einkommen',lambda m:m['planned_retention_cents']),('Tatsächliche Haushaltsersparnis',lambda m:m['household_saving_cents']),('Finanzierbare Käufe ohne verfügbare Ware',lambda m:m['purchase_totals']['stock_gap_cents']),('Rest wegen ganzer Warenteile',lambda m:m['purchase_totals']['unit_remainder_cents']),('Ungedeckter Sozialbedarf',lambda m:m['public_budget']['social_unfunded_cents'])]:lines.append(f'| {title} | {euro(avg(old,fn))} | {euro(avg(new,fn))} |')
 lines+=['', '## Interpretation','',
 'Die zeitlichen Verläufe unterscheiden sich deutlich: Der 100-%-Lauf nimmt bereits in Monat 128 Staatskredit auf, der 95-%-Lauf erst in Monat 415. Bei 100 % steigt die Schuld bis Monat 156 auf 15.151,29 Euro und sinkt anschliessend langfristig. Die erhaltenen öffentlichen Stellen verursachen anfangs weiterhin Ausgaben. Ein besserer Endbestand bedeutet daher keine geringere Kreditaufnahme in jedem einzelnen Monat.','',
 'Die geplante Zurückhaltung von Einkommen fällt im späten 100-%-Lauf vollständig weg. Gleichzeitig verschwinden dort die beobachteten Lieferlücken und die sechs Arbeitsverträge bleiben bestehen. Der Staat erzielt mehr Steuereinnahmen und finanziert eine andere Ausgabenstruktur. Der Saldo verbessert sich daher nicht bloss um den zuvor zurückbehaltenen Geldbetrag; die Unternehmens- und Staatsentscheidungen reagieren auf die veränderte Nachfrage.','',
 'Dieser Gegenlauf zeigt, dass die Konsumquote innerhalb der vorhandenen Regeln wesentlich zum bisherigen Defizit- und Beschäftigungsverlauf beiträgt. Die Verbesserung ist der Gesamteffekt der einen geänderten Annahme einschliesslich ihrer Rückkopplungen. Sie ist kein empirischer Nachweis, dass reale Ersparnis schädlich wäre oder eine Konsumquote von 100 % dauerhaft sinnvoll wäre. Ein kleiner später Überschuss und eine verbleibende Staatsschuld belegen auch keine unbegrenzte Stabilität.','',
 'Die Makroanzeige wird nur aus bereits ausgeführten Vorgängen berechnet und greift nicht in Entscheidungen ein. Die BIP-Näherung ist nominal und verwendet Lagerkosten sowie gezahlte öffentliche Löhne als vereinfachte Bewertungsansätze. Sie ist keine amtliche BIP-Rechnung; [Definitionen und Grenzen](../poc/MACRO_ACCOUNTS.md).','',
 '## Nachvollziehbarkeit','',f'[Alle Monatswerte und Quellprüfsummen]({Path(source).name}) · [Vorherige Defizitdiagnose](fiscal-balance-v15-diagnosis.md).','',
 'Der 95-%-Zweig reproduziert alle 600 archivierten feinen Abschlüsse bei Haushalts-, Firmen-, Staats- und Auslandsguthaben, Staatsschuld, Konsum, Beschäftigung, Steuern und vollständiger Budgetentscheidung exakt. Die Makroberechnung wird zusätzlich durch einen Lauf mit ausgeschalteter Beobachtung auf Einflussfreiheit geprüft.','',
 '```sh','poc/.venv/bin/python poc/scripts/compare_consumption.py --months 600','python poc/scripts/report_consumption.py --source .framework-review/consumption-comparison.json --output .framework-review/consumption-v16-comparison','```','',
 'Die Rohdaten speichern alle Monate beider Varianten und die Prüfsumme des Referenzarchivs. Die Abbildung glättet ausgewiesene Monatsgrössen über zwölf zurückliegende Werte; am Anfang werden entsprechend weniger Werte verwendet.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',default='.framework-review/consumption-comparison.json');p.add_argument('--output',default='.framework-review/consumption-v16-comparison');a=p.parse_args();report(a.source,a.output)
