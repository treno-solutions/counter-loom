import type {World} from './world-schema';
const money=(v:number)=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR'}).format(v/100);
export default function CapitalOrderView({world}:{world:World}) {
 const data=world.capital_orders,o=data.pending??data.history.at(-1),scale=world.parameters.goods_unit_scale??100;
 return <section className="capital-order-view"><h3>Maschinenauftrag und Lieferung</h3>
  {!o?<p>Noch kein Auftrag. Ein anhaltender Lieferengpass, vorhandenes Geld oberhalb des Betriebspuffers und verfügbare Beschäftigte begründen die Prüfung. Sparen der Haushalte allein löst keinen Maschinenkauf aus.</p>:<>
   <div className="capital-order-stages" aria-label="Ablauf des Maschinenauftrags"><div><span>1 · Auftrag finanziert</span><strong>{money(o.amount_cents)}</strong><small>Monat {o.placed_month} · Alltag bestellt bei Werkstatt. {o.delivery_month===null?'Der Betrag bleibt auf dem Käuferkonto gebunden.':'Der Kaufbetrag ist überwiesen.'}</small></div><b>→</b><div><span>2 · Teile produziert und reserviert</span><strong>{o.reserved_units.toLocaleString('de-DE')} / {o.units.toLocaleString('de-DE')}</strong><meter min={0} max={o.units} value={o.reserved_units} aria-label="Reservierte Teile"/><small>Entspricht {o.units/scale} ursprünglichen Wareneinheiten. Fehlende Teile gehen in die Produktionsplanung ein.</small></div><b>→</b><div><span>3 · Bezahlt und geliefert</span><strong>{o.delivery_month===null?'Ausstehend':`Monat ${o.delivery_month}`}</strong><small>{o.delivery_month===null?'Zusätzliche Kapazität noch nicht verfügbar.':`Kapazität ab Monat ${o.delivery_month+1}; Zahlungsbeleg ${o.transaction_id}.`}</small></div></div>
   <p>Preis je Teil bei Auftrag: {money(o.unit_price_cents)}. Keine Teilzahlung vor vollständiger Lieferung. Ein offener Auftrag verhindert eine weitere Bestellung.</p>
   {data.history.length>1&&<details><summary>{data.history.length} Maschinenaufträge im Verlauf</summary><ul>{data.history.map(r=><li key={r.id}>Auftrag {r.id}: M{r.placed_month} → {r.delivery_month===null?'noch offen':`M${r.delivery_month}`} · {money(r.amount_cents)}</li>)}</ul></details>}
  </>}
 </section>;
}
