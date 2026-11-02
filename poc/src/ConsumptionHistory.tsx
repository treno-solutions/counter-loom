import { useState } from 'react';
import { Activity } from 'lucide-react';
import PriceTransmission from './PriceTransmission';
import type { World } from './world-schema';

const money=(c:number)=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:c%100?2:0}).format(c/100);
const rate=(v:number)=>`${(v/100).toLocaleString('de-DE')} %`;
export default function ConsumptionHistory({world}:{world:World}) {
 const [chosen,setChosen]=useState<number|null>(null);
 const [real,setReal]=useState(false);
 const months=world.history,latest=months.at(-1),selected=months.find(m=>m.month===chosen)??latest;
 const households=world.nodes.filter(n=>n.sector==='households');
 const name=(id:string|null)=>id?world.nodes.find(n=>n.id===id)?.name??id:'ohne Beschäftigung';
 const events=new Map<number,string[]>();
 const add=(month:number,text:string)=>events.set(month,[...(events.get(month)??[]),text]);
 for(const e of world.active) add(e.month,e.event==='energy'?'Energiekosten verdoppelt':e.event==='demand'?'Konsumquote auf 65 % gesenkt':'Konsumquote auf 95 % zurückgesetzt');
 for(const e of world.monetary_policy.changes) add(e.month,`Leitzins: ${rate(e.old_rate_bps)} → ${rate(e.new_rate_bps)}`);
 for(const [i,m] of world.monetary_policy.history.entries()) {
  const before=world.monetary_policy.history[i-1]?.variable_rate_bps??world.monetary_policy.initial_rate_bps;
  if(before!==m.variable_rate_bps) add(m.month,`Variabler Betriebskredit: ${rate(before)} → ${rate(m.variable_rate_bps)}`);
 }
 for(const [i,m] of months.entries()) for(const h of m.households) {
  const before=months[i-1]?.households.find(p=>p.id===h.id);
  if(before&&before.employer!==h.employer) add(m.month,`${name(h.id)}: ${before.employer?`Arbeitsplatz bei ${name(before.employer)} endet`:`Arbeitsaufnahme bei ${name(h.employer)}`}`);
 }
 for(const m of months) for(const f of m.market.firms) if(f.unit_price_cents!==f.previous_price_cents) add(m.month,`${name(f.id)}: Stückpreis ${money(f.previous_price_cents)} → ${money(f.unit_price_cents)}`);
 const wishKey=real?'desired_real_cents':'desired_cents',paidKey=real?'paid_real_cents':'paid_cents';
 const max=Math.max(100000,...months.flatMap(m=>m.households.map(h=>h[wishKey])));
 const ceiling=Math.ceil(max/50000)*50000;
 const lastMonth=latest?.month??1;
 const tickStep=lastMonth<=6?1:lastMonth<=12?2:4;
 const ticks=[...new Set([1,...Array.from({length:Math.floor(lastMonth/tickStep)},(_,i)=>(i+1)*tickStep),lastMonth])];
 const x=(month:number)=>54+(month-1)*450/Math.max(1,lastMonth-1),y=(cents:number)=>132-cents/ceiling*108;
 const points=(id:string,key:'desired_cents'|'paid_cents'|'desired_real_cents'|'paid_real_cents')=>months.map(m=>`${x(m.month)},${y(m.households.find(h=>h.id===id)![key])}`).join(' ');
 return <section className="consumption-history" aria-labelledby="consumption-title">
  <div className="consumption-heading"><div><div className="section-heading"><Activity size={18}/><h2 id="consumption-title">Konsum nach Haushalt</h2></div><p>Kaufpläne, bezahlte Ausgaben und gekaufte Warenmengen je abgeschlossenem Monat. Alle Haushaltsdiagramme verwenden dieselbe Skala.</p></div><div className="consumption-legend"><span><i className="wish-key"/>Konsumwunsch</span><span><i className="purchase-key"/>Tatsächliche Käufe</span><span><i className="event-key"/>Ereignis</span></div></div>
  {!selected?<p className="quiet">Nach dem ersten Monatsabschluss erscheinen die sechs Haushaltsverläufe. Ereignisse werden im Monat ihres Wirksamwerdens markiert.</p>:<>
   <div className="consumption-month-heading"><strong>Ausgewählter Monat: {selected.month} · {latest!.month} Monate abgeschlossen</strong>{chosen!==null&&<button onClick={()=>setChosen(null)}>Aktuellsten Monat anzeigen</button>}</div>
   <div className="consumption-months" role="group" aria-label="Monat für alle Haushalte auswählen">{months.map(m=><button key={m.month} aria-pressed={selected.month===m.month} aria-label={`Monat ${m.month}${events.has(m.month)?` · ${events.get(m.month)!.join('; ')}`:''}`} onClick={()=>setChosen(m.month)}><span>M{m.month}</span><i className={events.has(m.month)?'marked':''}/></button>)}</div>
   <div className="consumption-events"><strong>Ereignisse · Monat {selected.month}</strong>{events.has(selected.month)?<ul>{events.get(selected.month)!.map((e,i)=><li key={i}>{e}</li>)}</ul>:<p>Keine neue Szenario-, Zins- oder Beschäftigungsänderung in diesem Monat.</p>}</div>
   <PriceTransmission world={world} month={selected.month}/>
   <div className="consumption-mode" role="group" aria-label="Darstellung des Konsumverlaufs"><button aria-pressed={!real} onClick={()=>setReal(false)}>Ausgaben in Euro</button><button aria-pressed={real} onClick={()=>setReal(true)}>Warenmengen zu Startpreisen</button></div>
   <p className="consumption-mode-note">{real?'Warenmengen werden mit den unveränderten Startpreisen bewertet. So bleiben reale Mengenänderungen sichtbar, auch wenn Preise steigen. Der Wunsch zeigt ganze, zum damaligen Budget geplante Einheiten.':'Gestrichelt: gewünschtes Kaufbudget. Durchgezogen: tatsächlich bezahlte Ausgaben. Höhere Ausgaben können durch höhere Preise entstehen.'}</p>
   <div className="household-charts">{households.map(n=>{
    const h=selected.households.find(h=>h.id===n.id)!,previous=months.find(m=>m.month===selected.month-1)?.households.find(h=>h.id===n.id);
    const net=h.income_cents-h.tax_cents+h.prior_dividend_cents;
    const delta=previous?h[paidKey]-previous[paidKey]:null;
    return <article className="household-chart" key={n.id}><header><h3>{n.name}</h3><span>M{selected.month} · {name(h.employer)}</span></header>
     <svg viewBox="0 0 528 164" role="img" aria-label={`${n.name}: Konsumwunsch und Käufe über ${months.length} Monate; ${real?'Warenmengen zu Startpreisen':'Ausgaben'}; gemeinsame Skala 0 bis ${money(ceiling)}`}>
      {[0,0.5,1].map(f=><g key={f}><line x1="54" x2="504" y1={y(ceiling*f)} y2={y(ceiling*f)} className="consumption-grid"/><text x="47" y={y(ceiling*f)+4} textAnchor="end">{Math.round(ceiling*f/100).toLocaleString('de-DE')} €</text></g>)}
      {ticks.map(m=><text key={m} x={x(m)} y="153" textAnchor="middle">M{m}</text>)}
      {[...events.keys()].filter(m=>m<=latest!.month).map(m=><line key={m} x1={x(m)} x2={x(m)} y1="19" y2="132" className="consumption-event-line"><title>M{m}: {events.get(m)!.join('; ')}</title></line>)}
      <line x1={x(selected.month)} x2={x(selected.month)} y1="19" y2="132" className="consumption-selection"/>
      <polyline points={points(n.id,wishKey)} className="consumption-wish"/><polyline points={points(n.id,paidKey)} className="consumption-purchases"/>
      {months.map(m=>{const row=m.households.find(h=>h.id===n.id)!;return <g key={m.month}><circle cx={x(m.month)} cy={y(row[wishKey])} r="3" className="consumption-wish-dot"/><circle cx={x(m.month)} cy={y(row[paidKey])} r="3" className="consumption-paid-dot"/><title>Monat {m.month}: Wunsch {money(row[wishKey])}, Käufe {money(row[paidKey])}</title></g>;})}
     </svg>
     <div className="consumption-values"><div><span>{real?'Geplante Waren zu Startpreisen':'Konsumwunsch'}</span><strong>{money(h[wishKey])}</strong></div><div><span>{real?'Gekaufte Waren zu Startpreisen':'Tatsächliche Käufe'}</span><strong>{money(h[paidKey])}</strong></div></div>
     <dl className="consumption-breakdown consumption-goods">{h.goods.map(g=><div key={g.seller}><dt>{g.seller==='alltag'?'Alltagswaren':'Werkstattwaren'} gekauft</dt><dd>{g.paid_units} × {money(g.unit_price_cents)}</dd></div>)}<div><dt>Gekaufte Waren zu Startpreisen</dt><dd>{money(h.paid_real_cents)}</dd></div></dl>
     <p className="consumption-change">{delta===null?'Erster abgeschlossener Monat':delta===0?`${real?'Warenwert zu Startpreisen':'Ausgaben'} gegenüber dem Vormonat unverändert`:`${real?'Warenwert zu Startpreisen':'Ausgaben'} gegenüber dem Vormonat: ${delta>0?'+':''}${money(delta)}`}</p>
     <h4 className="consumption-gap-heading">Nicht ausgegebenes Kaufbudget · nominale Euro</h4><dl className="consumption-breakdown"><div><dt>Wegen Geldmangel nicht finanzierbar</dt><dd>{money(h.funding_gap_cents)}</dd></div><div><dt>Finanzierbar, aber Ware fehlt</dt><dd>{money(h.stock_gap_cents)}</dd></div><div><dt>Rest wegen ganzer Wareneinheiten</dt><dd>{money(h.unit_remainder_cents)}</dd></div></dl>
     <details><summary>Wie entsteht der Kaufplan in Monat {selected.month}?</summary><dl className="consumption-breakdown"><div><dt>Lohn und Transfers nach gezahlten Steuern</dt><dd>{money(h.income_cents-h.tax_cents)}</dd></div><div><dt>Ausschüttungen seit der letzten Kaufrunde</dt><dd>{money(h.prior_dividend_cents)}</dd></div><div><dt>Einkommensbasis des Kaufplans</dt><dd>{money(net)}</dd></div><div><dt>Kontoguthaben vor den Käufen</dt><dd>{money(h.cash_before_cents)}</dd></div><div><dt>Finanzierbares Kaufbudget</dt><dd>{money(h.funded_cents)}</dd></div></dl><p>Der Konsumwunsch beträgt {selected.consumption_percent} % der Einkommensbasis, mindestens {money(selected.essential_budget_cents)} Grundbedarfsplan. Guthaben begrenzt das Budget; Warenbestand und ganze Einheiten begrenzen die Käufe. Ausschüttungen beim Monatsabschluss fließen erst in die nächste Kaufrunde ein.</p></details>
    </article>;
   })}</div>
   <p className="consumption-model-note">Der Leitzins wirkt zunächst auf die Kredite der Betriebe und neue Staatskredite. Haushalte haben hier keine eigenen Kredite; mögliche Konsumfolgen entstehen über Löhne, Beschäftigung, Transfers oder Ausschüttungen. Eine Zinsänderung muss deshalb keinen sofortigen Konsumrückgang auslösen.</p>
  </>}
 </section>;
}
