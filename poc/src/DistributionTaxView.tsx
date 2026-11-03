import type { World } from './world-schema';
const money=(v:number)=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:2}).format(v/100);
export default function DistributionTaxView({world,source,month}:{world:World;source?:string;month?:number}) {
 const t=world.distribution_tax;
 const row=month===undefined?t.monthly:t.history.find(r=>r.month===month)??(t.monthly.month===month?t.monthly:undefined);
 if(!row)return <section className="distribution-tax-view"><h4>Ausschüttungssteuer · Monat {month}</h4><p>Dieser Abschluss liegt ausserhalb der letzten 36 interaktiven Steuerabschlüsse. Die vollständigen Beträge und Belege stehen im Laufexport.</p></section>;
 const totals=source?row.sources.find(r=>r.id===source)!:row;
 const rows=t.history.map(r=>({month:r.month,...(source?r.sources.find(s=>s.id===source)!:r)}));
 const max=Math.max(100,...rows.map(r=>r.gross_cents));
 const first=rows[0]?.month??1,last=rows.at(-1)?.month??1;
 const x=(m:number)=>55+(m-first)*465/Math.max(1,last-first);
 const y=(v:number)=>130-v/max*100;
 return <section className="distribution-tax-view" aria-label="Ausschüttungssteuer und Nettoeinkommen">
  <h4>Ausschüttungen: Brutto → Steuer → Netto · Monat {row.month}</h4>
  <p>Modellannahme: {(t.rate_bps/100).toLocaleString('de-DE')} % auf tatsächlich ausgezahlte Firmengewinne und Bankzinsen. Einbehalt bei Auszahlung, ohne Freibetrag. Die Gewinnsteuer des Unternehmens bleibt eine eigene Steuer.</p>
  <div className="distribution-tax-flow"><div><span>Brutto ausgeschüttet</span><strong>{money(totals.gross_cents)}</strong></div><div><span>An den Staat einbehalten</span><strong>{money(totals.tax_cents)}</strong></div><div><span>Netto für Haushalte</span><strong>{money(totals.net_cents)}</strong></div></div>
  <div className="distribution-tax-bar" role="img" aria-label={`Von ${money(totals.gross_cents)} brutto gehen ${money(totals.tax_cents)} an den Staat und ${money(totals.net_cents)} netto an Haushalte`}><i style={{width:`${100*totals.tax_cents/Math.max(1,totals.gross_cents)}%`}}/><b style={{width:`${100*totals.net_cents/Math.max(1,totals.gross_cents)}%`}}/></div>
  <p>Orange: Steuer · Grün: Netto. Der Nettobetrag wird in der nächsten Kaufrunde berücksichtigt. Die Überweisung verändert die Verteilung vorhandenen Geldes.</p>
  {!source&&<div className="distribution-tax-flow"><div><span>Lohnsteuer · einschliesslich Nachzahlungen</span><strong>{money(row.state_taxes.income_tax+row.state_taxes.arrears_income_tax)}</strong></div><div><span>Gewinnsteuer · Unternehmen</span><strong>{money(row.state_taxes.profit_tax)}</strong></div><div><span>Ausschüttungssteuer · Haushalte</span><strong>{money(row.state_taxes.distribution_tax)}</strong></div></div>}
  {!source&&<div className="account-table-scroll"><table><thead><tr><th>Haushalt</th><th>Brutto</th><th>Steuer</th><th>Netto</th></tr></thead><tbody>{row.households.map(h=><tr key={h.id}><td>{world.nodes.find(n=>n.id===h.id)?.name}</td><td>{money(h.gross_cents)}</td><td>{money(h.tax_cents)}</td><td>{money(h.net_cents)}</td></tr>)}</tbody></table></div>}
  {rows.length>0&&<figure><figcaption>Ausschüttungen und Einbehalt · letzte {rows.length} Abschlüsse</figcaption><svg viewBox="0 0 550 160" role="img" aria-label="Bruttoausschüttung durchgezogen, Nettobetrag grün, Steuer orange; gemeinsame Euro-Skala">{[0,.5,1].map(f=><g key={f}><line x1="55" x2="520" y1={y(f*max)} y2={y(f*max)} className="consumption-grid"/><text x="49" y={y(f*max)+4} textAnchor="end">{Math.round(f*max/100)} €</text></g>)}{(['gross','tax','net'] as const).map(k=><polyline key={k} className={`distribution-line-${k}`} points={rows.map(r=>`${x(r.month)},${y(r[`${k}_cents`])}`).join(' ')}/>)}{row.month>=first&&row.month<=last&&<line x1={x(row.month)} x2={x(row.month)} y1="25" y2="130" className="consumption-selection"/>}{rows.filter(r=>r.month===first||r.month===last||r.month%6===0).map(r=><text key={r.month} x={x(r.month)} y="151" textAnchor="middle">M{r.month}</text>)}</svg><p>Blau: Brutto · Orange: Steuer · Grün: Netto. Alle Abschlüsse und Einzelbelege stehen im Laufexport.</p></figure>}
 </section>;
}
