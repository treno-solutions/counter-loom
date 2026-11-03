import { useState } from 'react';
import { ArrowRight, Factory, Landmark, Users } from 'lucide-react';
import { ComparisonSchema, type Comparison, type CrisisConfig, type World } from './world-schema';
const money=(c:number)=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:c%100?2:0}).format(c/100);
const firmName=(id:string)=>id==='both'?'Beide Betriebe':id==='alltag'?'Alltag & Versorgung':'Werkstatt & Technik';

export default function CrisisPanel({world,busy,onClosure}:{world:World;busy:boolean;onClosure:(c:CrisisConfig)=>void}) {
 const [firm,setFirm]=useState<CrisisConfig['firm']>('werkstatt'),[duration,setDuration]=useState(3),[withSupport,setSupport]=useState(true);
 const [comparing,setComparing]=useState(false),[result,setResult]=useState<Comparison|null>(null),[error,setError]=useState('');
 const blocked=busy||comparing||!!world.crisis.pending||world.crisis.closed_firms.length>0||world.completed;
 async function compare(){
  setComparing(true);setError('');
  try{
   const response=await fetch('/api/world/compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({world_id:world.world_id,revision:world.revision,firm,duration,replacement_bps:6000})});
   const data=await response.json();if(!response.ok)throw Error(data.error??'Vergleich fehlgeschlagen.');
   const parsed=ComparisonSchema.safeParse(data);if(!parsed.success)throw Error('Der Vergleich enthält unvollständige Daten. Bitte die Seite neu laden und einen neuen Vergleich starten.');setResult(parsed.data);
  }catch(e){setError(e instanceof Error?e.message:'Vergleich nicht verfügbar.');}finally{setComparing(false);}
 }
 return <div className="crisis-controls">
  <div><h3>Befristete Betriebsschliessung</h3><p>Ab dem nächsten Monat: keine Produktion und keine Verkäufe im gewählten Betrieb. Arbeitsverträge bleiben erhalten. Nach Ablauf wird der vorherige Arbeitszeitplan freigegeben.</p></div>
  <div className="crisis-form"><label>Betroffener Betrieb<select value={firm} onChange={e=>setFirm(e.target.value as CrisisConfig['firm'])} disabled={blocked}><option value="werkstatt">Werkstatt & Technik</option><option value="alltag">Alltag & Versorgung</option><option value="both">Beide Betriebe</option></select></label><label>Dauer · Monate<input type="number" min="1" max="12" step="1" value={duration} onChange={e=>setDuration(Number(e.target.value))} disabled={blocked}/></label><label className="crisis-check"><input type="checkbox" checked={withSupport} onChange={e=>setSupport(e.target.checked)} disabled={blocked}/>Mit Kurzarbeitsleistung · 60 % des Referenz-Nettoeinkommens</label></div>
  <p className="crisis-assumption">Eigene Modellannahmen: Netto-Arbeitszeitlohn vor Schliessung als feste Referenz, Leistung steuerfrei und nur soweit finanzierbar. Kein Lohn für ausgefallene Arbeit. Je geschlossenem Betrieb fallen monatlich 300 € Erhaltungsenergie an; Zahlung an das Auslandskonto. Keine Nachholung ausgefallener Käufe.</p>
  <div className="crisis-actions"><button disabled={blocked||!Number.isInteger(duration)||duration<1||duration>12} onClick={()=>onClosure({firm,duration,replacement_bps:withSupport?6000:0})}>Schliessung {withSupport?'mit':'ohne'} Kurzarbeit vormerken</button><button disabled={blocked||!Number.isInteger(duration)||duration<1||duration>12} onClick={()=>void compare()}>{comparing?'Beide Varianten werden berechnet …':'Mit / ohne Kurzarbeit vergleichen'}</button></div>
  {busy&&<p>Für einen neuen Krisenvergleich die Simulation pausieren und den laufenden Schritt abschliessen lassen.</p>}
  {world.crisis.pending&&<p role="status">Vorgemerkt: {firmName(world.crisis.pending.firm)} · {world.crisis.pending.duration} Monate · Ersatzquote {world.crisis.pending.replacement_bps/100} %.</p>}
  {world.crisis.closed_firms.length>0&&<p>Eine Schliessung läuft bereits. Eine weitere kann nach ihrer Aufhebung vorgemerkt werden.</p>}
  {error&&<p role="alert">{error}</p>}
  {result&&<ComparisonView key={`${result.source_world_id}-${result.source_revision}-${result.firm}-${result.duration}`} result={result} currentRevision={world.revision}/>}
 </div>;
}

function ComparisonView({result,currentRevision}:{result:Comparison;currentRevision:number}) {
 const without=result.branches[0]!,withSupport=result.branches[1]!;
 const metrics=[['household_net_cents','Haushalte · Netto-Lohn und Transfers'],['consumption_cents','Haushalte · tatsächliche Käufe'],['household_cash_cents','Haushalte · Kontoguthaben'],['firm_cash_cents','Unternehmen · Kontoguthaben'],['government_cash_cents','Staat · Kasse'],['government_debt_cents','Staat · Bankschuld']] as const;
 const [selected,setSelected]=useState(result.end_month);
 const row0=without.rows.find(r=>r.month===selected)??without.rows.at(-1)!,row1=withSupport.rows.find(r=>r.month===selected)??withSupport.rows.at(-1)!;
 const x=(m:number)=>56+(m-result.start_month)*384/Math.max(1,result.end_month-result.start_month);
 function download(){const url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`counterloom-closure-comparison-m${result.start_month}.json`;a.click();URL.revokeObjectURL(url);}
 return <section className="crisis-comparison" aria-label="Vergleich mit und ohne Kurzarbeit"><h3>Gleiche Schliessung, zwei Fortsetzungen</h3><p>{firmName(result.firm)} · geschlossen M{result.start_month}–M{result.start_month+result.duration-1}, danach sechs Monate Nachbeobachtung. Beide Varianten beginnen im selben bestätigten Weltzustand; sie verändern den laufenden Versuch nicht.</p><p className="comparison-legend"><span className="without-support">Gestrichelt: ohne Kurzarbeit</span><span className="with-support">Durchgezogen: 60 % Ersatz</span><span>Hinterlegt: Schliessungszeitraum</span></p>{currentRevision!==result.source_revision&&<p className="crisis-note">Gespeicherter Vergleich ab Revision {result.source_revision}. Der laufende Versuch wurde seitdem verändert; der Vergleich wird nicht automatisch neu berechnet.</p>}
 <div className="crisis-chart-grid">{metrics.map(([key,title])=>{
  const max=Math.max(10000,...result.branches.flatMap(b=>b.rows.map(r=>r[key]))),top=Math.ceil(max/10000)*10000;
  const y=(v:number)=>133-v/top*108;
  return <figure key={key}><figcaption>{title}</figcaption><svg viewBox="0 0 462 166" role="img" aria-label={`${title}: ohne und mit Kurzarbeit, gemeinsame Skala 0 bis ${money(top)}`}><rect x="56" y="22" width={x(result.start_month+result.duration)-56} height="111" className="closure-band"/>{[0,0.5,1].map(f=><g key={f}><line x1="56" x2="440" y1={y(top*f)} y2={y(top*f)} className="consumption-grid"/><text x="50" y={y(top*f)+4} textAnchor="end">{Math.round(top*f/100).toLocaleString('de-DE')}</text></g>)}{result.branches.map((b,i)=><polyline key={i} points={b.rows.map(r=>`${x(r.month)},${y(r[key])}`).join(' ')} className={i?'compare-supported':'compare-unsupported'}/>)}{[result.start_month,result.start_month+result.duration,result.end_month].map(m=><text key={m} x={x(m)} y="156" textAnchor="middle">M{m}</text>)}<line x1={x(row0.month)} x2={x(row0.month)} y1="22" y2="133" className="consumption-selection"/></svg><p>Ohne: <strong>{money(row0[key])}</strong> · Mit: <strong>{money(row1[key])}</strong><br/>Differenz mit − ohne: {money(row1[key]-row0[key])}</p></figure>;
 })}</div>
 <label className="comparison-month">Werte für Monat<select value={row0.month} onChange={e=>setSelected(Number(e.target.value))}>{without.rows.map(r=><option key={r.month} value={r.month}>Monat {r.month}{r.closed?' · geschlossen':''}</option>)}</select></label><div className="crisis-table-scroll"><table><caption>Weitere Ergebnisse · Monat {row0.month}</caption><thead><tr><th>Grösse</th><th>Ohne Kurzarbeit</th><th>Mit Kurzarbeit</th></tr></thead><tbody><tr><th>Arbeitsverträge gesamt</th><td>{row0.employment}</td><td>{row1.employment}</td></tr><tr><th>Produzierte Einheiten gesamt</th><td>{row0.production_units}</td><td>{row1.production_units}</td></tr><tr><th>Kurzarbeitsleistung · Monatszahlung</th><td>{money(row0.short_time_cents)}</td><td>{money(row1.short_time_cents)}</td></tr><tr><th>Kurzarbeitsleistung · ganzer Vergleich</th><td>{money(without.total_short_time_cents)}</td><td>{money(withSupport.total_short_time_cents)}</td></tr></tbody></table></div><p>Das ist ein kontrollierter Vergleich innerhalb unserer Modellregeln. Während der Schliessung bleiben Verträge in beiden Varianten erhalten; Unterschiede nach Wiederöffnung entstehen aus Einkommen, Käufen und Finanzierung. Kein Nachweis realer Corona-Wirkungen.</p><button onClick={download}>Vergleich als JSON exportieren</button>
 </section>;
}

export function CrisisImpact({world}:{world:World}) {
 const c=world.crisis,e=c.episodes.at(-1);if(!e&&!c.pending)return null;
 if(c.pending)return <section className="crisis-impact" aria-label="Betriebsschliessung vorgemerkt"><h2>Schliessung vorgemerkt</h2><p>{firmName(c.pending.firm)} · {c.pending.duration} Monate ab Monat {world.month+1} · Ersatzquote {c.pending.replacement_bps/100} %. Der aktuelle Monat wird nach den bisherigen Regeln abgeschlossen.</p></section>;
 const active=c.closed_firms.length>0,households=world.nodes.filter(n=>n.sector==='households');
 const affected=e?households.filter(h=>e.workers.some(w=>w.id===h.id)):[];
 const wages=affected.reduce((s,h)=>s+h.metrics.income-h.metrics.transfers,0),tax=affected.reduce((s,h)=>s+h.metrics.tax,0);
 return <section className="crisis-impact" aria-label="Betriebsschliessung und Einkommensersatz"><header><h2>{c.pending?'Schliessung vorgemerkt':active?'Befristete Betriebsschliessung':'Schliessung beendet · Nachwirkungen beobachten'}</h2>{e&&<span>M{e.start_month}–M{e.end_month} · Ersatzquote {e.replacement_bps/100} %</span>}</header><div className="crisis-flow"><div><Factory size={20}/><h3>Betriebe</h3><strong>{active?'Produktion & Verkauf gesperrt':'Betrieb freigegeben'}</strong><p>{e?.firms.map(firmName).join(', ')??firmName(c.pending!.firm)}</p><small>Arbeitsverträge bleiben erhalten. Laufende Zinsen und Erhaltungsenergie belasten die Firmenkasse.</small></div><ArrowRight/><div><Users size={20}/><h3>Betroffene Haushalte · Monat {world.month}</h3><strong>{money(wages-tax+c.monthly_paid_cents)}</strong><p>Lohn nach gezahlter Steuer + Kurzarbeitsleistung</p><small>Leistung: {money(c.monthly_paid_cents)} bezahlt / {money(c.monthly_due_cents)} vorgesehen. Vor den Phasen für Lohn und Transfer sind Zahlungen noch unvollständig.</small></div><ArrowRight/><div><Landmark size={20}/><h3>Staat · Monat {world.month}</h3><strong>{money(c.monthly_paid_cents)}</strong><p>Tatsächlich gezahlte Kurzarbeitsleistung</p><small>Kasse: {money(world.nodes.find(n=>n.id==='staat')!.cash_cents)} · Bankschuld: {money(world.public_finance.outstanding_cents)}. Fehlende Leistung bleibt als Verpflichtung sichtbar: {money(c.unpaid_cents)}.</small></div></div><p>Die Pfeile zeigen den Wirkungszusammenhang. Tatsächliche Zahlungen stehen in der Systemkarte und in den Kontobewegungen. Mehr Einkommen ermöglicht während einer Verkaufssperre nicht automatisch mehr Käufe.</p></section>;
}
