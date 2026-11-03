import {useState} from 'react';
import type {World} from './world-schema';
const money=(v:number)=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:2}).format(v/100);
export default function StabilityMonitor({world}:{world:World}) {
 const [open,setOpen]=useState(false),rows=world.history;
 const span=Math.min(30,Math.floor((rows.length-1)/6)*6),last=rows.at(-1),first=span>=6?rows.at(-1-span):undefined;
 const state=world.nodes.find(n=>n.id==='staat')!,households=world.nodes.filter(n=>n.sector==='households');
 const target=world.parameters.essential_budget_cents*world.parameters.liquidity_reserve_months;
 const f0=world.public_finance.history.find(r=>r.month===first?.month),f1=world.public_finance.history.find(r=>r.month===last?.month);
 const governmentDrift=f0&&f1?((f1.closing_cash_cents-f1.closing_principal_cents)-(f0.closing_cash_cents-f0.closing_principal_cents))/span:null;
 const householdDrift=first&&last?(last.household_cash_cents-first.household_cash_cents)/span:null;
 return <div className="stability-monitor"><button className="macro-toggle" aria-expanded={open} onClick={()=>setOpen(!open)}>{open?'Liquiditätsziele und Kontodrift schliessen':'Liquiditätsziele und Kontodrift öffnen'}</button>
  {open&&<><div className="stability-numbers"><div><span>Liquiditätsziel je Haushalt</span><strong>{world.parameters.consumption_policy==='liquidity_target'?money(target):'Kein Ziel in dieser Regel'}</strong><small>{world.parameters.liquidity_reserve_months} Monate Grundbedarf · Anpassung über {world.parameters.liquidity_adjustment_months} Monate</small></div><div><span>Staat · Kasse minus Schuld</span><strong>{money(state.cash_cents-world.public_finance.outstanding_cents)}</strong><small>Schuld und Kasse gemeinsam beurteilen.</small></div><div><span>Staat · Veränderung pro Monat</span><strong>{governmentDrift===null?'Noch zu wenig Verlauf':money(governmentDrift)}</strong><small>{span>=6?`M${first!.month} bis M${last!.month} · Haushaltskonten: ${money(householdDrift!)} / Monat`:'Mindestens sieben Abschlüsse erforderlich.'}</small></div></div>
   <p>Diese kurze Verlaufskontrolle ist kein Langzeitnachweis. Eine positive Kasse kann gleichzeitig schrumpfen. Der Referenzlauf wird zusätzlich über längere Zeitfenster geprüft.</p>
   {world.parameters.consumption_policy==='liquidity_target'&&<><div className="household-reserve-bars">{households.map(h=><div key={h.id}><span>{h.name}</span><div className="reserve-bar" role="img" aria-label={`${h.name}: ${money(h.cash_cents)}, Ziel ${money(target)}`}><i style={{width:`${Math.min(100,h.cash_cents/Math.max(1,target)*100)}%`}}/></div><strong>{money(h.cash_cents)}</strong><small>{h.cash_cents>=target?`${money(h.cash_cents-target)} über Ziel`:`${money(target-h.cash_cents)} bis zum Ziel`}</small></div>)}</div><p>Der Kaufplan verwendet die Einkommensbasis plus einen Anteil der Abweichung des Monatsanfangsguthabens vom Ziel. Mehr Guthaben kann den Kaufplan erhöhen, zu wenig Guthaben kann ihn senken. Grundbedarf, verfügbare Ware und Geld begrenzen die tatsächlichen Käufe.</p></>}
  </>}
 </div>;
}
