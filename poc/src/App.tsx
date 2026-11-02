import { useEffect, useRef, useState } from 'react';
import { Activity, ArrowLeft, ArrowRight, ArrowUpRight, Check, ChevronDown, CircleHelp, CirclePause, CirclePlay, Coins, GitBranch, Landmark, Layers3, LoaderCircle, RotateCcw, ShieldCheck, Wallet, X } from 'lucide-react';
import { ResultSchema, type CaseId, type Result, type Row } from './schema';

const euros = (value: number): string => new Intl.NumberFormat('de-DE', {style: 'currency', currency: 'EUR', maximumFractionDigits: 0}).format(value);
const percent = (value: number): string => new Intl.NumberFormat('de-DE', {style: 'percent', maximumFractionDigits: 2}).format(value);
const signed = (value: number): string => `${value > 0 ? '+' : ''}${euros(value)}`;
const labels: Record<CaseId, {title: string; subtitle: string; icon: typeof Wallet}> = {
  variable_loan: {title: 'Variabler Kredit', subtitle: '60.000 € · Zinssatz veränderlich', icon: Landmark},
  fixed_loan: {title: 'Festzinskredit', subtitle: '60.000 € · 2 % fest vereinbart', icon: ShieldCheck},
  deposit: {title: 'Verzinste Einlage', subtitle: '60.000 € · Zinssatz veränderlich', icon: Coins},
};
const lookup = (rows: Row[], id: CaseId, period: number): Row | undefined => rows.find(row => row.case === id && row.period === period);

function TraceChart({rows, baseline, id, period}: {rows: Row[]; baseline: Row[]; id: CaseId; period: number}) {
  const host = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(600);
  useEffect(() => {
    const observer = new ResizeObserver(entries => { const size = entries[0]?.contentRect.width; if (size) setWidth(Math.max(250, size)); });
    if (host.current) observer.observe(host.current);
    return () => observer.disconnect();
  }, []);
  const selected = rows.filter(row => row.case === id);
  const control = baseline.filter(row => row.case === id);
  const values = [1000, ...selected.map(row => row.cash_close), ...control.map(row => row.cash_close)];
  const low = Math.max(0, Math.floor((Math.min(...values) - 200) / 500) * 500);
  const high = Math.max(low + 1000, Math.ceil((Math.max(...values) + 200) / 500) * 500);
  const left = 66, right = width - 18, top = 15, bottom = 166;
  const x = (month: number) => left + (month / 6) * (right - left);
  const y = (cash: number) => bottom - ((cash - low) / (high - low)) * (bottom - top);
  const path = (series: Row[]) => [1000, ...series.map(row => row.cash_close)].map((value, index) => `${x(index)},${y(value)}`).join(' ');
  const chosen = lookup(rows, id, period);
  return <div ref={host} className="trace-chart">
    <svg width="100%" height="210" viewBox={`0 0 ${width} 210`} role="img" aria-label="Verfügbares Geld über sechs Monate: berechnete Variante und unveränderter Vergleich. Die Startreserve beträgt 1.000 Euro.">
      {[0, 1, 2, 3].map(i => {const value = low + ((high - low) * i) / 3; return <g key={i}><line x1={left} x2={right} y1={y(value)} y2={y(value)} className="chart-grid"/><text x={left - 10} y={y(value) + 4} textAnchor="end" className="chart-label">{Math.round(value).toLocaleString('de-DE')}</text></g>;})}
      <text x="8" y="11" className="chart-label">EUR</text>
      <line x1={x(2)} x2={x(2)} y1={top} y2={bottom} className="change-marker"/>
      <polyline points={path(control)} className="baseline-line"/>
      <polyline points={path(selected)} className="scenario-line"/>
      {chosen && <><line x1={x(period)} x2={x(period)} y1={top} y2={bottom} className="selected-marker"/><circle cx={x(period)} cy={y(chosen.cash_close)} r="5" className="chart-dot"/></>}
      {(width < 400 ? [0, 2, 4, 6] : [0, 1, 2, 3, 4, 5, 6]).map(month => <text key={month} x={x(month)} y="187" textAnchor="middle" className="chart-label">{month === 0 ? 'Start' : month}</text>)}
      <text x={(left+right)/2} y="207" textAnchor="middle" className="chart-label">Monat · Änderung ab Monat 3</text>
    </svg>
  </div>;
}

