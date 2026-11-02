import { useState } from 'react';
import { ArrowDownLeft, ArrowUpRight, ChevronDown, CircleHelp, Landmark, ShieldCheck, Wallet } from 'lucide-react';
import type { SectorId, World } from './world-schema';

const euro = (value: number) => new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: value % 100 ? 2 : 0 }).format(value / 100);
const signed = (value: number) => `${value > 0 ? '+' : ''}${euro(value)}`;
const sectors: SectorId[] = ['households', 'firms', 'government', 'bank', 'external'];
const names: Record<SectorId, string> = { households: 'Haushalte', firms: 'Unternehmen', government: 'Staat', bank: 'Finanzsektor', external: 'Ausland · Energie' };
const kinds: Record<string, string> = { wage: 'Löhne', income_tax: 'Lohnsteuer', profit_tax: 'Überschusssteuer', transfer: 'Transfers', procurement: 'Öffentliche Aufträge', consumption: 'Einkäufe', dividend: 'Zinsausschüttungen', energy: 'Energieimporte', interest: 'Kreditzinsen', investment: 'Anlagenkäufe' };
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

export function CashAccount({ world, ids, title = 'Woher kommt das Geld?' }: { world: World; ids: string[]; title?: string }) {
  const data = account(world, ids);
  return <section className="cash-account" aria-label={title}>
    <div className="account-heading"><Wallet size={18} /><div><h3>{title}</h3><p>Monat {world.month} · {world.phase === 4 ? 'abgeschlossen' : world.month ? 'bisher verbucht, Monat noch offen' : 'noch nicht gestartet'}</p></div></div>
    <div className="cash-equation"><div><span>Am Monatsbeginn</span><strong>{euro(data.opening)}</strong></div><b>+</b><div className="cash-plus"><span>Eingegangen</span><strong>{euro(data.income)}</strong></div><b>−</b><div className="cash-minus"><span>Ausgegeben</span><strong>{euro(data.spending)}</strong></div><b>=</b><div><span>Jetzt auf dem Konto</span><strong>{euro(data.closing)}</strong></div></div>
    <div className="cash-sides"><div><h4><ArrowDownLeft size={16} />Von wem kam das Geld?</h4>{data.incomingRows.length ? data.incomingRows.map(r => <div className="cash-row" key={r.label + r.party}><div><strong>{r.label}</strong><small>von {r.party}</small></div><span>+{euro(r.amount)}</span></div>) : <p className="cash-empty">Noch keine Eingänge in diesem Monat.</p>}</div><div><h4><ArrowUpRight size={16} />An wen ging es weiter?</h4>{data.outgoingRows.length ? data.outgoingRows.map(r => <div className="cash-row" key={r.label + r.party}><div><strong>{r.label}</strong><small>an {r.party}</small></div><span>−{euro(r.amount)}</span></div>) : <p className="cash-empty">Noch keine Ausgänge in diesem Monat.</p>}</div></div>
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
  return <section className="money-origin" aria-label="Herkunft und Verteilung der Zahlungsmittel">
    <div className="origin-intro"><ShieldCheck size={20} /><div><h2>Das Geld wechselt die Konten.</h2><p>Die Welt startet mit <strong>{euro(world.audit.total_money_cents)}</strong>. Löhne und Einkäufe sind Umbuchungen zwischen diesen Konten. Zusätzliche Geldschöpfung ist in diesem Ausschnitt nicht modelliert.</p></div><button onClick={() => setExpanded(!expanded)} aria-expanded={expanded}>Verteilung seit Start <ChevronDown size={15} /></button></div>
    <div className="sector-changes">{changes.map(row => <span key={row.sector} className={row.delta < 0 ? 'decreased' : row.delta > 0 ? 'increased' : ''}><small>{names[row.sector]}</small><strong>{signed(row.delta)}</strong></span>)}<span className="change-total"><small>Summe der Änderungen</small><strong>{signed(sum(changes.map(r => r.delta)))}</strong></span></div>
    {expanded && <div className="origin-detail"><div className="account-table-scroll"><table><caption>Alle Konten, einschließlich des vereinfachten Auslandskontos. Geldbestände, keine vollständigen Vermögensbilanzen.</caption><thead><tr><th>System</th><th>Anfangsbestand</th><th>Aktueller Bestand</th><th>Änderung seit Start</th></tr></thead><tbody>{changes.map(r => <tr key={r.sector}><th>{names[r.sector]}</th><td>{euro(r.opening)}</td><td>{euro(r.now)}</td><td>{signed(r.delta)}</td></tr>)}</tbody></table></div><p><CircleHelp size={15} />Steigt ein Kontenbestand, muss die Summe der anderen Bestände entsprechend sinken. Das Auslandskonto enthält Energiezahlungen; ein Rückfluss durch Exportnachfrage ist noch nicht modelliert.</p></div>}
  </section>;
}

