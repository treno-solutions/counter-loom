import { useState } from 'react';
import { ArrowDownLeft, ArrowUpRight, ChevronDown, CircleHelp, ShieldCheck, Wallet } from 'lucide-react';
import GovernmentFinance from './GovernmentFinance';
import type { SectorId, World } from './world-schema';

const euro = (value: number) => new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: value % 100 ? 2 : 0 }).format(value / 100);
const signed = (value: number) => `${value > 0 ? '+' : ''}${euro(value)}`;
const sectors: SectorId[] = ['households', 'firms', 'government', 'external'];
const names: Record<SectorId, string> = { households: 'Haushalte', firms: 'Unternehmen', government: 'Staat', bank: 'Finanzsektor', external: 'Ausland' };
const kinds: Record<string, string> = { wage: 'Löhne', public_wage_arrears:'Nachzahlungen öffentlicher Löhne', arrears_income_tax:'Steuer auf Lohnnachzahlungen', income_tax: 'Lohnsteuer', profit_tax: 'Gewinnsteuer', company_dividend: 'Reguläre Gewinnausschüttungen', company_extra_dividend:'Zusätzliche Gewinnausschüttungen', transfer: 'Transfers', procurement: 'Öffentliche Aufträge', consumption: 'Einkäufe', dividend: 'Zinsausschüttungen', energy: 'Energieimporte', export_sale: 'Warenexporte', government_credit: 'Staatskredit · Finanzierung', government_interest: 'Zinsen Staatskredit', government_principal: 'Staatliche Kredittilgung', interest: 'Kreditzinsen', investment: 'Anlagenkäufe', machine_credit: 'Neues Kreditguthaben', machine_purchase: 'Kreditfinanzierte Maschine', machine_interest: 'Zinsen Maschinenkredit', machine_principal: 'Tilgung Maschinenkredit' };
const sum = (values: number[]) => values.reduce((a, b) => a + b, 0);

function account(world: World, ids: string[]) {
  const members = new Set(ids);
  const incoming = world.transactions.filter(t => members.has(t.target) && !members.has(t.source));
  const outgoing = world.transactions.filter(t => members.has(t.source) && !members.has(t.target));
  const rows = (direction: 'incoming' | 'outgoing') => {
    const grouped = new Map<string, { label: string; party: string; amount: number }>();
    for (const t of direction === 'incoming' ? incoming : outgoing) {
      const partyId = direction === 'incoming' ? t.source : t.target;
      const party = names[world.nodes.find(n => n.id === partyId)!.sector];
      const key = `${t.kind}-${party}`;
      const row = grouped.get(key) ?? { label: kinds[t.kind] ?? t.label, party, amount: 0 };
      row.amount += t.amount_cents;
      grouped.set(key, row);
    }
    return [...grouped.values()];
  };
  return { opening: sum(ids.map(id => world.month_open[id] ?? 0)), closing: sum(world.nodes.filter(n => members.has(n.id)).map(n => n.cash_cents)), income: sum(incoming.map(t => t.amount_cents)), spending: sum(outgoing.map(t => t.amount_cents)), incomingRows: rows('incoming'), outgoingRows: rows('outgoing') };
}

export function CashAccount({ world, ids, title = 'Kontobewegungen' }: { world: World; ids: string[]; title?: string }) {
  const data = account(world, ids);
  return <section className="cash-account" aria-label={title}>
    <div className="account-heading"><Wallet size={18} /><div><h3>{title}</h3><p>Monat {world.month} · {world.phase === 4 ? 'abgeschlossen' : world.month ? 'bisher verbucht, Monat noch offen' : 'noch nicht gestartet'}</p></div></div>
    <div className="cash-equation"><div><span>Am Monatsbeginn</span><strong>{euro(data.opening)}</strong></div><b>+</b><div className="cash-plus"><span>Eingegangen</span><strong>{euro(data.income)}</strong></div><b>−</b><div className="cash-minus"><span>Ausgegeben</span><strong>{euro(data.spending)}</strong></div><b>=</b><div><span>Jetzt auf dem Konto</span><strong>{euro(data.closing)}</strong></div></div>
    <div className="cash-sides"><div><h4><ArrowDownLeft size={16} />Einzahlungen nach Herkunft</h4>{data.incomingRows.length ? data.incomingRows.map(r => <div className="cash-row" key={r.label + r.party}><div><strong>{r.label}</strong><small>von {r.party}</small></div><span>+{euro(r.amount)}</span></div>) : <p className="cash-empty">Noch keine Eingänge in diesem Monat.</p>}</div><div><h4><ArrowUpRight size={16} />Auszahlungen nach Empfänger</h4>{data.outgoingRows.length ? data.outgoingRows.map(r => <div className="cash-row" key={r.label + r.party}><div><strong>{r.label}</strong><small>an {r.party}</small></div><span>−{euro(r.amount)}</span></div>) : <p className="cash-empty">Noch keine Ausgänge in diesem Monat.</p>}</div></div>
  </section>;
}

