#!/usr/bin/env python3
"""Repeat the independent V6 audit: eight 24-month worlds and eleven fiscal ports.

Reconstructs integer-cent cash, bank claims, goods/cost/company equity, foreign
trade and state cash/debt/interest. Requires POC Python dependencies.
Illustrative model consistency, not empirical or teaching validation.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'qa/fiscal-v6-plausibility.json'
SCENARIOS = [
 ('no_state_credit', [], None, 0),
 ('baseline', [], None, 5000000),
 ('energy_m3', [(3, 'energy')], None, 5000000),
 ('demand_m3', [(3, 'demand')], None, 5000000),
 ('both_m3', [(3, 'energy'), (3, 'demand')], None, 5000000),
 ('recovery_m13', [(3, 'demand'), (13, 'demand_recovery')], None, 5000000),
 ('machine_credit_m1', [], 1, 5000000),
 ('binding_limit', [(3, 'demand')], None, 10000),
]

def run_world(name, events, credit_month, limit=5000000):
    """Reconstruct cash, bank balance, goods, inventory costs and retained equity from actual transactions."""
    w = World(government_credit_limit_cents=limit)
    export_orders = None
    cumulative_gov_credit = cumulative_gov_principal = charged_interest = paid_interest = 0
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
        state_open = accounts['staat']
        state_debt_open = cumulative_gov_credit - cumulative_gov_principal
        arrears_open = charged_interest - paid_interest
        interest_charge = state_debt_open * 300 // 120000
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
                assert t['source_after'] == accounts[t['source']] and t['target_after'] == accounts[t['target']]
                if t['kind'] == 'government_credit':
                    cumulative_gov_credit += a
                    assert t['source'] == 'bank' and t['target'] == 'staat' and (effect == 'loan_creation')
                    assert cumulative_gov_credit - cumulative_gov_principal <= limit
                if t['kind'] == 'government_principal':
                    cumulative_gov_principal += a
                    assert t['source'] == 'staat' and t['target'] == 'bank' and (effect == 'principal_repayment')
                    assert cumulative_gov_credit - cumulative_gov_principal >= 0
                if t['kind'] == 'government_interest':
                    paid_interest += a
                    assert t['source'] == 'staat' and t['target'] == 'bank' and (effect == 'bank_income')
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
            if phase == 0:
                charged_interest += interest_charge
            assert w.treasury.interest_charged_cents == charged_interest
            assert w.treasury.interest_paid_cents == paid_interest
            assert w.treasury.overdue_interest_cents == charged_interest - paid_interest >= 0
            assert w.treasury.opening_principal_cents == state_debt_open
            assert w.treasury.month_interest_charge_cents == interest_charge
            assert w.treasury.outstanding_cents == cumulative_gov_credit - cumulative_gov_principal
            assert w.nodes['staat']['government_loan_cents'] == cumulative_gov_credit - cumulative_gov_principal
            assert w.nodes['bank']['loan_assets'] == loan_assets
            assert loan_assets == 2400000 + w.banking.loan.outstanding_cents + cumulative_gov_credit - cumulative_gov_principal
            assert w.banking.created == credit_created and w.banking.repaid == principal_repaid
            assert w.banking.interest_received == bank_income and w.banking.distributed == bank_distributions
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
        tx = [t for t in w.journal if t['month'] == month]
        taxes = sum((t['amount_cents'] for t in tx if t['target'] == 'staat' and t['kind'] in ('income_tax', 'profit_tax')))
        primary = sum((t['amount_cents'] for t in tx if t['source'] == 'staat' and t['kind'] in ('wage', 'transfer', 'procurement')))
        interest = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_interest'))
        credit = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_credit'))
        repaid = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_principal'))
        deficit = primary + interest - taxes
        assert accounts['staat'] == state_open + taxes + credit - primary - interest - repaid
        assert cumulative_gov_credit - cumulative_gov_principal == state_debt_open + credit - repaid
        assert charged_interest - paid_interest == arrears_open + interest_charge - interest
        m = w.treasury.history[-1]
        expected = dict(month=month, taxes_cents=taxes, primary_spending_cents=primary, interest_due_cents=arrears_open + interest_charge, interest_paid_cents=interest, cash_deficit_cents=deficit, credit_cents=credit, principal_repaid_cents=repaid, opening_cash_cents=state_open, closing_cash_cents=accounts['staat'], opening_principal_cents=state_debt_open, closing_principal_cents=cumulative_gov_credit - cumulative_gov_principal, unfunded_financing_cents=max(0, deficit - credit + repaid))
        assert m == expected
        assert len(w.treasury.history) == month
        month_bank_interest = sum((t['amount_cents'] for t in tx if t['ledger_effect'] == 'bank_income'))
        month_bank_dividends = sum((t['amount_cents'] for t in tx if t['ledger_effect'] == 'bank_distribution'))
        assert month_bank_interest == month_bank_dividends
        assert accounts['bank'] == 1000000
        final_snapshot = w.snapshot()
        w.treasury.service(w)
        w.treasury.close(w)
        assert w.snapshot() == final_snapshot
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
        months.append({'month': month, 'foreign_open_eur': foreign_open / 100, 'foreign_budget_eur': expected_budget / 100, 'imports_eur': month_imports / 100, 'exports_eur': month_exports / 100, 'net_inflow_eur': (month_exports - month_imports) / 100, 'cumulative_imports_eur': cumulative_imports / 100, 'cumulative_exports_eur': cumulative_exports / 100, 'consumption_eur': w.history[-1]['consumption_cents'] / 100, 'employment_relations': w.history[-1]['employment'], 'household_cash_eur': sum((h['cash_cents'] for h in w.households())) / 100, 'government_cash_eur': w.nodes['staat']['cash_cents'] / 100, 'external_cash_eur': w.nodes['ausland']['cash_cents'] / 100, 'companies': company, 'fiscal': expected})
    assert w.snapshot()['completed']
    before = len(w.journal)
    try:
        w.step()
        raise AssertionError('25th month accepted')
    except ValueError:
        pass
    assert len(w.journal) == before
    return {'name': name, 'government_credit_limit_cents': limit, 'export_orders_units': desired_orders, 'events': [{'month': m, 'event': e} for m, e in events], 'credit_month': credit_month, 'independently_reconstructed_postings': postings, 'all_bridges_passed': True, 'months': months, 'government_interest_paid_eur': paid_interest / 100, 'government_interest_charged_eur': charged_interest / 100, 'government_outstanding_eur': (cumulative_gov_credit - cumulative_gov_principal) / 100, 'government_interest_arrears_eur': (charged_interest - paid_interest) / 100, 'loan_status': w.banking.loan.status, 'loan_interest_paid_eur': w.banking.loan.interest_paid_cents / 100, 'loan_remaining_eur': w.banking.loan.outstanding_cents / 100}

def run_fiscal_ports():
    results = []

    def begin(w, month, phase=0):
        w.month = month
        w.phase = phase
        w.month_open = {k: n['cash_cents'] for k, n in w.nodes.items()}
        w.treasury.begin_month(w)

    def drain(w):
        w.pay('staat', 'h1', w.nodes['staat']['cash_cents'], 'audit_fixture', 'Explicit test transfer')

    def check(name, w, extra=None):
        a = dict(w.initial)
        loans = 2400000
        debt = 0
        interest = 0
        for t in w.journal:
            amount = t['amount_cents']
            source = t['source']
            target = t['target']
            effect = t['ledger_effect']
            assert t['source_before'] == a[source] and t['target_before'] == a[target]
            deposits = sum((v for k, v in a.items() if k != 'bank'))
            equity = a['bank']
            oldloans = loans
            if effect == 'loan_creation':
                a[target] += amount
                loans += amount
            elif effect == 'principal_repayment':
                a[source] -= amount
                loans -= amount
            else:
                a[source] -= amount
                a[target] += amount
            if t['kind'] == 'government_credit':
                debt += amount
            if t['kind'] == 'government_principal':
                debt -= amount
            if t['kind'] == 'government_interest':
                interest += amount
            assert 0 <= debt <= w.treasury.credit_limit_cents
            assert t['source_after'] == a[source] and t['target_after'] == a[target]
            newdeposits = sum((v for k, v in a.items() if k != 'bank'))
            assert t['deposit_delta_cents'] == newdeposits - deposits
            assert t['loan_delta_cents'] == loans - oldloans and t['equity_delta_cents'] == a['bank'] - equity
            assert 13200000 + loans == newdeposits + a['bank']
        assert a == {k: n['cash_cents'] for k, n in w.nodes.items()}
        assert debt == w.treasury.outstanding_cents == w.nodes['staat']['government_loan_cents']
        assert interest == w.treasury.interest_paid_cents
        assert w.treasury.interest_charged_cents - interest == w.treasury.overdue_interest_cents >= 0
        assert loans == w.nodes['bank']['loan_assets']
        w.check()
        r = dict(name=name, postings=len(w.journal), state_cash_cents=a['staat'], state_debt_cents=debt, interest_charged_cents=w.treasury.interest_charged_cents, interest_paid_cents=interest, interest_arrears_cents=w.treasury.overdue_interest_cents, credit_created_cents=w.treasury.credit_created_cents, principal_repaid_cents=w.treasury.principal_repaid_cents)
        if extra:
            r.update(extra)
        results.append(r)
    w = World()
    begin(w, 1)
    w.treasury.issue(w, 100000)
    w.treasury.service(w)
    assert w.treasury.interest_charged_cents == 0
    begin(w, 2)
    w.treasury.service(w)
    before = w.snapshot()
    w.treasury.service(w)
    assert before == w.snapshot() and w.treasury.interest_paid_cents == 250
    w.treasury.repay(w, 100000)
    begin(w, 3)
    w.treasury.service(w)
    assert w.treasury.month_interest_charge_cents == 0 and w.treasury.interest_paid_cents == 250
    check('opening_debt_only_and_no_double_charge', w)
    w = World()
    drain(w)
    w.step()
    assert w.treasury.outstanding_cents == 480000
    for _ in range(4):
        w.step()
    tx = w.journal
    credit = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_credit'))
    repaid = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_principal'))
    assert credit - repaid == 241360 and w.nodes['staat']['cash_cents'] == 0
    before = w.snapshot()
    w.treasury.close(w)
    w.treasury.service(w)
    assert before == w.snapshot()
    check('interim_credit_and_late_tax_net_once', w)
    w = World()
    begin(w, 1, 4)
    w.treasury.issue(w, 100000)
    w.pay('h1', 'staat', 200000, 'income_tax', 'Test tax')
    w.treasury.close(w)
    assert w.treasury.outstanding_cents == 0 and w.nodes['staat']['cash_cents'] == 8200000 and (w.nodes['bank']['cash_cents'] == 1000000)
    check('surplus_repay_capped_at_debt', w)
    w = World(government_credit_limit_cents=100000)
    begin(w, 1)
    w.treasury.issue(w, 100000)
    drain(w)
    begin(w, 2)
    w.treasury.service(w)
    before = w.snapshot()
    w.treasury.service(w)
    assert before == w.snapshot()
    begin(w, 3)
    w.treasury.service(w)
    assert w.treasury.interest_charged_cents == 500 and w.treasury.overdue_interest_cents == 500 and (w.treasury.outstanding_cents == 100000)
    check('binding_limit_arrears_without_compound_or_double_charge', w)
    w = World(government_credit_limit_cents=100000)
    begin(w, 1)
    w.treasury.issue(w, 100000)
    drain(w)
    begin(w, 2)
    w.treasury.service(w)
    w.pay('h1', 'staat', 10000, 'income_tax', 'Late tax')
    w.phase = 4
    w.treasury.close(w)
    assert w.treasury.interest_paid_cents == 250 and w.treasury.overdue_interest_cents == 0 and (w.treasury.outstanding_cents == 90250)
    rows = [t for t in w.journal if t['month'] == 2]
    assert next((t['id'] for t in rows if t['kind'] == 'government_interest')) < next((t['id'] for t in rows if t['kind'] == 'government_principal'))
    check('late_tax_pays_arrears_before_principal', w)
    w = World()
    drain(w)
    begin(w, 1, 2)
    assert w.buy('staat', 'alltag', 120000, 'procurement') == 0 and w.treasury.credit_created_cents == 0
    check('missing_goods_no_procurement_credit', w)
    w = World()
    drain(w)
    begin(w, 1, 2)
    n = w.nodes['alltag']
    n['inventory'] = 5
    n['reserved_units'] = 3
    n['company']['inventory_value_cents'] = 50000
    assert w.buy('staat', 'alltag', 120000, 'procurement') == 2
    assert n['inventory'] == 3 and n['company']['inventory_value_cents'] == 30000 and (w.treasury.outstanding_cents == 20000)
    assert w.buy('staat', 'alltag', 120000, 'procurement') == 0 and w.treasury.outstanding_cents == 20000
    check('procurement_finances_only_free_delivered_goods', w, {'delivered_units': 2, 'reserved_units_remaining': 3})
    w = World(government_credit_limit_cents=10000)
    drain(w)
    begin(w, 1, 2)
    n = w.nodes['alltag']
    n['inventory'] = 2
    n['company']['inventory_value_cents'] = 12000
    assert w.buy('staat', 'alltag', 120000, 'procurement') == 1 and n['inventory'] == 1
    assert w.treasury.outstanding_cents == 10000 and w.nodes['staat']['cash_cents'] == 0
    check('partial_procurement_at_credit_limit', w, {'delivered_units': 1})
    w = World(government_credit_limit_cents=0)
    drain(w)
    w.step()
    unpaid = sum((o['amount_cents'] for o in w.obligations if o['source'] == 'staat' and o['kind'] == 'wage'))
    assert unpaid == 480000 and w.treasury.outstanding_cents == 0 and (w.nodes['staat']['cash_cents'] == 0)
    check('no_cash_no_credit_public_wage_arrears', w, {'unpaid_wages_cents': unpaid})
    w = World()
    w.pay('bank', 'h1', 1000000, 'audit_fixture', 'Explicit equity distribution')
    begin(w, 1)
    assert w.treasury.issue(w, 100000) == 0 and w.treasury.outstanding_cents == 0
    check('zero_bank_equity_blocks_credit', w)
    w = World()
    for _ in range(10):
        w.step()
    tx = [t for t in w.journal if t['month'] == 2]
    govt = sum((t['amount_cents'] for t in tx if t['kind'] == 'government_interest'))
    income = sum((t['amount_cents'] for t in tx if t['ledger_effect'] == 'bank_income'))
    dividends = sum((t['amount_cents'] for t in tx if t['ledger_effect'] == 'bank_distribution'))
    assert govt == 603 and income == dividends == 4603 and (w.nodes['bank']['cash_cents'] == 1000000)
    check('government_interest_reaches_household_bank_owners', w, {'month2_bank_income_cents': income, 'month2_bank_dividends_cents': dividends})
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write this repeat to a new JSON file; existing evidence is never overwritten.')
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
            parser.error('Source differs from the audited V6 kernel: ' + item['path'])
    runtime = ROOT / 'poc/.runtime/fiscal-plausibility'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    sys.path.insert(0, str(ROOT / 'poc'))
    global World
    from world import World
    results = []
    for name, events, credit, limit in SCENARIOS:
        result = run_world(name, events, credit, limit)
        results.append(result)
        print(name, result['independently_reconstructed_postings'], 'postings; all bridges passed', flush=True)
    ports = run_fiscal_ports()
    if results != evidence['scenarios'] or ports != evidence['fiscal_ports']:
        raise AssertionError('Repeated results differ from the recorded independent V6 audit.')
    count = sum(r['independently_reconstructed_postings'] for r in results)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            'executed_at_utc': datetime.now(timezone.utc).isoformat(),
            'evidence_reference': 'qa/fiscal-v6-plausibility.json',
            'source_files': evidence['source_files'],
            'scope': 'Repeat of the recorded V6 audit; not empirical validation.',
            'recorded_results_match': True,
            'scenarios': results, 'fiscal_ports': ports,
            'summary': {'worlds': 8, 'world_months': 192, 'phases': 960,
                        'independently_reconstructed_postings': count, 'isolated_ports': len(ports)},
        }, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: 8 worlds, 192 months, {count} postings, {len(ports)} isolated ports; recorded results match.')

if __name__ == '__main__':
    main()
