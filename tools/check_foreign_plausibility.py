#!/usr/bin/env python3
"""Repeat seven independent 24-month V5 worlds and nine isolated foreign-trade ports.

Checks integer-cent journals, bank balances, goods, inventory costs, company
results/equity and export delivery/budget bridges. Requires POC dependencies.
This is a reproducible model-consistency audit, not empirical validation.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'qa/foreign-v5-plausibility.json'
SCENARIOS = [
 ('baseline', [], None, None),
 ('no_exports', [], None, {'alltag': 0, 'werkstatt': 0}),
 ('energy_m3', [(3, 'energy')], None, None),
 ('demand_m3', [(3, 'demand')], None, None),
 ('both_m3', [(3, 'energy'), (3, 'demand')], None, None),
 ('recovery_m13', [(3, 'demand'), (13, 'demand_recovery')], None, None),
 ('machine_credit_m1', [], 1, None),
]

def run_world(name, events, credit_month, export_orders=None):
    """Reconstruct cash, bank balance, goods, inventory costs and retained equity from actual transactions."""
    w = World(export_orders_units=export_orders)
    accounts = dict(w.initial)
    loan_assets = 2400000
    reserves = 13200000
    pos = 0
    postings = 0
    months = []
    goods = {f: {'units': 0, 'value': 0} for f in ['alltag', 'werkstatt']}
    retained = {f: 0 for f in goods}
    desired_orders = export_orders if export_orders is not None else {'alltag': 6, 'werkstatt': 2}
    cumulative_imports = cumulative_exports = credit_created = principal_repaid = bank_income = bank_distributions = 0
    export_ids = set()
    for month in range(1, 25):
        for when, e in events:
            if month == when:
                w.queue(e)
        if month == credit_month:
            w.banking.request(w)
        opening = {f: dict(goods[f]) for f in goods}
        foreign_open = accounts['ausland']
        desired_cents = {f: desired_orders[f] * w.nodes[f]['price'] for f in goods}
        total_desired = sum(desired_cents.values())
        expected_budget = min(foreign_open, total_desired)
        allocated_alltag = expected_budget * desired_cents['alltag'] // total_desired if total_desired else 0
        allocations = {'alltag': allocated_alltag, 'werkstatt': expected_budget - allocated_alltag}
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
                before_deposits = sum((v for k, v in accounts.items() if k != 'bank'))
                before_equity = accounts['bank']
                before_loans = loan_assets
                assert t['source_before'] == accounts[t['source']] and t['target_before'] == accounts[t['target']]
                if effect == 'loan_creation':
                    credit_created += a
                    accounts[t['target']] += a
                    loan_assets += a
                elif effect == 'principal_repayment':
                    principal_repaid += a
                    accounts[t['source']] -= a
                    loan_assets -= a
                else:
                    accounts[t['source']] -= a
                    accounts[t['target']] += a
                    if effect == 'bank_income':
                        bank_income += a
                    if effect == 'bank_distribution':
                        bank_distributions += a
                if t['kind'] == 'energy':
                    cumulative_imports += a
                if t['kind'] == 'export_sale':
                    cumulative_exports += a
                deposits = sum((v for k, v in accounts.items() if k != 'bank'))
                equity = accounts['bank']
                assert reserves + loan_assets == deposits + equity
                assert t['deposit_delta_cents'] == deposits - before_deposits and t['loan_delta_cents'] == loan_assets - before_loans and (t['equity_delta_cents'] == equity - before_equity)
                for b, l, d, e in [(t['bank_before'], before_loans, before_deposits, before_equity), (t['bank_after'], loan_assets, deposits, equity)]:
                    assert b['assets_cents'] == reserves + l and b['liabilities_and_equity_cents'] == d + e
                if t['target'] in goods and t['kind'] in ['consumption', 'procurement', 'investment', 'machine_purchase', 'export_sale']:
                    f = t['target']
                    price = w.nodes[f]['price']
                    assert a % price == 0
                    units = a // price
                    assert units <= goods[f]['units']
                    cost = goods[f]['value'] * units // goods[f]['units']
                    if t['kind'] == 'export_sale':
                        export_ids.add(t['id'])
                        matches = [d for d in w.foreign.deliveries if d['transaction_id'] == t['id']]
                        assert len(matches) == 1
                        d = matches[0]
                        assert d['seller'] == f and d['buyer'] == 'ausland' and (t['source'] == 'ausland')
                        assert (d['units'], d['unit_price_cents'], d['amount_cents'], d['cost_cents']) == (units, price, a, cost)
                        assert (d['inventory_before'], d['inventory_after']) == (goods[f]['units'], goods[f]['units'] - units)
                        assert t['deposit_delta_cents'] == t['loan_delta_cents'] == t['equity_delta_cents'] == 0
                    goods[f]['units'] -= units
                    goods[f]['value'] -= cost
                    cost_of_sales[f] += cost
                    sold[f] += units
                postings += 1
            pos = len(w.journal)
            p = w.foreign.plan
            assert p['opening_cash_cents'] == foreign_open and p['budget_cents'] == expected_budget
            assert p['desired_cents'] == total_desired
            for order in p['orders']:
                seller = order['seller']
                assert order['allocated_cents'] == allocations[seller]
                assert order['funded_units'] == min(desired_orders[seller], allocations[seller] // w.nodes[seller]['price'])
                month_rows = [d for d in w.foreign.deliveries if d['month'] == month and d['seller'] == seller]
                assert sum((d['amount_cents'] for d in month_rows)) <= allocations[seller]
                assert sum((d['units'] for d in month_rows)) <= order['funded_units']
            actual_ids = [d['transaction_id'] for d in w.foreign.deliveries]
            assert len(actual_ids) == len(set(actual_ids)) and set(actual_ids) == export_ids
            assert accounts['ausland'] == cumulative_imports - cumulative_exports
            domestic = sum((v for k, v in accounts.items() if k not in ('bank', 'ausland')))
            assert domestic == 14600000 + cumulative_exports - cumulative_imports + credit_created - principal_repaid - bank_income + bank_distributions
            if phase == 2:
                export_tx = [t for t in new if t['kind'] == 'export_sale']
                domestic_tx = [t for t in new if t['kind'] in ('consumption', 'procurement')]
                if export_tx and domestic_tx:
                    assert max((t['id'] for t in domestic_tx)) < min((t['id'] for t in export_tx))
            assert accounts == {k: n['cash_cents'] for k, n in w.nodes.items()}
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
            sales = sum((t['amount_cents'] for t in tx if t['target'] == f and t['kind'] in ['consumption', 'procurement', 'investment', 'machine_purchase', 'export_sale']))
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
        month_imports = sum((t['amount_cents'] for t in tx if t['kind'] == 'energy'))
        month_exports = sum((t['amount_cents'] for t in tx if t['kind'] == 'export_sale'))
        months.append({'month': month, 'foreign_open_eur': foreign_open / 100, 'foreign_budget_eur': expected_budget / 100, 'imports_eur': month_imports / 100, 'exports_eur': month_exports / 100, 'net_inflow_eur': (month_exports - month_imports) / 100, 'cumulative_imports_eur': cumulative_imports / 100, 'cumulative_exports_eur': cumulative_exports / 100, 'consumption_eur': w.history[-1]['consumption_cents'] / 100, 'employment_relations': w.history[-1]['employment'], 'household_cash_eur': sum((h['cash_cents'] for h in w.households())) / 100, 'government_cash_eur': w.nodes['staat']['cash_cents'] / 100, 'external_cash_eur': w.nodes['ausland']['cash_cents'] / 100, 'companies': company})
    assert w.snapshot()['completed']
    before = len(w.journal)
    try:
        w.step()
        raise AssertionError('25th month accepted')
    except ValueError:
        pass
    assert len(w.journal) == before
    return {'name': name, 'export_orders_units': desired_orders, 'events': [{'month': m, 'event': e} for m, e in events], 'credit_month': credit_month, 'independently_reconstructed_postings': postings, 'all_bridges_passed': True, 'months': months, 'loan_status': w.banking.loan.status, 'loan_interest_paid_eur': w.banking.loan.interest_paid_cents / 100, 'loan_remaining_eur': w.banking.loan.outstanding_cents / 100}

def run_foreign_ports():
    results = []

    def stocks(w, alltag=100, werkstatt=100, reserved=0):
        for key, units, cost in [('alltag', alltag, 6000), ('werkstatt', werkstatt, 9000)]:
            w.nodes[key]['inventory'] = units
            w.nodes[key]['company']['inventory_value_cents'] = units * cost
        w.nodes['werkstatt']['reserved_units'] = reserved

    def check_port(name, w, expected_amount, expected_units, expected_allocations):
        before = {k: n['cash_cents'] for k, n in w.nodes.items()}
        stock_before = {f: w.nodes[f]['inventory'] for f in ['alltag', 'werkstatt']}
        value_before = {f: w.nodes[f]['company']['inventory_value_cents'] for f in ['alltag', 'werkstatt']}
        pos = len(w.journal)
        w.foreign.purchase(w)
        new = w.journal[pos:]
        rows = w.foreign.deliveries
        assert sum((t['amount_cents'] for t in new)) == expected_amount
        assert [o['allocated_cents'] for o in w.foreign.plan['orders']] == expected_allocations
        actual_units = {f: sum((d['units'] for d in rows if d['seller'] == f)) for f in ['alltag', 'werkstatt']}
        assert actual_units == expected_units
        assert w.nodes['ausland']['cash_cents'] == before['ausland'] - expected_amount
        for f in ['alltag', 'werkstatt']:
            units = actual_units[f]
            paid = units * w.nodes[f]['price']
            cost = value_before[f] * units // stock_before[f] if units else 0
            assert w.nodes[f]['cash_cents'] == before[f] + paid
            assert w.nodes[f]['inventory'] == stock_before[f] - units
            assert w.nodes[f]['company']['inventory_value_cents'] == value_before[f] - cost
            for d in [d for d in rows if d['seller'] == f]:
                assert d['cost_cents'] == cost
                t = next((t for t in new if t['id'] == d['transaction_id']))
                assert t['kind'] == 'export_sale' and t['source'] == 'ausland' and (t['target'] == f)
                assert t['deposit_delta_cents'] == t['loan_delta_cents'] == t['equity_delta_cents'] == 0
        assert sum((n['cash_cents'] for n in w.nodes.values())) == sum(before.values())
        after = (len(w.journal), len(w.foreign.deliveries), [(n['cash_cents'], n.get('inventory')) for n in w.nodes.values()])
        w.foreign.purchase(w)
        assert after == (len(w.journal), len(w.foreign.deliveries), [(n['cash_cents'], n.get('inventory')) for n in w.nodes.values()])
        w.check()
        results.append({'name': name, 'opening_foreign_eur': w.foreign.plan['opening_cash_cents'] / 100, 'budget_eur': w.foreign.plan['budget_cents'] / 100, 'allocated_cents': expected_allocations, 'paid_exports_eur': expected_amount / 100, 'delivered_units': actual_units, 'foreign_after_eur': w.nodes['ausland']['cash_cents'] / 100, 'unfunded_units': {f: w.nodes[f]['metrics']['unfunded_units'] for f in ['alltag', 'werkstatt']}, 'funded_unmet_units': {f: w.nodes[f]['metrics']['unmet_units'] for f in ['alltag', 'werkstatt']}, 'duplicate_execution_ignored': True})
    w = World()
    w.step()
    w.phase = 2
    check_port('current_energy_does_not_retrofund_zero_opening', w, 0, {'alltag': 0, 'werkstatt': 0}, [0, 0])
    for name, cash, stock_a, stock_w, reserved, amount, units, alloc in [('partial_720_eur', 72000, 100, 100, 0, 55000, {'alltag': 4, 'werkstatt': 1}, [48000, 24000]), ('fractional_600_01_eur', 60001, 100, 100, 0, 55000, {'alltag': 4, 'werkstatt': 1}, [40000, 20001]), ('rigid_split_100_eur', 10000, 100, 100, 0, 0, {'alltag': 0, 'werkstatt': 0}, [6666, 3334]), ('high_cash_cap', 1000000, 100, 100, 0, 90000, {'alltag': 6, 'werkstatt': 2}, [60000, 30000]), ('funded_but_no_stock', 90000, 0, 0, 0, 0, {'alltag': 0, 'werkstatt': 0}, [60000, 30000]), ('reserved_machine_protected', 90000, 100, 8, 8, 60000, {'alltag': 6, 'werkstatt': 0}, [60000, 30000]), ('partial_stock_no_forced_balance', 90000, 2, 1, 0, 35000, {'alltag': 2, 'werkstatt': 1}, [60000, 30000])]:
        w = World()
        w.pay('staat', 'ausland', cash, 'audit_fixture', 'Expliziter Zahlungseingang im isolierten Prüffall')
        stocks(w, stock_a, stock_w, reserved)
        w.month = 1
        w.phase = 2
        w.foreign.begin_month(w)
        check_port(name, w, amount, units, alloc)
    w = World(export_orders_units={'alltag': 0, 'werkstatt': 0})
    w.pay('staat', 'ausland', 72000, 'audit_fixture', 'Expliziter Zahlungseingang im isolierten Prüffall')
    stocks(w)
    w.month = 1
    w.phase = 2
    w.foreign.begin_month(w)
    check_port('zero_orders', w, 0, {'alltag': 0, 'werkstatt': 0}, [0, 0])
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write repeat results to a new JSON file; existing evidence is never overwritten.')
    args = parser.parse_args()
    if not __debug__:
        parser.error('Assertions must be enabled; do not use Python -O.')
    output = args.output.resolve() if args.output else None
    if output and output.exists():
        parser.error('Output already exists; choose a new path.')
    evidence = json.loads(EVIDENCE.read_text())
    for item in evidence['source_files']:
        actual = hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            parser.error('Source differs from the audited V5 kernel: ' + item['path'])
    runtime = ROOT / 'poc/.runtime/foreign-plausibility'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    sys.path.insert(0, str(ROOT / 'poc'))
    global World
    from world import World
    results = []
    for name, events, credit, orders in SCENARIOS:
        result = run_world(name, events, credit, orders)
        results.append(result)
        print(name, result['independently_reconstructed_postings'], 'postings; all bridges passed', flush=True)
    ports = run_foreign_ports()
    if results != evidence['scenarios'] or ports != evidence['foreign_ports']:
        raise AssertionError('Repeated results differ from the recorded independent V5 audit.')
    count = sum(r['independently_reconstructed_postings'] for r in results)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            'executed_at_utc': datetime.now(timezone.utc).isoformat(),
            'evidence_reference': 'qa/foreign-v5-plausibility.json',
            'source_files': evidence['source_files'],
            'scope': 'Repeat of the recorded V5 audit; not empirical validation.',
            'recorded_results_match': True,
            'scenarios': results, 'foreign_ports': ports,
            'summary': {'worlds': 7, 'world_months': 168, 'phases': 840,
                        'independently_reconstructed_postings': count, 'isolated_ports': len(ports)},
        }, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: 7 worlds, 168 months, {count} postings, {len(ports)} isolated ports; recorded results match.')

if __name__ == '__main__':
    main()