export function GovernmentBudget({ world }: { world: World }) {
  const state = world.nodes.find(n => n.id === 'staat')!;
  const data = account(world, ['staat']);
  const gap = data.spending - data.income;
  const initial = world.initial_balances.staat ?? 0;
  const remaining = initial ? Math.min(100, state.cash_cents / initial * 100) : 0;
  const last = world.history.at(-1);
  const previous = world.history.at(-2)?.government_cash_cents ?? initial;
  const lastGap = last ? previous - last.government_cash_cents : 0;
  const months = lastGap > 0 ? state.cash_cents / lastGap : null;
  return <section className="government-budget" aria-label="Staatshaushalt und Finanzierung">
    <div className="fiscal-title"><Landmark size={25} /><div><h2>Was bezahlt der Staat — und womit?</h2><p>Steuern sind Einnahmen. Öffentliche Löhne, Transfers und Aufträge sind Ausgaben. Ein verbleibender Fehlbetrag wird hier aus dem vorhandenen Staatskonto bezahlt.</p></div></div>
    <CashAccount world={world} ids={['staat']} title="Einnahmen und Ausgaben des Staates" />
    <div className="fiscal-financing"><div><span className="overline">FINANZIERUNG · LAUFENDER MONAT</span><h3>{gap > 0 ? 'Der Staat greift auf vorhandenes Geld zurück.' : gap < 0 ? 'Die Eingänge übersteigen bisher die Ausgaben.' : 'Eingänge und Ausgänge sind bisher ausgeglichen.'}</h3><div className="fiscal-gap"><span>{gap > 0 ? 'Bisheriger Fehlbetrag' : gap < 0 ? 'Bisheriger Überschuss' : 'Saldo'}</span><strong>{euro(Math.abs(gap))}</strong></div><p>{gap > 0 ? 'Dieser Betrag ist die Abnahme des Kontos gegenüber dem Monatsbeginn. Er wurde nicht neu erzeugt.' : 'Der Kontenbestand ergibt sich aus dem Monatsanfang und den tatsächlich verbuchten Zahlungen.'} {world.phase !== 4 && 'Der Monat ist noch nicht abgeschlossen; spätere Steuerzahlungen oder Ausgaben können den Saldo ändern.'}</p><div className="debt-scope"><span>Neue Staatsanleihen / Kredite</span><strong>Noch nicht modelliert</strong></div></div><div className="reserve-card"><span className="overline">VERFÜGBARER PUFFER</span><strong>{euro(state.cash_cents)}</strong><div className="reserve-track"><span style={{ width: `${remaining}%` }} /></div><p>{new Intl.NumberFormat('de-DE', { maximumFractionDigits: 1 }).format(remaining)} % des Anfangskontos von {euro(initial)} sind noch vorhanden.</p>{months !== null && <p className="runway">Bei einem unveränderten Fehlbetrag wie im letzten abgeschlossenen Monat: rechnerisch noch <b>{new Intl.NumberFormat('de-DE', { maximumFractionDigits: 1 }).format(months)} Monate</b>. Diese Fortschreibung hält den Saldo konstant; der tatsächliche weitere Verlauf kann abweichen.</p>}<p>Bei fehlendem Geld werden Zahlungen begrenzt. Das ist ein endlicher Staatskassen-Test, keine vollständige staatliche Schuldenfinanzierung.</p></div></div>
  </section>;
}

export function HouseholdPlan({ world, id }: { world: World; id: string }) {
  const node = world.nodes.find(n => n.id === id)!;
  return <section className="household-plan"><div><CircleHelp size={19} /><h3>Leben auch ohne neues Einkommen</h3></div><p>Der monatliche Grundbedarfsplan beträgt im Test <strong>{euro(world.parameters.essential_budget_cents)}</strong>. Er darf aus vorhandenem Kontoguthaben bezahlt werden. Darüber gilt der einkommensabhängige Kaufplan. Jeder Kauf bezahlt ein Unternehmen und belastet dieses Haushaltskonto.</p>{world.phase >= 2 ? <div className="plan-numbers"><span>Kaufplan<strong>{euro(node.metrics.consumption_plan)}</strong></span><span>Aus dem Konto finanzierbar<strong>{euro(node.metrics.consumption_budget)}</strong></span><span>Tatsächlich gekauft<strong>{euro(node.metrics.consumption_paid)}</strong></span><span>Davon aus älterem Kontoguthaben<strong>{euro(node.metrics.reserve_used)}</strong></span></div> : <p className="cash-empty">Die Einkaufsphase dieses Monats steht noch aus.</p>}<small>Güter werden in ganzen Einheiten verkauft. Lagerengpässe und Rundung können Käufe unter das finanzierbare Budget drücken. Ein unerfüllter Kaufplan ist keine gebuchte Schuld.</small></section>;
}
