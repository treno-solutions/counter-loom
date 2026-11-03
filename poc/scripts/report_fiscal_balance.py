"""Explain the current-default fiscal gap with a reproduced cash-flow bridge."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def euro(c):return f'{c/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')+' €'
def report(source,output):
 data=json.loads(Path(source).read_text());w=data['window'];n=w['count'];t=w['totals'];b=t['household_bridge'];s=t['sector_cash_change_cents'];tax=t['taxes_by_kind'];target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
 assert data['months']==600 and w['start']==481 and w['end']==600
 avg=lambda v:v/n
 plt.rcParams.update({'font.size':10,'svg.fonttype':'none','svg.hashsalt':'counterloom-fiscal-diagnosis-v15'})
 fig,axes=plt.subplots(2,1,figsize=(12,9),gridspec_kw={'height_ratios':[1,1.2]});fig.subplots_adjust(top=.88,bottom=.12,hspace=.55)
 fig.suptitle('Counterloom · Zusammensetzung des verbleibenden Staatsdefizits',fontsize=15)
 fig.text(.5,.92,f'Mittelwerte der Monate {w["start"]} bis {w["end"]} · kleinere Gütereinheiten · unveränderte Wirtschaftsregeln',ha='center',fontsize=10)
 ax=axes[0]
 sources=[('Lohnsteuer',tax['income_tax']+tax['arrears_income_tax'],'#526f89'),('Gewinnsteuer',tax['profit_tax'],'#7d98aa'),('Ausschüttungssteuer',tax['distribution_tax'],'#a9bdc4')]
 costs=[('Transfers',t['social_paid_cents'],'#66895a'),('Staatszinsen',t['interest_paid_cents'],'#b5804d')]
 for x,items in [(0,sources),(1,costs)]:
  bottom=0
  for label,value,color in items:
   v=avg(value)/100;ax.bar(x,v,bottom=bottom,color=color,width=.5,label=label);bottom+=v
  ax.text(x,bottom+35,euro(avg(sum(v for _,v,_ in items))),ha='center',fontweight='bold')
 ax.set_xticks([0,1],['Steuereingänge','Bezahlte Ausgaben']);ax.set_xlim(-.8,1.8);ax.set_ylim(0,2700);ax.set_ylabel('Euro pro Monat');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,-.13),frameon=False,fontsize=9)
 ax.set_title(f'Finanzierungslücke: {euro(avg(t["cash_deficit_cents"]))} monatlich',loc='left')
 ax=axes[1];running=0
 entries=[('Kaufplan',b['planned_retention_cents'],False),('Ware fehlt',b['stock_gap_cents'],False),('Stückelung',b['unit_remainder_cents'],False),('Zeitlage',b['distribution_timing_cents'],False),('Haushalte\ngesamt',b['actual_saving_cents'],True),('Firmen',s['firms'],False),('Ausland',s['external'],False),('Staatsdefizit',t['cash_deficit_cents'],True)]
 for i,(label,value,total) in enumerate(entries):
  v=avg(value)/100
  if total:bottom=0;running=v;color='#526f89'
  else:bottom=running if v>=0 else running+v;running+=v;color='#66895a' if v>=0 else '#b5804d'
  ax.bar(i,abs(v),bottom=bottom,color=color,width=.65)
  top=v if total else max(bottom,bottom+abs(v));ax.text(i,top+4,euro(avg(value)),ha='center',fontsize=9)
  if i<7:ax.plot([i+.325,i+.675],[running,running],color='#999',lw=.7)
 ax.set_xticks(range(len(entries)),[e[0] for e in entries]);ax.set_ylabel('Euro pro Monat');ax.set_ylim(0,225);ax.set_title('Gegenkonten des Defizits und Entstehung des Haushaltsguthabens',loc='left');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 fig.text(.5,.03,'Kaufplan: Einkommensbasis minus Konsumwunsch. Zeitlage: aktuelle Nettoauszahlung minus Ausschüttungen der vorherigen Kaufrunde.',ha='center',fontsize=9)
 fig.savefig(target.with_suffix('.svg'),metadata={'Date':None,'Creator':'Counterloom / Matplotlib'});p=target.with_suffix('.svg');p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n');fig.savefig(target.with_suffix('.png'),dpi=130);plt.close(fig)
 lines=['# Zusammensetzung des verbleibenden Staatsdefizits','', 'Stand: 3. November 2026. Modell v15 verwendet die kleineren Gütereinheiten als Standard. Steuer-, Ausgaben- und Verhaltensregeln bleiben erhalten.','',
 f'Der neue Standard reproduziert jeden der 600 Abschlüsse des bisherigen feinen Gegenlaufs. In Monat {w["start"]} bis {w["end"]} beträgt das Defizit durchschnittlich {euro(avg(t["cash_deficit_cents"]))}. Sämtliche Sozial-Referenzbeträge dieses Zeitraums werden bezahlt. Die Finanzierungslücke entspricht vollständig den zusätzlich aufgebauten Guthaben der anderen Sektoren.','',
 f'![Einnahmen und Ausgaben sowie Gegenkonten des Defizits]({target.name}.svg)','', '## Einnahmen und Ausgaben pro Monat','', '| Monatsmittel | Betrag |','| --- | ---: |']
 for label,value in [('Lohnsteuer einschliesslich Nachzahlungen',tax['income_tax']+tax['arrears_income_tax']),('Gewinnsteuer',tax['profit_tax']),('Ausschüttungssteuer',tax['distribution_tax']),('Alle Steuern',t['total_taxes_cents']),('Transfers',t['social_paid_cents']),('Staatszinsen',t['interest_paid_cents']),('Öffentliche Löhne',t['public_payroll_cents']),('Beschaffung',t['procurement_budget_cents']),('Alle laufenden Ausgaben',t['committed_spending_cents']),('Defizit',t['cash_deficit_cents'])]:lines.append(f'| {label} | {euro(avg(value))} |')
 lines+=['',f'Bereits vor der Zinsausgabe fehlen bei den tatsächlich vorliegenden Steuereingängen durchschnittlich {euro(avg(t["primary_need_deficit_cents"]))}. Hinzu kommen {euro(avg(t["interest_paid_cents"]))} bezahlte Zinsen. Diese Zerlegung ist eine Rechnung über den vorhandenen Lauf. Ein Lauf ohne Staatszinsen würde auch die Bankausschüttungen und Steuereingänge verändern; sein Nettoeffekt ist hier nicht gemessen.','',
 'Der Transferbedarf besteht aus jeweils 1.000 Euro für h5 und h6 sowie durchschnittlich 216,67 Euro für h4. Der vierte Haushalt ist in 26 der 120 Lohnrunden ohne Arbeit. Die Werkstatt wechselt wiederholt zwischen einer und zwei Arbeitskräften. Verträge und tatsächliche Arbeitszeit sind getrennt: Die zwei Beschäftigten im Alltagsbetrieb arbeiten im Mittel rund 53 % Vollzeit, die betriebliche Arbeitszeitquote der Werkstatt beträgt im Monatsmittel rund 59 %. Diese Werte beschreiben die laufenden Firmenentscheidungen bei der vorhandenen Nachfrage.','',
 '## Wo die Finanzierungslücke als Guthaben ankommt','', '| Veränderung der Guthaben pro Monat | Betrag |','| --- | ---: |']
 for label,key in [('Haushalte','households'),('Unternehmen','firms'),('Ausland','external'),('Bankeigenkapital','bank')]:lines.append(f'| {label} | {euro(avg(s[key]))} |')
 lines+=['',f'Die Haushalte bauen monatlich {euro(avg(s["households"]))} auf. Firmen und Ausland geben geringfügig Guthaben ab. Zusammengenommen entsprechen die Veränderungen exakt den {euro(avg(t["cash_deficit_cents"]))} Staatsdefizit. Der vollständige Monatslauf und jede einzelne Buchungsidentität wurden erneut geprüft.','',
 'Kredit finanziert die Lücke, ohne sie als Einnahme auszugeben. Von Ende Monat 480 bis Ende Monat 600 wächst die Staatsschuld um 22.118,36 Euro. Das kumulierte Defizit beträgt 22.066,70 Euro; die Differenz von 51,66 Euro erhöht die Staatskasse. Es gibt keinen zusätzlichen Maschinenkredit und das Bankkapital bleibt konstant.','',
 '## Warum die Haushalte Guthaben aufbauen','', '| Beitrag pro Monat | Betrag |','| --- | ---: |']
 for label,key in [('Einkommensbasis über dem gewünschten Kaufbudget','planned_retention_cents'),('Finanzierbar aber Ware fehlt','stock_gap_cents'),('Rest aus Stückelung','unit_remainder_cents'),('Geldmangel gegenüber dem Kaufplan','funding_gap_cents'),('Zeitlage aktueller und vorheriger Ausschüttungen','distribution_timing_cents'),('Tatsächliche Guthabenzunahme','actual_saving_cents')]:lines.append(f'| {label} | {euro(avg(b[key]))} |')
 lines+=['', 'Mittelwerte sind auf Cent gerundet; die Rohdaten rechnen mit ganzen Cent und prüfen die Gleichung vor jeder Mittelwertbildung exakt.','',
 'Die Konsumregel verwendet 95 % der Einkommensbasis, mindestens 1.000 Euro. Die Basis umfasst Lohn und Transfers nach Lohnsteuer sowie die Nettoauszahlungen seit der vorherigen Kaufrunde. Guthaben oberhalb des Grundbedarfs erhöht diesen einkommensabhängigen Plan nicht automatisch. Die Differenz zwischen Einkommensbasis und Konsumwunsch bleibt deshalb als geplantes Zurückbehalten erhalten; bei niedriger Basis kann der Mindestbedarf umgekehrt alte Rücklagen verbrauchen. Die tatsächliche Nettosumme dieser Planungswirkung beträgt hier 139,36 Euro monatlich.','',
 'Weitere 42,79 Euro könnten aus dem geplanten Budget bezahlt werden, treffen aber auf fehlende Ware. Kaufreihenfolge, Lager und geglättete Produktionsplanung erzeugen Lieferlücken auch dann, wenn Betriebe in anderen Monaten freie Kapazität haben. Die beobachteten Lieferlücken sind gemessen; welcher einzelne Firmenparameter sie verursacht, wird durch diese reine Buchungsdiagnose nicht isoliert. Die restliche Güterstückelung trägt nur 5,22 Euro bei.','',
 'Die kleinen 0,34 Euro aus der Zeitlage entstehen, weil der Kaufplan frühere Ausschüttungen nutzt, der Kontostand am Monatsende aber die neue Auszahlung enthält. Sie sind kein verschwundener Betrag und kein zusätzlicher Sparparameter.','',
 '## Haushalte einzeln','', '| Haushalt | Transfer pro Monat | Guthabenzuwachs pro Monat | Guthaben Ende M600 |','| --- | ---: | ---: | ---: |']
 for h in w['households']:lines.append(f'| {h["id"]} | {euro(avg(h["transfer_cents"]))} | {euro(avg(h["actual_saving_cents"]))} | {euro(h["closing_cash_cents"])} |')
 lines+=['', 'h5 und h6 erhalten weiterhin den vollen 1.000-Euro-Transfer und gleiche Unternehmensanteile, obwohl ihre Guthaben steigen. Der Transfer kennt im bestehenden Modell keine Prüfung des Vermögens und keine Verrechnung von Ausschüttungseinkommen. Aus Transfer plus Nettoauszahlung wird wie bei den anderen Haushalten ein Kaufplan gebildet. Diese bestehenden Annahmen ermöglichen laufenden Guthabenzuwachs auch ohne Beschäftigung. Sie wurden für die Diagnose nicht verändert.','',
 '## Einordnung und nächste Prüfung','',
 'Das verbleibende Defizit lässt sich aus den vorhandenen Regeln und Zahlungen vollständig erklären. Die hohe grobe Rundung ist weitgehend beseitigt. Das Modell erlaubt nun weiterhin geplantes Zurückbehalten von Einkommen und begrenzte Warenkäufe, während der Staat Sozialleistungen und Zinsen finanziert. Eine Anlageentscheidung, die Haushaltsersparnisse wieder in zusätzliche reale Investitionen oder Nachfrage übersetzt, ist bislang kein eigener Haushaltsprozess. Eine Umbuchung auf ein anderes Finanzkonto allein würde die fehlende Nachfrage jedoch nicht ersetzen.','',
 'Die Sektorrechnung belegt die Gegenbuchungen, aber keine alleinige wirtschaftliche Ursache oder einen eindeutigen Eingriff. Zur weiteren Ursachentrennung wären kontrollierte Gegenläufe zu vorhandener Konsumquote, Grundbedarfsgrenze und Lieferlücken geeignet. In dieser Fassung wurde weder ein solcher Eingriff noch eine neue Steuer-, Transfer- oder Ausgabenregel eingebaut. Die 184 Euro sind der Durchschnitt des untersuchten Fensters, kein garantierter Wert für spätere Monate.','',
 '## Daten und Reproduktion','',f'[Monatsdaten und exakte Zerlegungen]({Path(source).name}) · [Vergleich der Stückelungen](goods-granularity-comparison.md) · [Modellumfang](../poc/WORLD_MODEL.md).','',
 '```sh','poc/.venv/bin/python poc/scripts/diagnose_fiscal_balance.py','python poc/scripts/report_fiscal_balance.py --source .framework-review/fiscal-balance-diagnosis.json --output .framework-review/fiscal-balance-v15-diagnosis','```','',
 'Die Diagnose startet die normale Konfiguration von v15. Sie vergleicht alle 600 Monate gegen den archivierten feinen Lauf und wertet anschliessend Monate 481 bis 600 aus. Rohdaten enthalten verwendete Quellenprüfsummen. Matplotlib ist nur für die Abbildung erforderlich.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',default='.framework-review/fiscal-balance-diagnosis.json');p.add_argument('--output',default='.framework-review/fiscal-balance-v15-diagnosis');a=p.parse_args();report(a.source,a.output)
