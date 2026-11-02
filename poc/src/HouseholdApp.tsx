import { useEffect, useRef, useState } from 'react';
import { ArrowDown, Check, ChevronDown, ChevronRight, CircleHelp, Coins, Home, Landmark, Layers3, LoaderCircle, Pause, Play, RotateCcw, ShieldCheck, Wallet, X } from 'lucide-react';
import { ResultSchema, type CaseId, type Result, type Row } from './schema';

const euros = (value: number) => new Intl.NumberFormat('de-DE', {style: 'currency', currency: 'EUR', maximumFractionDigits: 0}).format(value);
const percent = (value: number) => new Intl.NumberFormat('de-DE', {style: 'percent', maximumFractionDigits: 2}).format(value);
const signed = (value: number) => `${value > 0 ? '+' : ''}${euros(value)}`;
const ids: CaseId[] = ['variable_loan', 'fixed_loan', 'deposit'];
const households = {
  variable_loan: {name: 'Variabel verzinster Kredit', short: 'Variabler Kredit', situation: 'Dieser Haushalt schuldet der Bank 60.000 €. Steigt der Vertragszins, steigt auch seine monatliche Zinszahlung.', icon: Landmark, theme: 'peach'},
  fixed_loan: {name: 'Fest verzinster Kredit', short: 'Festzinskredit', situation: 'Dieser Haushalt schuldet der Bank ebenfalls 60.000 €. Der Vertragszins beträgt während aller sechs Monate 2 %.', icon: ShieldCheck, theme: 'lavender'},
  deposit: {name: 'Verzinste Bankeinlage', short: 'Verzinstes Guthaben', situation: 'Dieser Haushalt hat stattdessen 60.000 € auf einem separaten Konto. Ändert sich dessen Zins, ändern sich seine Zinseinnahmen.', icon: Coins, theme: 'mint'},
};
const lookup = (rows: Row[], id: CaseId, month: number) => rows.find(row => row.case === id && row.period === month)!;

// Decorative, fictional households. No demographic or psychological properties are inferred.
function HouseholdPicture({theme}: {theme: string}) {
  return <svg className={`household-picture ${theme}`} viewBox="0 0 300 148" aria-hidden="true">
    <ellipse cx="150" cy="137" rx="123" ry="8" fill="currentColor" opacity=".08"/>
    <path d="M156 55 210 15 264 55V130H156Z" fill="white" opacity=".8"/>
    <path d="m148 56 62-46 62 46" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" opacity=".35"/>
    <rect x="199" y="88" width="24" height="42" rx="3" fill="currentColor" opacity=".13"/>
    <rect x="177" y="58" width="19" height="20" rx="3" fill="currentColor" opacity=".13"/>
    <rect x="228" y="58" width="19" height="20" rx="3" fill="currentColor" opacity=".13"/>
    <path d="M55 132V104Q55 78 80 78Q105 78 105 104V132" fill="currentColor" opacity=".85"/>
    <circle cx="80" cy="58" r="20" fill="#e5b592"/>
    <path d="M60 58Q55 31 80 34Q104 31 101 58L93 48 67 48Z" fill="#393c40"/>
    <path d="M99 132V110Q99 85 122 85Q145 85 145 110V132" fill="currentColor" opacity=".45"/>
    <circle cx="122" cy="65" r="18" fill="#bd8a69"/>
    <path d="M104 66V54Q104 41 122 42Q142 40 141 65L132 55 111 54Z" fill="#393c40"/>
    <path d="M43 132h114" stroke="currentColor" strokeWidth="3" strokeLinecap="round" opacity=".3"/>
    <circle cx="264" cy="117" r="12" fill="currentColor" opacity=".2"/><path d="M264 117v17" stroke="currentColor" strokeWidth="3" opacity=".3"/>
  </svg>;
}

function outcome(row: Row, baseline: Row, started: boolean) {
  if (!started) return 'Ausgangswerte vor der Zinsänderung.';
  const delta = row.monthly_headroom - baseline.monthly_headroom;
  if (row.period < 3) return 'Noch gilt der alte Zins. Es hat sich nichts verändert.';
  if (row.case === 'fixed_loan') return 'Der Vertragszins bleibt fest bei 2 %. Die Zinszahlung ändert sich nicht.';
  if (Math.abs(delta) < .005) return 'Bei unverändertem Vertragszins bleibt der monatliche Überschuss unverändert.';
  return row.case === 'deposit'
    ? `Die Bank zahlt ${euros(Math.abs(delta))} ${delta > 0 ? 'mehr' : 'weniger'} Zinsen im Monat.`
    : `An die Bank gehen ${euros(Math.abs(delta))} ${delta < 0 ? 'mehr' : 'weniger'} Zinsen im Monat.`;
}

