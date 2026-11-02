#!/usr/bin/env python3
"""Repeat the independent company-v4 audit: six 24-month worlds.

Uses integer-cent reconstruction and explicit goods/cost/equity bridges.
Requires POC Python dependencies. No UI, network, LLM or empirical calibration.
The original QA evidence is read for source/version and result comparison only.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'qa/company-v4-plausibility.json'
SCENARIOS = [
    ('baseline', [], None),
    ('energy_m3', [(3, 'energy')], None),
    ('demand_m3', [(3, 'demand')], None),
    ('both_m3', [(3, 'energy'), (3, 'demand')], None),
    ('demand_m3_recovery_m13', [(3, 'demand'), (13, 'demand_recovery')], None),
    ('machine_credit_m1', [], 1),
]

def run_world(name, events, credit_month):
    """Reconstruct cash, bank balance, goods, inventory costs and retained equity from actual transactions."""
    w = World()
    accounts = dict(w.initial)
    loan_assets = 2400000
    reserves = 13200000
    pos = 0
    postings = 0
    months = []
    goods = {f: {'units': 0, 'value': 0} for f in ['alltag', 'werkstatt']}
    retained = {f: 0 for f in goods}
    for month in range(1, 25):
        for (when, e) in events:
            if month == when:
                w.queue(e)
        if month == credit_month:
            w.banking.request(w)
        opening = {f: dict(goods[f]) for f in goods}
        loan_open_principal = w.banking.loan.outstanding_cents
        loan_open_delivered = w.banking.loan.delivery_month
        capital_open = {f: w.nodes[f]['capital'] for f in goods}
        staff_open = {f: len(w.nodes[f]['employees']) for f in goods}
        forecast_open = {f: w.nodes[f]['company']['forecast_milli'] for f in goods}
        cost_of_sales = {f: 0 for f in goods}
        paid_production = {f: 0 for f in goods}
        produced = {f: 0 for f in goods}
        sold = {f: 0 for f in goods}
        for phase in range(5):
            w.step()
            new = w.journal[pos:]
            if phase == 0:
                for f in goods:
                    n = w.nodes[f]
                    m = n['metrics']
                    wages = sum((t['amount_cents'] for t in new if t['source'] == f and t['kind'] == 'wage'))
                    energy = sum((t['amount_cents'] for t in new if t['source'] == f and t['kind'] == 'energy'))
                    unitcost = (500 if f == 'alltag' else 900) * w.energy_multiplier
                    assert energy % unitcost == 0
                    units = energy // unitcost
                    labor = wages * n['productivity'] // 240000
                    if labor:
                        labor += capital_open[f] * 4
                    demand = (forecast_open[f] + 500) // 1000
                    target = (demand + 3) // 4
                    need = max(0, demand + target - (opening[f]['units'] - n.get('reserved_units', 0)))
                    assert units <= labor and units <= need
                    assert units == m['produced_units'] == n['company']['plan']['funded_units']
                    direct_cost = wages * units // max(1, labor) + energy
                    assert direct_cost == m['production_cost']
                    assert m['idle_cost'] == wages - wages * units // max(1, labor)
                    assert m['unpaid_wages'] == staff_open[f] * 240000 - wages
                    produced[f] = units
                    paid_production[f] = direct_cost
                    goods[f]['units'] += units
                    goods[f]['value'] += direct_cost
            for t in new:
                a = t['amount_cents']
                effect = t['ledger_effect']
                before_deposits = sum((v for (k, v) in accounts.items() if k != 'bank'))
                before_equity = accounts['bank']
                before_loans = loan_assets
                assert t['source_before'] == accounts[t['source']] and t['target_before'] == accounts[t['target']]
                if effect == 'loan_creation':
                    accounts[t['target']] += a
                    loan_assets += a
                elif effect == 'principal_repayment':
                    accounts[t['source']] -= a
                    loan_assets -= a
                else:
                    accounts[t['source']] -= a
                    accounts[t['target']] += a
                deposits = sum((v for (k, v) in accounts.items() if k != 'bank'))
                equity = accounts['bank']
                assert reserves + loan_assets == deposits + equity
                assert t['deposit_delta_cents'] == deposits - before_deposits and t['loan_delta_cents'] == loan_assets - before_loans and (t['equity_delta_cents'] == equity - before_equity)
                for (b, l, d, e) in [(t['bank_before'], before_loans, before_deposits, before_equity), (t['bank_after'], loan_assets, deposits, equity)]:
                    assert b['assets_cents'] == reserves + l and b['liabilities_and_equity_cents'] == d + e
                if t['target'] in goods and t['kind'] in ['consumption', 'procurement', 'investment', 'machine_purchase']:
                    f = t['target']
                    price = w.nodes[f]['price']
                    assert a % price == 0
                    units = a // price
                    assert units <= goods[f]['units']
                    cost = goods[f]['value'] * units // goods[f]['units']
                    goods[f]['units'] -= units
                    goods[f]['value'] -= cost
                    cost_of_sales[f] += cost
                    sold[f] += units
                postings += 1
            pos = len(w.journal)
            assert accounts == {k: n['cash_cents'] for (k, n) in w.nodes.items()}
            for f in goods:
                assert goods[f]['units'] == w.nodes[f]['inventory']
                assert goods[f]['value'] == w.nodes[f]['company']['inventory_value_cents']
                assert goods[f]['value'] >= 0
                if goods[f]['units'] == 0:
                    assert goods[f]['value'] == 0
        company = []
        tx = [t for t in w.journal if t['month'] == month]
        for f in goods:
            n = w.nodes[f]
            m = n['metrics']
            r = n['company']['result']
            c = n['company']
            sales = sum((t['amount_cents'] for t in tx if t['target'] == f and t['kind'] in ['consumption', 'procurement', 'investment', 'machine_purchase']))
            interest_due = 2000 + (loan_open_principal * 600 // 120000 if f == 'alltag' and loan_open_delivered is not None and (month > loan_open_delivered) else 0)
            profit = sales - cost_of_sales[f] - m['idle_cost'] - m['unpaid_wages'] - interest_due
            tax_due = max(0, profit) * 20 // 100
            dividends = sum((t['amount_cents'] for t in tx if t['source'] == f and t['kind'] == 'company_dividend'))
            assert m['sales'] == sales and m['cost_of_sales'] == cost_of_sales[f]
            assert profit == r['profit_before_tax_cents'] and tax_due == r['tax_due_cents']
            assert dividends == r['distribution_cents'] and dividends <= max(0, profit - tax_due) // 2
            assert r['retained_result_cents'] == profit - tax_due - dividends
            retained[f] += profit - tax_due - dividends
            liabilities = n['loan'] + n.get('machine_loan_cents', 0) + sum((o['amount_cents'] for o in w.obligations if o['source'] == f)) + (w.banking.loan.overdue_interest_cents if f == 'alltag' else 0)
            balance_equity = n['cash_cents'] + goods[f]['value'] + n['capital'] * 120000 - liabilities
            assert balance_equity == 1200000 + retained[f]
            if dividends:
                assert n['cash_cents'] >= r['reserve_cents'] and (not any((o['source'] == f for o in w.obligations)))
            assert n['inventory'] == opening[f]['units'] + produced[f] - sold[f]
            assert c['inventory_value_cents'] == opening[f]['value'] + paid_production[f] - cost_of_sales[f]
            expected_forecast = (3 * forecast_open[f] + (m['sold_units'] + m['unmet_units']) * 1000) // 4
            assert c['forecast_milli'] == expected_forecast
            assert abs(len(n['employees']) - staff_open[f]) <= 1
            company.append({'id': f, 'cash_eur': n['cash_cents'] / 100, 'inventory_units': n['inventory'], 'inventory_value_eur': c['inventory_value_cents'] / 100, 'produced_units': produced[f], 'sold_units': sold[f], 'forecast_units': c['forecast_milli'] / 1000, 'staff': len(n['employees']), 'desired_staff': r['desired_staff'], 'profit_eur': profit / 100, 'tax_eur': r['tax_paid_cents'] / 100, 'dividend_eur': dividends / 100, 'retained_eur': r['retained_result_cents'] / 100, 'reserve_eur': r['reserve_cents'] / 100, 'reconstructed_equity_eur': balance_equity / 100, 'cumulative_retained_eur': retained[f] / 100})
        months.append({'month': month, 'consumption_eur': w.history[-1]['consumption_cents'] / 100, 'employment_relations': w.history[-1]['employment'], 'household_cash_eur': sum((h['cash_cents'] for h in w.households())) / 100, 'government_cash_eur': w.nodes['staat']['cash_cents'] / 100, 'external_cash_eur': w.nodes['ausland']['cash_cents'] / 100, 'companies': company})
    assert w.snapshot()['completed']
    before = len(w.journal)
    try:
        w.step()
        raise AssertionError('25th month accepted')
    except ValueError:
        pass
    assert len(w.journal) == before
    return {'name': name, 'events': [{'month': m, 'event': e} for (m, e) in events], 'credit_month': credit_month, 'independently_reconstructed_postings': postings, 'all_bridges_passed': True, 'months': months, 'loan_status': w.banking.loan.status, 'loan_interest_paid_eur': w.banking.loan.interest_paid_cents / 100, 'loan_remaining_eur': w.banking.loan.outstanding_cents / 100}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write this repeat to a new JSON file; recorded QA is never overwritten.')
    args = parser.parse_args()
    if not __debug__:
        parser.error('Assertions must be enabled; do not run Python with -O.')
    output = args.output.resolve() if args.output else None
    if output and output.exists():
        parser.error('Output already exists. Choose a new path for this repeat.')
    evidence = json.loads(EVIDENCE.read_text())
    for item in evidence['source_files']:
        actual = hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            parser.error('Source differs from the audited V4 kernel: ' + item['path'])
    runtime = ROOT / 'poc/.runtime/company-plausibility'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    sys.path.insert(0, str(ROOT / 'poc'))
    global World
    from world import World
    results = []
    for name, events, credit_month in SCENARIOS:
        result = run_world(name, events, credit_month)
        results.append(result)
        print(name, result['independently_reconstructed_postings'], 'postings and all company bridges passed', flush=True)
    if results != evidence['scenarios']:
        raise AssertionError('Repeated scenarios differ from the recorded independent V4 audit.')
    count = sum(r['independently_reconstructed_postings'] for r in results)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            'executed_at_utc': datetime.now(timezone.utc).isoformat(),
            'evidence_reference': 'qa/company-v4-plausibility.json',
            'source_files': evidence['source_files'],
            'scope': 'Repeat of the recorded independent V4 company audit, not empirical validation.',
            'recorded_results_match': True,
            'scenarios': results,
            'summary': {'worlds': 6, 'world_months': 144, 'phases': 720, 'independently_reconstructed_postings': count},
        }, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: 6 worlds, 144 months, {count} postings; cash, goods, inventory-value, profit and equity bridges match.')


if __name__ == '__main__':
    main()