function Flow({row, reference, period, selected, onSelect}: {row: Row; reference: Row; period: number; selected: number; onSelect: (n: number) => void}) {
  const saving = row.case === 'deposit';
  const nodes = [
    {label: 'Szenarioparameter', title: 'Jährlicher Zins', value: percent(row.annual_rate), note: period < 3 ? 'Noch vor der Änderung' : 'Ab Monat 3 wirksam', icon: GitBranch},
    {label: 'Vertrag', title: saving ? 'Zinseinnahmen' : 'Zinskosten', value: euros(saving ? row.interest_income : row.interest_cost), note: `${percent(row.contract_rate)} jährlich · pro Monat`, icon: Landmark},
    {label: 'Haushaltsbudget', title: 'Laufender Spielraum', value: euros(row.monthly_headroom), note: 'Nach notwendigen Zahlungen', icon: Wallet},
    {label: 'Anlageplan', title: 'Neue Vormerkung', value: euros(row.planned_allocation), note: 'Ziel: 100 € pro Monat', icon: Coins},
  ];
  const changed = Math.abs(row.contract_rate-reference.contract_rate) > .000001;
  return <div className={`flow-grid ${changed ? 'has-change' : ''}`} aria-label="Berechnete Wirkungskette">
    {nodes.map((node, index) => <div className="flow-cell" key={node.label}>
      <button type="button" className={`flow-node ${selected === index ? 'selected' : ''} ${index === 3 && row.planned_allocation < 100 ? 'restricted' : ''}`} onClick={() => onSelect(index)} aria-pressed={selected === index}>
        <span className="node-top"><node.icon size={18}/><span className="node-number">0{index+1}</span></span>
        <span className="node-label">{node.label}</span><span className="node-title">{node.title}</span>
        <strong className="node-value">{node.value}</strong><span className="node-note">{node.note}</span>
      </button>
      {index < 3 && <span key={`${index}-${period}-${changed}`} className={`connector ${changed ? 'active' : ''}`} aria-hidden="true"><ArrowRight size={19}/></span>}
    </div>)}
  </div>;
}

function Explanation({node, row, reference, period}: {node: number; row: Row; reference: Row; period: number}) {
  const details = [
    {title: 'Was ändert sich?', text: period < 3 ? 'Die Zinsänderung ist erst für Monat 3 angesetzt. Bis dahin gilt in allen Varianten der Ausgangszins von 2 %.' : `Der Szenarioparameter liegt bei ${percent(row.annual_rate)}. Im POC ist das direkt ein Vertragszinssatz. Eine Übertragung vom Leitzins wird nicht simuliert.`},
    {title: 'Welche Vertragsbedingung wirkt?', text: row.case === 'fixed_loan' ? 'Dieser Kredit ist im Test auf 2 % festgelegt. Die Szenarioänderung verändert seine Zinskosten deshalb nicht. Tilgungen sind nicht enthalten.' : row.case === 'deposit' ? `Die separate Einlage von 60.000 € bringt in diesem Monat ${euros(row.interest_income)} Zinsen. Berechnung: Kapital × jährlicher Zinssatz ÷ 12.` : `Der variable Kredit über 60.000 € verursacht in diesem Monat ${euros(row.interest_cost)} Zinskosten. Berechnung: Restschuld × jährlicher Zinssatz ÷ 12. Eine Tilgung ist nicht enthalten.`},
    {title: 'Wie entsteht der Spielraum?', text: `Den laufenden Einnahmen von ${euros(row.total_income)} stehen notwendige Zahlungen von ${euros(row.required_payments)} gegenüber. Der Unterschied beträgt ${euros(row.monthly_headroom)}. Die Änderung zum unveränderten Vergleich ist ${signed(row.monthly_headroom-reference.monthly_headroom)}.`},
    {title: 'Welche Regel steuert die Vormerkung?', text: 'Der Test merkt höchstens 100 € aus dem positiven laufenden Überschuss vor. Reicht der Überschuss nicht, sinkt die Vormerkung. Rücklagen werden dafür nicht angegriffen. Das ist eine feste Rechenregel und keine individuelle Entscheidung oder ein Aktienkauf.'},
  ];
  const detail = details[node] ?? details[0]!;
  return <div className="explanation" aria-live="polite"><span className="explanation-icon"><CircleHelp size={18}/></span><div><h3>{detail.title}</h3><p>{detail.text}</p></div><span className="rule-tag">Modellregel</span></div>;
}