function MoneyJourney({row, baseline}: {row: Row; baseline: Row}) {
  const [explain, setExplain] = useState(false);
  const delta = row.monthly_headroom - baseline.monthly_headroom;
  const deposit = row.case === 'deposit';
  return <div className="money-journey">
    <div className="money-source"><span className="money-icon"><Wallet size={23}/></span><div><span>Monatliches Einkommen</span><strong>{euros(row.income)}</strong><small>Einkommen</small></div></div>
    <div className="journey-arrow" aria-hidden="true"><span/><ArrowDown size={19}/></div>
    <div className="payment-row">
      <div className="payment-block"><Home size={20}/><span>Notwendige Ausgaben</span><strong>− {euros(row.essential_expenses)}</strong><small>Wohnen, Essen und weitere notwendige Ausgaben</small></div>
      <div className={`payment-block bank-payment ${delta < 0 ? 'costlier' : delta > 0 ? 'better' : ''}`}><Landmark size={20}/><span>{deposit ? 'Von der Bank' : 'An die Bank'}</span><strong>{deposit ? '+' : '−'} {euros(deposit ? row.interest_income : row.interest_cost)}</strong><small>{deposit ? 'Zinsen für das Guthaben' : 'Zinsen für den Kredit'} · {percent(row.contract_rate)} im Jahr</small>{row.period >= 3 && <em>{row.case === 'fixed_loan' ? 'Bleibt fest bei 2 %' : Math.abs(delta) < .005 ? 'Unverändert' : `${signed(delta)} für den Haushalt`}</em>}</div>
    </div>
    <div className="journey-arrow" aria-hidden="true"><span/><ArrowDown size={19}/></div>
    <div className={`money-remainder ${row.monthly_headroom < 0 ? 'shortfall' : ''}`}><div><span>{row.monthly_headroom < 0 ? 'Fehlbetrag nach laufenden Kosten' : 'Überschuss nach laufenden Kosten'}</span><strong>{euros(Math.abs(row.monthly_headroom))}</strong></div><p>{row.monthly_headroom < 0 ? 'Die laufenden Einnahmen reichen nicht für alle notwendigen Zahlungen.' : 'Dieser Betrag kann auf dem verfügbaren Konto bleiben oder als Rücklage geführt werden.'}</p></div>
    <div className="saving-explainer"><span className="saving-icon"><Coins size={22}/></span><div><strong>{euros(row.planned_allocation)} für eine spätere Anlage zurückgelegt</strong><p>{row.planned_allocation >= 100 ? 'Der Wunschbetrag von 100 € passt in den monatlichen Überschuss.' : row.planned_allocation > 0 ? 'Für die gewünschten 100 € reicht der Überschuss nicht ganz.' : 'Aus diesem Monat bleibt kein Überschuss für den gewünschten Anlagebetrag.'}</p><button className="inline-button" onClick={() => setExplain(!explain)} aria-expanded={explain}>Berechnungsregel anzeigen <ChevronDown size={14}/></button>{explain && <p className="rule-note">Modellregel: höchstens 100 € pro Monat aus dem positiven Überschuss auf ein separates Rücklagenkonto übertragen. Der restliche Überschuss bleibt auf dem verfügbaren Konto. Das ist eine Modellregel, keine persönliche Entscheidung. Es werden keine Wertpapiere gekauft.</p>}</div></div>
    {row.monthly_headroom < 0 && <div className="gap-note" role="status">{row.cash_open > 0 ? `Für notwendige Zahlungen wird auch auf das verfügbare Geld zu Monatsbeginn (${euros(row.cash_open)}) zurückgegriffen. ` : 'Es ist kein verfügbares Kontoguthaben mehr vorhanden. '}{row.payment_gap > 0 ? `${euros(row.payment_gap)} können diesen Monat nicht bezahlt werden und bleiben als Verpflichtung offen.` : 'Die Zahlungen können diesen Monat noch vollständig gedeckt werden.'}</div>}
    <div className="account-summary"><div><span>Verfügbares Guthaben am Monatsende</span><strong>{euros(row.cash_close)}</strong><small>Ohne den separaten Rücklagenkonto</small></div><div><span>Insgesamt für spätere Anlage zurückgelegt</span><strong>{euros(row.earmarked_close)}</strong><small>Seit Beginn der sechs Monate</small></div>{row.arrears_close > 0 && <div className="arrears"><span>Insgesamt noch offen</span><strong>{euros(row.arrears_close)}</strong><small>Nicht gedeckte Verpflichtungen</small></div>}</div>
  </div>;
}