export function MoneyOrigin({ world }: { world: World }) {
  const [expanded, setExpanded] = useState(false);
  const changes = sectors.map(sector => {
    const nodes = world.nodes.filter(n => n.sector === sector);
    const opening = sum(nodes.map(n => world.initial_balances[n.id] ?? 0));
    const now = sum(nodes.map(n => n.cash_cents));
    return { sector, opening, now, delta: now - opening };
  });
  const domestic=changes.filter(r=>r.sector!=='external');
  return <section className="money-origin" aria-label="Herkunft und Verteilung der Zahlungsmittel">
    <div className="origin-intro"><ShieldCheck size={20} /><div><h2>Guthaben im Inland und Ausland</h2><p>Energieimporte verringern das Inlandsguthaben, bezahlte Warenexporte erhöhen es. Die folgenden Bestände enthalten außerdem die Auswirkungen von Kreditaufnahme, Tilgung und Bankzinsen.</p></div><button onClick={() => setExpanded(!expanded)} aria-expanded={expanded}>Geldbestände und Änderungen <ChevronDown size={15} /></button></div>
    <div className="sector-changes" aria-label="Aktuelle Kundenguthaben mit Veränderung seit Start">{changes.map(row => <span key={row.sector} className={row.delta < 0 ? 'decreased' : row.delta > 0 ? 'increased' : ''}><small>{row.sector==='external'?'Auslandskonto':names[row.sector]} · aktuell</small><strong>{euro(row.now)}</strong><span className="sector-delta">{signed(row.delta)} seit Start</span></span>)}<span className="change-total"><small>Inland · zusammen</small><strong>{euro(sum(domestic.map(r=>r.now)))}</strong><span className="sector-delta">{signed(sum(domestic.map(r => r.delta)))} seit Start</span></span></div>
    {expanded && <div className="origin-detail"><p>Inlandsguthaben + Auslandskonto = <strong>{euro(world.audit.current_money_cents)}</strong> auf allen Kundenkonten des Modells. Energieimporte und Warenexporte verschieben Geld zwischen diesen Konten. Importzahlungen senken das Inlandsguthaben, Exporterlöse erhöhen es.</p><div className="money-bridge"><span>Anfangseinlagen <b>{euro(world.banking.initial_deposits_cents)}</b></span><span>+ neue Kredite <b>{euro(world.banking.credit_created_cents)}</b></span><span>− Tilgung <b>{euro(world.banking.principal_repaid_cents)}</b></span><span>− Bankerträge <b>{euro(world.banking.interest_received_cents)}</b></span><span>+ Bankausschüttungen <b>{euro(world.banking.distributed_cents)}</b></span><span>= alle Kundenkonten inkl. Ausland <b>{euro(world.audit.current_money_cents)}</b></span></div><div className="account-table-scroll"><table><caption>Alle Kundenkonten einschließlich Auslandskonto. Die 10.000 € Bankeigenkapital und die Bankreserven werden nicht hinzuaddiert.</caption><thead><tr><th>System</th><th>Anfangsbestand</th><th>Aktueller Bestand</th><th>Änderung seit Start</th></tr></thead><tbody>{changes.map(r => <tr key={r.sector}><th>{names[r.sector]}</th><td>{euro(r.opening)}</td><td>{euro(r.now)}</td><td>{signed(r.delta)}</td></tr>)}</tbody></table></div><p><CircleHelp size={15} />Neue Bankkredite erhöhen die Summe aller Kundenkonten, Tilgungen verringern sie. Zinszahlungen an die Bank senken sie ebenfalls; Bankausschüttungen führen Geld zurück. Eine Gewinnausschüttung von Unternehmen an Haushalte verteilt vorhandenes Geld innerhalb des Inlands.</p></div>}
  </section>;
}

export function GovernmentBudget({world,running=false}:{world:World;running?:boolean}) {
  return <GovernmentFinance world={world} running={running}><CashAccount world={world} ids={['staat']} title="Staatskasse · Geldherkunft und Verwendung"/></GovernmentFinance>;
}

export function HouseholdPlan({ world, id }: { world: World; id: string }) {
  const node = world.nodes.find(n => n.id === id)!;
  return <section className="household-plan"><div><CircleHelp size={19} /><h3>Konsumbudget und vorhandenes Guthaben</h3></div><p>Der monatliche Grundbedarfsplan beträgt im Test <strong>{euro(world.parameters.essential_budget_cents)}</strong>. Vorhandenes Kontoguthaben kann diesen Grundbedarf finanzieren. Bei höherem Einkommen kann der Kaufplan darüber liegen. Jeder bezahlte Kauf verringert das Haushaltsguthaben und erhöht das Guthaben des verkaufenden Betriebs.</p>{world.phase >= 2 ? <div className="plan-numbers"><span>Kurzarbeitsleistung · dieser Monat<strong>{euro(node.metrics.short_time)}</strong></span><span>Kaufplan<strong>{euro(node.metrics.consumption_plan)}</strong></span><span>Aus dem Konto finanzierbar<strong>{euro(node.metrics.consumption_budget)}</strong></span><span>Tatsächlich gekauft<strong>{euro(node.metrics.consumption_paid)}</strong></span><span>Davon aus älterem Kontoguthaben<strong>{euro(node.metrics.reserve_used)}</strong></span></div> : <p className="cash-empty">Die Einkaufsphase dieses Monats steht noch aus.</p>}<small>Güter werden in ganzen Einheiten verkauft. Fehlende Ware und die Rundung auf ganze Einheiten können die bezahlten Käufe begrenzen. Ein unerfüllter Kaufplan ist keine gebuchte Schuld.</small></section>;
}