export default function App() {
  const [draft, setDraft] = useState(6);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [period, setPeriod] = useState(1);
  const [caseId, setCaseId] = useState<CaseId>('variable_loan');
  const [playing, setPlaying] = useState(false);
  const [node, setNode] = useState(2);
  const [assumptionsOpen, setAssumptionsOpen] = useState(false);
  const controller = useRef<AbortController | null>(null);
  async function calculate(rate: number) {
    if (!Number.isFinite(rate) || rate < 0 || rate > 20) {setError('Bitte einen jährlichen Zinssatz zwischen 0 und 20 % eingeben.'); return;}
    controller.current?.abort();
    const abort = new AbortController(); controller.current = abort;
    setLoading(true); setError(''); setPlaying(false);
    try {
      const response = await fetch('/api/simulate', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({annual_rate_after: rate/100}), signal: abort.signal});
      const data: unknown = await response.json();
      if (!response.ok) throw new Error(typeof data === 'object' && data !== null && 'error' in data && typeof data.error === 'string' ? data.error : 'Die Berechnung ist fehlgeschlagen.');
      const parsed = ResultSchema.safeParse(data);
      if (!parsed.success) throw new Error('Die Antwort enthält keinen vollständigen, gültigen Verlauf.');
      setResult(parsed.data); setPeriod(1);
    } catch (failure) {
      if (abort.signal.aborted) return;
      setResult(null); setError(failure instanceof Error ? failure.message : 'Der Rechenkern ist nicht erreichbar.');
    } finally {if (!abort.signal.aborted) setLoading(false);}
  }
  useEffect(() => {void calculate(6); return () => controller.current?.abort();}, []);
  useEffect(() => {
    if (!playing) return;
    const timer = window.setInterval(() => setPeriod(previous => {if (previous >= 6) {setPlaying(false); return 6;} return previous+1;}), 1100);
    return () => window.clearInterval(timer);
  }, [playing]);
  const row = result ? lookup(result.rows, caseId, period) : undefined;
  const reference = result ? lookup(result.baseline, caseId, period) : undefined;
  const dirty = result !== null && Math.abs(draft/100-result.request.annual_rate_after) > .000001;
  const currentEvents = result?.events.filter(event => event.case === caseId && event.period === period) ?? [];
  function move(to: number) {setPlaying(false); setPeriod(Math.max(1, Math.min(6, to)));}
  return <div className="app">
    <header className="topbar"><a href="#" className="brand" aria-label="Counterloom Start"><span className="brand-mark"><Layers3 size={21}/></span><span>counterloom<span className="brand-dot">.</span></span></a><div className="top-divider"/><span className="top-context">Lernwelt</span><span className="poc-pill">POC 01</span><div className="top-right"><span className="offline-dot"/>Algorithmisch · 0 LLM-Aufrufe</div></header>
    <main>
      <div className="page-title"><div><div className="eyebrow">ZUSAMMENHÄNGE SICHTBAR MACHEN</div><h1>Ein Zins. Drei Ausgangslagen.</h1><p>Verändere eine Bedingung und verfolge, wie sich der finanzielle Spielraum entwickelt.</p></div><span className="fixture-badge"><Activity size={14}/>Fiktiver Lerntest</span></div>
      <div className="workspace">
        <aside className="scenario-panel">
          <div className="section-caption"><GitBranch size={16}/>Szenario</div>
          <h2>Eine Bedingung verändern</h2><p className="muted">Der neue Vertragszinssatz gilt ab Monat 3. Der Vergleich bleibt bei 2 %.</p>
          <label htmlFor="rate">Jährlicher Zinssatz</label><div className="rate-input"><input id="rate" type="number" min="0" max="20" step="0.1" value={Number.isNaN(draft) ? '' : draft} onChange={event => setDraft(event.target.valueAsNumber)} aria-describedby="rate-hint"/><span>%</span></div>
          <input type="range" aria-label="Jährlicher Zinssatz auswählen" min="0" max="20" step=".5" value={Number.isFinite(draft) ? draft : 0} onChange={event => setDraft(Number(event.target.value))}/><div className="range-labels"><span>0 %</span><span>20 %</span></div>
          <div className="presets">{[0, 2, 6].map(value => <button type="button" key={value} aria-pressed={draft === value} onClick={() => setDraft(value)}>{value === 0 ? 'Sinkt · 0 %' : value === 2 ? 'Gleich · 2 %' : 'Steigt · 6 %'}</button>)}</div>
          <button type="button" className="primary-button" disabled={loading || !Number.isFinite(draft) || draft < 0 || draft > 20} onClick={() => {void calculate(draft);}}>{loading ? <LoaderCircle className="spin" size={17}/> : <ArrowUpRight size={17}/>} {loading ? 'Wird berechnet …' : 'Verlauf berechnen'}</button>
          <p id="rate-hint" className="small-note">{dirty ? 'Neue Eingabe: Noch nicht berechnet. Die Ansicht zeigt den letzten Lauf.' : result ? `Berechnet: ${percent(result.request.annual_rate_after)} ab Monat 3.` : 'Ein neuer Lauf wird lokal berechnet.'}</p>
          <div className="scenario-separator"/>
          <div className="section-caption"><Wallet size={16}/>Gemeinsame Ausgangswerte</div>
          <dl className="assumption-list"><div><dt>Einkommen / Monat</dt><dd>2.400 €</dd></div><div><dt>Notwendige Ausgaben</dt><dd>2.100 €</dd></div><div><dt>Verfügbares Geld zu Beginn</dt><dd>1.000 €</dd></div><div><dt>Ziel-Vormerkung / Monat</dt><dd>100 €</dd></div></dl>
          <button className="text-button" type="button" onClick={() => setAssumptionsOpen(!assumptionsOpen)} aria-expanded={assumptionsOpen}><CircleHelp size={15}/>Annahmen und Grenzen<ChevronDown size={14}/></button>
        </aside>
        <section className="model-panel" aria-label="Modellverlauf">
          {error && <div className="error-banner" role="alert"><X size={18}/><div><strong>Kein berechneter Verlauf</strong><p>{error}</p></div></div>}
          {!result && !error && <div className="empty-state" role="status"><LoaderCircle className="spin"/><p>Der erste Verlauf wird berechnet …</p></div>}
          {result && row && reference && <>
            <div className="panel-heading"><div><span className="section-caption">DIE GLEICHE ÄNDERUNG, ANDERE WIRKUNG</span><h2>Eine Ausgangslage erkunden</h2></div><span className="run-status"><Check size={13}/>Berechnet</span></div>
            <div className="case-tabs" role="group" aria-label="Vertragslage auswählen">{(['variable_loan','fixed_loan','deposit'] as const).map(id => {const item = labels[id]; const Icon = item.icon; return <button key={id} type="button" className={caseId === id ? 'active' : ''} aria-pressed={caseId === id} onClick={() => setCaseId(id)}><Icon size={19}/><span><strong>{item.title}</strong><small>{item.subtitle}</small></span></button>;})}</div>
            <div className="timeline"><div className="timeline-head"><span className="month-label">Monat <strong>{period}</strong><span> / 6</span></span><div className="play-controls"><button aria-label="Zum ersten Monat" type="button" onClick={() => move(1)}><RotateCcw size={15}/></button><button aria-label="Vorheriger Monat" type="button" onClick={() => move(period-1)} disabled={period === 1}><ArrowLeft size={16}/></button><button className="play-button" aria-label={playing ? 'Wiedergabe pausieren' : 'Verlauf abspielen'} type="button" onClick={() => {if (period === 6 && !playing) setPeriod(1); setPlaying(!playing);}}>{playing ? <CirclePause size={19}/> : <CirclePlay size={19}/>}<span>{playing ? 'Pause' : 'Abspielen'}</span></button><button aria-label="Nächster Monat" type="button" onClick={() => move(period+1)} disabled={period === 6}><ArrowRight size={16}/></button></div></div><input type="range" min="1" max="6" step="1" value={period} aria-label="Monat auswählen" onChange={event => move(Number(event.target.value))}/><div className="month-ticks">{[1,2,3,4,5,6].map(m => <button key={m} type="button" onClick={() => move(m)} aria-label={`Monat ${m} anzeigen`} aria-current={period === m ? 'step' : undefined}>{m === 3 ? <><span className="change-dot"/>3 · Änderung</> : m}</button>)}</div></div>
            <Flow row={row} reference={reference} period={period} selected={node} onSelect={setNode}/>
            <Explanation node={node} row={row} reference={reference} period={period}/>
            {row.payment_gap > 0 && <div className="gap-banner" role="status">Zahlungslücke in diesem Monat: <strong>{euros(row.payment_gap)}</strong>. Offene Verpflichtungen gesamt: {euros(row.arrears_close)}. Es wird kein zusätzlicher Kredit angenommen.</div>}
            <div className="lower-panels">
              <section className="history-panel"><div className="subheading"><h3>Verfügbares Geld</h3><div className="legend"><span><i className="scenario-swatch"/>Variante</span><span><i className="baseline-swatch"/>Unverändert · 2 %</span></div></div><TraceChart rows={result.rows} baseline={result.baseline} id={caseId} period={period}/></section>
              <section className="balance-panel"><h3>Stand nach Monat {period}</h3><dl><div><dt>Verfügbares Geld</dt><dd>{euros(row.cash_close)}</dd></div><div><dt>Zum unveränderten Verlauf</dt><dd className={row.cash_close-reference.cash_close < -.01 ? 'negative' : row.cash_close-reference.cash_close > .01 ? 'positive' : ''}>{signed(row.cash_close-reference.cash_close)}</dd></div><div><dt>Für Anlagen vorgemerkt</dt><dd>{euros(row.earmarked_close)}</dd></div><div><dt>Offene Verpflichtungen</dt><dd className={row.arrears_close > 0 ? 'negative' : ''}>{euros(row.arrears_close)}</dd></div></dl><div className="balance-footnote">Vormerkungen bleiben ein eigener Geldtopf. Sie sind kein verfügbarer Kontostand und kein Wertpapierbestand.</div></section>
            </div>
            <section className="event-strip" aria-label="Vorgänge des ausgewählten Monats"><span className="event-strip-title">IN DIESEM MONAT</span>{currentEvents.map(event => <span key={event.id} className={`event-chip ${event.kind === 'contract_repriced' ? 'highlight' : ''}`}><span className="event-dot"/>{event.label}{event.amount !== null && <strong>{event.kind === 'cash_flow_settled' ? signed(event.amount) : euros(event.amount)}</strong>}</span>)}</section>
          </>}
          {loading && result && <div className="loading-overlay" role="status"><LoaderCircle className="spin" size={22}/><span>Neuen Verlauf berechnen …</span></div>}
        </section>
      </div>
      {assumptionsOpen && result && <section className="assumptions-panel"><div className="subheading"><h2>Annahmen und Grenzen dieses POC</h2><button aria-label="Annahmen schließen" type="button" className="icon-button" onClick={() => setAssumptionsOpen(false)}><X size={18}/></button></div><ul>{result.assumptions.map(text => <li key={text}>{text}</li>)}</ul></section>}
      <footer><span>Fiktive Rechenfälle · keine autonomen Personas · keine Anlageempfehlung</span>{result && <span>BPTK-Py {result.meta.version} · Lauf {result.meta.run_id} · {Math.round(result.meta.elapsed_ms)} ms<span className="replay-label"> Ansicht = Wiedergabe</span></span>}</footer>
    </main>
  </div>;
}