export default function App() {
  const [draft, setDraft] = useState(6);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [started, setStarted] = useState(false);
  const [period, setPeriod] = useState(1);
  const [caseId, setCaseId] = useState<CaseId>('variable_loan');
  const [playing, setPlaying] = useState(false);
  const [customOpen, setCustomOpen] = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const controller = useRef<AbortController | null>(null);
  const detailRef = useRef<HTMLElement>(null);
  const householdsRef = useRef<HTMLElement>(null);
  async function calculate(rate: number, launch: boolean) {
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
      setResult(parsed.data); setStarted(launch); setPeriod(launch ? 3 : 1);
      if (launch) window.requestAnimationFrame(() => householdsRef.current?.scrollIntoView({behavior: 'instant', block: 'start'}));
    } catch (failure) {
      if (abort.signal.aborted) return;
      setResult(null); setError(failure instanceof Error ? failure.message : 'Der Rechenkern ist nicht erreichbar.');
    } finally {if (!abort.signal.aborted) setLoading(false);}
  }
  useEffect(() => {void calculate(2, false); return () => controller.current?.abort();}, []);
  useEffect(() => {
    if (!playing) return;
    const timer = window.setInterval(() => setPeriod(previous => {const next = Math.min(6, previous+1); if (next === 6) setPlaying(false); return next;}), 2000);
    return () => window.clearInterval(timer);
  }, [playing]);
  const rows = result ? started ? result.rows : result.baseline : [];
  const row = result ? lookup(rows, caseId, period) : undefined;
  const baseline = result ? lookup(result.baseline, caseId, period) : undefined;
  const dirty = started && result !== null && Math.abs(draft/100-result.request.annual_rate_after) > .000001;
  const valid = Number.isFinite(draft) && draft >= 0 && draft <= 20;
  const action = draft > 2 ? `Zinsen auf ${percent(draft/100)} erhöhen` : draft < 2 ? `Zinsen auf ${percent(draft/100)} senken` : 'Zins bei 2 % belassen';
  function reset() {setPlaying(false); setStarted(false); setPeriod(1);}
  function choose(id: CaseId) {setCaseId(id); detailRef.current?.scrollIntoView({behavior: 'instant', block: 'start'});}
  return <div className="app">
    <header className="topbar"><a href="#" className="brand" aria-label="Counterloom Start"><Layers3 size={24}/><span>counterloom<span className="brand-dot">.</span></span></a><span className="header-context">Haushaltsvergleich</span><span className="poc-pill">Fiktives Beispiel</span></header>
    <main>
      <div className="intro-heading"><span className="eyebrow">HAUSHALTSBUDGET UND VERTRAGSZINSEN</span><h1>Zinsänderungen und Haushaltsbudgets</h1><p>Drei Haushalte mit gleichem Einkommen und unterschiedlichen Kredit- oder Einlagenverträgen.<br className="desktop-break"/> Verglichen werden Zinszahlungen, monatlicher Überschuss und Kontoguthaben.</p></div>
      <section className="starting-point" aria-label="Gemeinsame Ausgangslage"><span className="step-number">1</span><div><h2>Ausgangswerte der drei Haushalte</h2><p>Alle haben monatlich <strong>2.400 € Einkommen</strong> und <strong>2.100 € Alltagskosten</strong>. Zu Beginn liegen <strong>1.000 € auf dem verfügbaren Konto</strong>. Sie möchten jeden Monat bis zu <strong>100 € für eine spätere Anlage</strong> zurücklegen.</p></div></section>
      {error && <div className="error-banner" role="alert"><X size={20}/><div><strong>Der Verlauf konnte nicht berechnet werden.</strong><p>{error} Bitte erneut versuchen.</p><button className="text-button" onClick={() => void calculate(valid ? draft : 6, true)}>Erneut versuchen</button></div></div>}
      {!result && !error && <div className="loading-state" role="status"><LoaderCircle className="spin"/>Die Haushalte werden vorbereitet …</div>}
      {result && row && baseline && <div className={loading ? 'results is-loading' : 'results'} aria-busy={loading}>
        <section className="households" ref={householdsRef} aria-label="Drei Haushalte vergleichen">{ids.map(id => {
          const info=households[id], current=lookup(rows,id,period), control=lookup(result.baseline,id,period), delta=current.monthly_headroom-control.monthly_headroom, Icon=info.icon;
          return <article className={`household-card ${info.theme} ${caseId===id ? 'selected' : ''}`} key={id}>
            <div className="card-scene"><span className="contract-tag"><Icon size={14}/>{info.short}</span><HouseholdPicture theme={info.theme}/></div>
            <div className="household-body"><h3>{info.name}</h3><p className="situation">{info.situation}</p><div className="household-outcome" aria-live="polite"><span>{current.monthly_headroom < 0 ? 'Fehlt nach laufenden Kosten / Monat' : 'Übrig nach laufenden Kosten / Monat'}</span><div><strong>{euros(Math.abs(current.monthly_headroom))}</strong>{started && <span className={`delta ${delta<0?'negative':delta>0?'positive':'neutral'}`}>{Math.abs(delta)<.005 ? 'Unverändert' : `${signed(delta)} zum Vergleich`}</span>}</div><div className="budget-track" aria-hidden="true"><span style={{width:`${Math.min(100,Math.max(0,current.monthly_headroom)/600*100)}%`}}/></div><p>{outcome(current,control,started)}</p></div><button className="inspect-button" aria-label={`Geldfluss: ${info.short}`} onClick={() => choose(id)} aria-pressed={caseId===id}>{caseId===id ? <Check size={16}/> : <CircleHelp size={16}/>} {caseId===id ? 'Berechnung ausgewählt' : 'Berechnung anzeigen'}<ChevronRight size={16}/></button></div>
          </article>;
        })}</section>
      <section className="experiment" aria-labelledby="experiment-title">
        <div className="experiment-main"><span className="step-number">2</span><div><h2 id="experiment-title">{started ? 'Zinsänderung angewendet' : 'Vertragszins ab Monat 3 ändern'}</h2><p>{started && result ? `Ab Monat 3 gilt ${percent(result.request.annual_rate_after)} statt 2 % für die veränderlichen Verträge. Der feste Kredit bleibt bei 2 %.` : `Bisher gelten 2 % Zins im Jahr. ${valid ? draft > 2 ? 'Erhöhe' : draft < 2 ? 'Senke' : 'Belasse' : 'Verändere'} den Zins für die veränderlichen Verträge ab Monat 3${valid ? ` auf ${percent(draft/100)}` : ''}.`}</p></div><button className="primary-button" disabled={loading || !valid} onClick={() => void calculate(draft, true)}>{loading ? <LoaderCircle size={19} className="spin"/> : <Play size={17} fill="currentColor"/>}{loading ? 'Wird berechnet …' : started && !dirty ? 'Erneut berechnen' : action}</button></div>
        <div className="experiment-tools"><button className="text-button" aria-expanded={customOpen} onClick={() => setCustomOpen(!customOpen)}>Vertragszins einstellen <ChevronDown size={14}/></button>{started && <button className="text-button" onClick={reset}><RotateCcw size={14}/>Zur Ausgangslage</button>}</div>
        {customOpen && <div className="custom-controls"><label htmlFor="rate">Neuer jährlicher Vertragszins</label><div className="rate-field"><input id="rate" type="number" min="0" max="20" step=".1" value={Number.isNaN(draft) ? '' : draft} onChange={e => setDraft(e.target.valueAsNumber)}/><span>%</span></div><div className="presets">{[0,2,6].map(value => <button key={value} aria-pressed={draft===value} onClick={() => setDraft(value)}>{value} %</button>)}</div><p>{dirty ? 'Noch nicht angewandt. Oben die Änderung auslösen; bis dahin bleibt der zuletzt berechnete Verlauf sichtbar.' : 'Erlaubt: 0 bis 20 %. Der neue Wert wird erst mit der Schaltfläche zur Zinsänderung angewendet.'}</p></div>}
      </section>
        <section className="time-panel" aria-label="Zeitverlauf"><div className="time-caption"><span className="time-dot"/><div><strong>{started ? `Monat ${period} von 6` : 'Ausgangslage · Monat 1'}</strong><span>{!started ? 'Löse oben die Zinsänderung aus, um die Folgen zu sehen.' : period<3 ? 'Noch vor der Änderung' : period===3 ? 'Der neue Zins wirkt jetzt zum ersten Mal.' : 'So entwickeln sich die Konten im weiteren Verlauf.'}</span></div></div>{started && <div className="timeline-controls"><div className="months">{[1,2,3,4,5,6].map(month=><button key={month} aria-label={`Monat ${month} ansehen`} aria-pressed={period===month} onClick={()=>{setPlaying(false);setPeriod(month);}} className={period===month?'active':''}>{month}<small>{month===3?'Änderung':'Monat'}</small></button>)}</div><button className="play-button" onClick={()=>{if(period===6)setPeriod(1);setPlaying(!playing);}} aria-label={playing?'Verlauf pausieren':'Monate abspielen'}>{playing?<Pause size={17}/>:<Play size={17}/>} {playing?'Pause':'Abspielen'}</button></div>}</section>
        <section className="household-detail" ref={detailRef} aria-labelledby="detail-title"><div className="detail-heading"><span className="step-number">3</span><div><span className="eyebrow">ZAHLUNGEN UND RÜCKLAGEN · MONAT {period}</span><h2 id="detail-title">{households[caseId].name}</h2><p>{outcome(row,baseline,started)} Die folgende Aufstellung zeigt die Berechnung.</p></div></div><div className="detail-layout"><aside className={`detail-person ${households[caseId].theme}`}><HouseholdPicture theme={households[caseId].theme}/><h3>Monatliches Haushaltsbudget</h3><p>Aufgeführt sind Einkommen, notwendige Ausgaben, Zinszahlungen und der verbleibende Überschuss oder Fehlbetrag.</p><div className="comparison-note"><span>Ohne Zinsänderung wären es</span><strong>{euros(baseline.monthly_headroom)} pro Monat</strong><small>Der Vergleich behält durchgehend 2 % bei.</small></div></aside><MoneyJourney key={`${caseId}-${result.meta.run_id}`} row={row} baseline={baseline}/></div></section>
        {started && period>=3 && <div className="reflection"><CircleHelp size={25}/><div><h2>{result.request.annual_rate_after > .02 ? 'Auswirkungen der Zinsänderung nach Vertragstyp' : 'Unterschiede zwischen den Vertragstypen'}</h2><p>Der monatliche Überschuss hängt vom Vertragstyp und dem angewendeten Zinssatz ab. Vergleiche Kredit- und Einlagenzinsen mit dem unveränderten Vertragszins von 2 %.</p></div></div>}
        <section className="model-details"><button className="details-toggle" onClick={()=>setDetailsOpen(!detailsOpen)} aria-expanded={detailsOpen}><span><CircleHelp size={17}/>Rechnung und Modellgrenzen</span><ChevronDown size={18}/></button>{detailsOpen && <div className="details-content"><h3>Ein vereinfachtes Beispiel</h3><p>Die Haushalte sind erfunden. Ihr Verhalten folgt einer festen Regel. Der veränderte Zins ist direkt der Vertragszins — es wird keine automatische Übertragung eines Zentralbankzinses auf alle Kredite behauptet. Kreditbetrag und Einlage bleiben konstant; Tilgung, Steuern, Inflation und Gebühren sind nicht enthalten. Die 60.000 € Einlage sind vom verfügbaren Konto getrennt.</p><ul>{result.assumptions.map(text=><li key={text}>{text}</li>)}</ul><h3>Sechs Monate für diesen Haushalt</h3><div className="table-scroll"><table><caption>Beträge in Euro. Zinskosten sind negativ, Zinseinnahmen positiv.</caption><thead><tr><th>Monat</th><th>Zinseffekt</th><th>Überschuss / Fehlbetrag</th><th>Für Anlage zurückgelegt</th><th>Verfügbares Konto</th><th>Offene Verpflichtungen</th></tr></thead><tbody>{rows.filter(r=>r.case===caseId).map(r=><tr key={r.period}><th>{r.period}</th><td>{euros(r.interest_income-r.interest_cost)}</td><td>{euros(r.monthly_headroom)}</td><td>{euros(r.planned_allocation)}</td><td>{euros(r.cash_close)}</td><td>{euros(r.arrears_close)}</td></tr>)}</tbody></table></div><p className="run-meta">Lauf {result.meta.run_id} · Die Monatsauswahl und die Wiedergabe zeigen den berechneten Verlauf.</p></div>}</section>
      </div>}
      <footer><Layers3 size={15}/><span>Counterloom · Ein reduziertes Lernmodell von Treno Solutions</span><span>Fiktive Haushalte · feste Rechenregeln · keine Anlageberatung</span></footer>
    </main>
  </div>;
}
