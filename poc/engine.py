"""Bounded local adapter around the already tested BPTK fixture."""
from datetime import datetime, timezone
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from threading import Lock
import math
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location('counterloom_fixture', ROOT / 'tools/probe_bptk_hybrid.py')
fixture = module_from_spec(spec)
spec.loader.exec_module(fixture)
LOCK = Lock()


def validate_request(payload):
    if not isinstance(payload, dict) or set(payload) != {'annual_rate_after'}:
        raise ValueError('Erwartet wird ausschließlich der Parameter annual_rate_after.')
    rate = payload['annual_rate_after']
    if isinstance(rate, bool) or not isinstance(rate, (int, float)) or not math.isfinite(rate):
        raise ValueError('Der Zinssatz muss eine endliche Zahl sein.')
    if not 0 <= rate <= .20:
        raise ValueError('Der jährliche Zinssatz muss zwischen 0 und 20 % liegen.')
    return float(rate)


def enrich(rows):
    result = []
    for original in rows:
        row = {k: round(v, 6) if isinstance(v, float) else v for k, v in original.items()}
        received = row['income'] + row['interest_income']
        due = row['essential_expenses'] + row['interest_cost']
        paid = min(due, row['cash_open'] + received)
        row.update(total_income=round(received, 6), required_payments=round(due, 6),
                   actual_payment=round(paid, 6), monthly_headroom=round(received-due, 6),
                   cash_change=round(row['cash_close']-row['cash_open'], 6),
                   payment_gap=round(max(0, due-paid), 6))
        result.append(row)
    return result


def simulate_request(payload):
    rate = validate_request(payload)
    started = time.perf_counter()
    with LOCK:
        baseline = enrich(fixture.simulate(.02))
        rows = enrich(fixture.simulate(rate))
    events = []
    for row in rows:
        case = next(c for c in fixture.CASES if c['id'] == row['case'])
        records = [('cash_flow_settled', 'Zahlungsströme verbucht', row['cash_change'])]
        if row['period'] == 3 and rate != .02 and case['variable']:
            records.append(('contract_repriced', 'Vertragszins angepasst', None))
        if row['planned_allocation'] > 0:
            records.append(('investment_earmarked', 'Geld für Anlage vorgemerkt', row['planned_allocation']))
        if row['payment_gap'] > 0:
            records.append(('payment_gap', 'Zahlung nicht vollständig gedeckt', row['payment_gap']))
        for kind, label, amount in records:
            events.append({'id': f"{row['case']}-{row['period']}-{kind}", 'case': row['case'],
                           'period': row['period'], 'kind': kind, 'label': label, 'amount': amount})
    return {
        'meta': {'engine': 'BPTK-Py', 'version': fixture.VERSION,
                 'elapsed_ms': round((time.perf_counter()-started)*1000, 2), 'llm_calls': 0,
                 'classification': 'hypothetical_algorithmic_poc', 'run_id': uuid.uuid4().hex[:12],
                 'generated_at': datetime.now(timezone.utc).isoformat()},
        'request': {'annual_rate_after': rate}, 'periods': 6, 'change_month': 3,
        'cases': fixture.CASES, 'rows': rows, 'baseline': baseline, 'events': events,
        'assumptions': [
            'Drei fiktive Rechenfälle, keine empirisch abgeleiteten Investorentypen.',
            'Alle Fälle: 2.400 € monatliches Einkommen, 2.100 € notwendige Ausgaben und 1.000 € verfügbares Geld zu Beginn.',
            'Kredit oder separate verzinste Einlage: 60.000 €. Einfache Zinsen: jährlicher Satz geteilt durch zwölf; keine Tilgung oder Zinseszinsen.',
            'Ausgangszins 2 %. Der gewählte Vertragszinssatz gilt ab Monat 3; der Festzinskredit bleibt bei 2 %.',
            'Vormerkung: höchstens 100 € pro Monat aus dem laufenden Überschuss. Das ist ein separater Geldtopf und kein ausgeführter Wertpapierkauf.',
            'Für notwendige Zahlungen dürfen Rücklagen aufgebraucht werden. Nicht gedeckte Beträge werden als offene Verpflichtungen fortgeschrieben.',
            'Das technische Ereignis „Vertrag angepasst“ ist keine modellierte Angst oder autonome Persona-Entscheidung.',
            'Kein EZB-Transmissionsmodell, keine Inflation, vollständigen Bankbilanzen, Gebühren oder makroökonomischen Rückkopplungen.'
        ]}
