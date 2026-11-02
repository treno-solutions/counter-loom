#!/usr/bin/env python3
"""Repeat the independent V7 audit: nine 24-month worlds and eleven rate ports.

Reconstructs integer-cent cash, bank claims, goods/cost/company equity, foreign
trade and state cash/debt/interest and credit-rate contracts. Requires POC Python dependencies.
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
EVIDENCE = ROOT / 'qa/rates-v7-plausibility.json'
SCENARIOS = [('baseline', [], None, []), ('hike_m2', [], None, [(2, 400)]), ('cut_m2', [], None, [(2, 100)]), ('reversal_m8', [], None, [(2, 400), (8, 100)]), ('zero_m2', [], None, [(2, 0)]), ('hike_energy', [(3, 'energy')], None, [(2, 400)]), ('hike_demand', [(3, 'demand')], None, [(2, 400)]), ('machine_before_hike', [], 1, [(2, 400)]), ('machine_after_hike', [], 3, [(2, 400)])]

def run_world(name, events, credit_month, policy_events=None):
    """Reconstruct cash, bank balance, goods, inventory costs and retained equity from actual transactions."""
    limit = 5000000
    w = World()
    policy_events = policy_events or []
    tranches = []
    locked_machine_rate = None
    machine_principal_created = machine_principal_repaid = machine_interest_charged = machine_interest_paid = 0
    machine_delivery_month = None
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
        for when, rate in policy_events:
            if month == when:
                before_journal = len(w.journal)
                w.monetary.queue(w, rate)
                assert len(w.journal) == before_journal
        policy = 200
        previous_policy = 200
        for when, rate in policy_events:
            if when <= month:
                policy = rate
            if when < month:
                previous_policy = rate
        expected_rates = {'alltag': previous_policy, 'werkstatt': 200}
        opening = {f: dict(goods[f]) for f in goods}
        foreign_open = accounts['ausland']
        state_open = accounts['staat']
        state_debt_open = cumulative_gov_credit - cumulative_gov_principal
        arrears_open = charged_interest - paid_interest
        interest_basis = [dict(tranche_id=t['tranche_id'], principal_cents=t['outstanding_cents'], annual_rate_bps=t['annual_rate_bps'], interest_cents=t['outstanding_cents'] * t['annual_rate_bps'] // 120000) for t in tranches if t['outstanding_cents']]
        interest_charge = sum((b['principal_cents'] * b['annual_rate_bps'] for b in interest_basis)) // 120000
        ranked = sorted(interest_basis, key=lambda b: (-(b['principal_cents'] * b['annual_rate_bps'] % 120000), b['tranche_id']))
        for b in ranked[:interest_charge - sum((b['interest_cents'] for b in interest_basis))]:
            b['interest_cents'] += 1
        desired_cents = {f: desired_orders[f] * w.nodes[f]['price'] for f in goods}
        total_desired = sum(desired_cents.values())
        expected_budget = min(foreign_open, total_desired)
        allocated_alltag = expected_budget * desired_cents['alltag'] // total_desired if total_desired else 0
        allocations = {'alltag': allocated_alltag, 'werkstatt': expected_budget - allocated_alltag}
        loan_open_principal = machine_principal_created - machine_principal_repaid
        assert loan_open_principal == w.banking.loan.outstanding_cents
        loan_open_delivered = machine_delivery_month
        assert loan_open_delivered == w.banking.loan.delivery_month
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
                    assert n['company']['plan']['interest_due_cents'] == n['loan'] * expected_rates[f] // 120000
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
                if t['kind'] == 'machine_credit':
                    assert locked_machine_rate is None
                    locked_machine_rate = policy + 400
                    machine_principal_created += a
                if t['kind'] == 'machine_principal':
                    machine_principal_repaid += a
                if t['kind'] == 'machine_interest':
                    machine_interest_paid += a
                if t['kind'] == 'machine_purchase':
                    machine_delivery_month = month
                if t['kind'] == 'government_credit':
                    tranches.append(dict(tranche_id=len(tranches) + 1, transaction_id=t['id'], issue_month=month, original_cents=a, outstanding_cents=a, annual_rate_bps=policy + 100, policy_rate_at_issue_bps=policy, spread_bps=100))
                    cumulative_gov_credit += a
                    assert t['source'] == 'bank' and t['target'] == 'staat' and (effect == 'loan_creation')
                    assert cumulative_gov_credit - cumulative_gov_principal <= limit
                if t['kind'] == 'government_principal':
                    left = a
                    for tranche in tranches:
                        take = min(left, tranche['outstanding_cents'])
                        tranche['outstanding_cents'] -= take
                        left -= take
                    assert left == 0
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
                if loan_open_delivered is not None and month > loan_open_delivered:
                    machine_interest_charged += loan_open_principal * locked_machine_rate // 120000
            assert w.monetary.rate_bps == policy
            assert w.nodes['alltag']['loan_rate_bps'] == previous_policy
            assert w.nodes['alltag']['loan_next_rate_bps'] == policy
            assert w.nodes['werkstatt']['loan_rate_bps'] == w.nodes['werkstatt']['loan_next_rate_bps'] == 200
            assert w.monetary.machine_offer() == policy + 400 and w.monetary.state_offer(w) == policy + 100
            assert w.treasury.tranches == tranches
            assert w.treasury.month_interest_basis == interest_basis
            assert w.banking.loan.outstanding_cents == machine_principal_created - machine_principal_repaid
            assert w.banking.loan.interest_charged_cents == machine_interest_charged
            assert w.banking.loan.interest_paid_cents == machine_interest_paid
            assert w.banking.loan.overdue_interest_cents == machine_interest_charged - machine_interest_paid
            if locked_machine_rate is not None:
                assert w.banking.loan.annual_rate_bps == locked_machine_rate
                assert w.banking.loan.policy_rate_at_issue_bps == locked_machine_rate - 400
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
        expected = dict(month=month, taxes_cents=taxes, primary_spending_cents=primary, interest_due_cents=arrears_open + interest_charge, interest_paid_cents=interest, cash_deficit_cents=deficit, credit_cents=credit, principal_repaid_cents=repaid, opening_cash_cents=state_open, closing_cash_cents=accounts['staat'], opening_principal_cents=state_debt_open, closing_principal_cents=cumulative_gov_credit - cumulative_gov_principal, unfunded_financing_cents=max(0, deficit - credit + repaid), interest_basis=interest_basis, new_interest_charge_cents=interest_charge)
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
            interest_due = n['loan'] * expected_rates[f] // 120000 + (loan_open_principal * locked_machine_rate // 120000 if f == 'alltag' and loan_open_delivered is not None and (month > loan_open_delivered) else 0)
            profit = sales - cost_of_sales[f] - m['idle_cost'] - m['unpaid_wages'] - interest_due
            tax_due = max(0, profit) * 20 // 100
            dividends = sum((t['amount_cents'] for t in tx if t['source'] == f and t['kind'] == 'company_dividend'))
            assert m['sales'] == sales and m['cost_of_sales'] == cost_of_sales[f]
            assert profit == r['profit_before_tax_cents'] and tax_due == r['tax_due_cents']
            assert dividends == r['distribution_cents'] and dividends <= max(0, profit - tax_due) // 2
            assert r['retained_result_cents'] == profit - tax_due - dividends
            demand = (c['forecast_milli'] + 500) // 1000
            energy = (500 if f == 'alltag' else 900) * w.energy_multiplier
            next_rate = policy if f == 'alltag' else 200
            next_service = 0
            if f == 'alltag' and machine_delivery_month is not None and (machine_principal_created > machine_principal_repaid):
                principal = machine_principal_created - machine_principal_repaid
                next_service = machine_interest_charged - machine_interest_paid + principal * locked_machine_rate // 120000
                next_service += max(0, min(principal, min(12, month + 1 - machine_delivery_month) * 10000 - machine_principal_repaid))
            needed = (max(0, demand - n['capital'] * 4) + n['productivity'] - 1) // n['productivity']
            affordable = max(0, demand * (n['price'] - energy) - n['loan'] * next_rate // 120000 - next_service) // 240000
            expected_desired = min(4, needed, affordable)
            expected_reserve = 2 * max(expected_desired, staff_open[f]) * 240000 + demand * energy + n['loan'] * next_rate // 120000 + next_service
            assert r['desired_staff'] == expected_desired and r['reserve_cents'] == expected_reserve
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
        months.append({'month': month, 'foreign_open_eur': foreign_open / 100, 'foreign_budget_eur': expected_budget / 100, 'imports_eur': month_imports / 100, 'exports_eur': month_exports / 100, 'net_inflow_eur': (month_exports - month_imports) / 100, 'cumulative_imports_eur': cumulative_imports / 100, 'cumulative_exports_eur': cumulative_exports / 100, 'consumption_eur': w.history[-1]['consumption_cents'] / 100, 'employment_relations': w.history[-1]['employment'], 'household_cash_eur': sum((h['cash_cents'] for h in w.households())) / 100, 'government_cash_eur': w.nodes['staat']['cash_cents'] / 100, 'external_cash_eur': w.nodes['ausland']['cash_cents'] / 100, 'companies': company, 'fiscal': expected, 'policy_rate_bps': policy, 'variable_rate_bps': previous_policy, 'fixed_rate_bps': 200, 'machine_contract_rate_bps': locked_machine_rate})
    assert w.snapshot()['completed']
    before = len(w.journal)
    try:
        w.step()
        raise AssertionError('25th month accepted')
    except ValueError:
        pass
    assert len(w.journal) == before
    return {'name': name, 'policy_events': [{'month': m, 'annual_rate_bps': r} for m, r in policy_events], 'government_credit_limit_cents': limit, 'export_orders_units': desired_orders, 'events': [{'month': m, 'event': e} for m, e in events], 'credit_month': credit_month, 'independently_reconstructed_postings': postings, 'all_bridges_passed': True, 'months': months, 'government_interest_paid_eur': paid_interest / 100, 'government_interest_charged_eur': charged_interest / 100, 'government_outstanding_eur': (cumulative_gov_credit - cumulative_gov_principal) / 100, 'government_interest_arrears_eur': (charged_interest - paid_interest) / 100, 'state_tranches': tranches, 'loan_status': w.banking.loan.status, 'loan_interest_paid_eur': w.banking.loan.interest_paid_cents / 100, 'loan_remaining_eur': w.banking.loan.outstanding_cents / 100}

def run_rate_ports():
    from world import world_request, WORLDS
    results = []

    def begin(w, month, rate=None):
        if rate is not None:
            w.monetary.queue(w, rate)
        w.month = month
        w.phase = 0
        w.month_open = {k: n['cash_cents'] for k, n in w.nodes.items()}
        w.monetary.begin_month(w)
        w.treasury.begin_month(w)

    def check(name, w, schedule=None, extra=None, spread=100):
        schedule = schedule or {}
        a = dict(w.initial)
        loans = 2400000
        tranches = []
        machine_rate = None
        for t in w.journal:
            amount = t['amount_cents']
            source = t['source']
            target = t['target']
            effect = t['ledger_effect']
            assert (t['source_before'], t['target_before']) == (a[source], a[target])
            dep = sum((v for k, v in a.items() if k != 'bank'))
            eq = a['bank']
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
            assert (t['source_after'], t['target_after']) == (a[source], a[target])
            newdep = sum((v for k, v in a.items() if k != 'bank'))
            assert (t['deposit_delta_cents'], t['loan_delta_cents'], t['equity_delta_cents']) == (newdep - dep, loans - oldloans, a['bank'] - eq)
            assert 13200000 + loans == newdep + a['bank']
            policy = 200
            for month, rate in sorted(schedule.items()):
                if month <= t['month']:
                    policy = rate
            if t['kind'] == 'government_credit':
                tranches.append(dict(tranche_id=len(tranches) + 1, transaction_id=t['id'], issue_month=t['month'], original_cents=amount, outstanding_cents=amount, annual_rate_bps=max(0, policy + spread), policy_rate_at_issue_bps=policy, spread_bps=spread))
            if t['kind'] == 'government_principal':
                left = amount
                for row in tranches:
                    take = min(left, row['outstanding_cents'])
                    row['outstanding_cents'] -= take
                    left -= take
                assert left == 0
            if t['kind'] == 'machine_credit':
                machine_rate = policy + 400
        assert a == {k: n['cash_cents'] for k, n in w.nodes.items()}
        assert loans == w.nodes['bank']['loan_assets'] and tranches == w.treasury.tranches
        if machine_rate is not None:
            assert w.banking.loan.annual_rate_bps == machine_rate
        w.check()
        r = dict(name=name, postings=len(w.journal), policy_rate_bps=w.monetary.rate_bps, variable_rate_bps=w.nodes['alltag']['loan_rate_bps'], fixed_rate_bps=w.nodes['werkstatt']['loan_rate_bps'], state_tranches=tranches, interest_basis=w.treasury.month_interest_basis, new_state_interest_cents=w.treasury.month_interest_charge_cents, state_interest_arrears_cents=w.treasury.overdue_interest_cents, machine_rate_at_issue_bps=machine_rate)
        if extra:
            r.update(extra)
        results.append(r)
    w = World()
    w.monetary.queue(w, 400)
    w.monetary.queue(w, 300)
    assert w.monetary.pending_rate_bps == 300
    assert not w.journal and w.monetary.rate_bps == 200
    w.monetary.queue(w, 200)
    assert w.monetary.pending_rate_bps is None
    w.step()
    assert w.monetary.changes == [] and w.monetary.rate_bps == 200
    check('queued_replacement_and_cancellation_no_money', w)
    w = World()
    for rate in (-1, 1001, True, 1.5, '400', None):
        before = w.snapshot()
        try:
            w.monetary.queue(w, rate)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid rate accepted')
        assert before == w.snapshot()
    w.monetary.queue(w, 1000)
    w.step()
    assert w.monetary.rate_bps == 1000 and w.nodes['alltag']['loan_rate_bps'] == 200
    begin(w, 24)
    before = w.snapshot()
    try:
        w.monetary.queue(w, 0)
    except ValueError:
        pass
    else:
        raise AssertionError('Final-month queue accepted')
    assert before == w.snapshot()
    check('input_bounds_and_final_month_atomic_rejection', w, {1: 1000})
    w = World()
    WORLDS[w.id] = w
    try:
        body = dict(world_id=w.id, revision=w.revision, annual_rate_bps=400)
        s = world_request('rate', body)
        assert s['monetary_policy']['pending_rate_bps'] == 400
        before = w.snapshot()
        try:
            world_request('rate', body)
        except ValueError:
            pass
        else:
            raise AssertionError('Stale revision accepted')
        assert w.snapshot() == before
        try:
            world_request('rate', dict(world_id=w.id, revision=w.revision, event='rate'))
        except ValueError:
            pass
        else:
            raise AssertionError('Missing rate accepted')
        assert w.snapshot() == before and (not w.journal)
        check('rate_api_revision_and_required_field_guards', w)
    finally:
        WORLDS.pop(w.id, None)
    w = World()
    for _ in range(5):
        w.step()
    w.monetary.queue(w, 400)
    for _ in range(5):
        w.step()
    assert w.nodes['alltag']['loan_rate_bps'] == 200 and w.nodes['alltag']['loan_next_rate_bps'] == 400
    assert w.nodes['alltag']['company']['plan']['interest_due_cents'] == 2000
    w.step()
    assert w.nodes['alltag']['company']['plan']['interest_due_cents'] == 4000
    assert w.nodes['werkstatt']['company']['plan']['interest_due_cents'] == 2000
    check('policy_boundary_and_variable_lag', w, {2: 400})
    w = World()
    w.banking.request(w)
    begin(w, 1)
    w.phase = 3
    assert w.banking.originate(w) and w.banking.loan.status == 'requested' and (not w.journal)
    begin(w, 2, 400)
    w.phase = 3
    n = w.nodes['werkstatt']
    n['inventory'] = 8
    n['company']['inventory_value_cents'] = 72000
    assert w.banking.originate(w) and w.banking.loan.annual_rate_bps == 800
    w.phase = 4
    w.banking.deliver(w)
    begin(w, 3, 0)
    w.banking.service(w)
    assert w.banking.loan.annual_rate_bps == 800 and w.monetary.machine_offer() == 400 and (w.banking.loan.interest_paid_cents == 800)
    check('waiting_request_locks_only_at_credit_then_stays_fixed', w, {2: 400, 3: 0}, {'machine_interest_paid_cents': 800})
    w = World()
    begin(w, 1)
    w.treasury.issue(w, 100001)
    begin(w, 2, 400)
    w.treasury.issue(w, 200003)
    w.treasury.repay(w, 150000)
    assert [t['outstanding_cents'] for t in w.treasury.tranches] == [0, 150004]
    begin(w, 3, 0)
    assert w.treasury.month_interest_charge_cents == 625
    assert w.treasury.month_interest_basis == [dict(tranche_id=2, principal_cents=150004, annual_rate_bps=500, interest_cents=625)]
    check('mixed_fixed_tranches_fifo_and_post_cut_basis', w, {2: 400, 3: 0})
    w = World()
    begin(w, 1)
    for _ in range(3):
        w.treasury.issue(w, 200)
    begin(w, 2)
    assert w.treasury.month_interest_charge_cents == 1
    assert [b['interest_cents'] for b in w.treasury.month_interest_basis] == [1, 0, 0]
    check('aggregate_rounding_preserves_cent_and_stable_tie_break', w)
    w = World()
    begin(w, 1)
    w.treasury.issue(w, 199)
    begin(w, 2, 400)
    w.treasury.issue(w, 199)
    begin(w, 3, 0)
    w.treasury.issue(w, 401)
    begin(w, 4)
    assert [t['annual_rate_bps'] for t in w.treasury.tranches] == [300, 500, 100]
    assert w.treasury.month_interest_charge_cents == 1
    assert [b['interest_cents'] for b in w.treasury.month_interest_basis] == [0, 1, 0]
    check('mixed_rate_largest_fraction_not_oldest_tranche', w, {2: 400, 3: 0})
    w = World(government_credit_limit_cents=100000)
    begin(w, 1)
    w.treasury.issue(w, 100000)
    w.pay('staat', 'h1', w.nodes['staat']['cash_cents'], 'audit_fixture', 'Explicit transfer')
    begin(w, 2, 1000)
    w.treasury.service(w)
    assert w.treasury.overdue_interest_cents == 250
    begin(w, 3, 0)
    w.treasury.service(w)
    assert w.treasury.overdue_interest_cents == 500 and w.treasury.interest_charged_cents == 500
    before = w.snapshot()
    w.treasury.service(w)
    assert before == w.snapshot()
    check('old_state_arrears_and_fixed_rate_survive_hike_and_cut', w, {2: 1000, 3: 0})
    w = World()
    w.pay('alltag', 'h1', w.nodes['alltag']['cash_cents'], 'audit_fixture', 'Explicit transfer')
    w.step()
    old = [o.copy() for o in w.obligations if o['source'] == 'alltag' and o['kind'] == 'interest']
    assert old[0]['amount_cents'] == 2000
    w.monetary.queue(w, 400)
    for _ in range(10):
        w.step()
    assert w.nodes['alltag']['loan_rate_bps'] == 400
    assert [o for o in w.obligations if o['month'] == 1 and o['source'] == 'alltag' and (o['kind'] == 'interest')] == old
    check('old_variable_interest_claim_not_repriced', w, {2: 400})
    w = World(government_annual_rate_bps=100)
    begin(w, 1)
    w.treasury.issue(w, 100000)
    assert w.treasury.tranches[0]['annual_rate_bps'] == 100
    begin(w, 2, 0)
    w.treasury.issue(w, 100000)
    assert w.monetary.state_offer(w) == 0 and w.treasury.tranches[1]['annual_rate_bps'] == 0
    begin(w, 3)
    assert w.treasury.month_interest_charge_cents == 83
    check('custom_negative_spread_offer_clamped_at_zero', w, {2: 0}, spread=-100)
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
            parser.error('Source differs from the audited V7 kernel: ' + item['path'])
    runtime = ROOT / 'poc/.runtime/rates-plausibility'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    sys.path.insert(0, str(ROOT / 'poc'))
    global World
    from world import World
    results = []
    for name, events, credit, policy in SCENARIOS:
        result = run_world(name, events, credit, policy)
        results.append(result)
        print(name, result['independently_reconstructed_postings'], 'postings; all bridges passed', flush=True)
    ports = run_rate_ports()
    if results != evidence['scenarios'] or ports != evidence['rate_ports']:
        raise AssertionError('Repeated results differ from the recorded independent V7 audit.')
    count = sum((r['independently_reconstructed_postings'] for r in results))
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({'executed_at_utc': datetime.now(timezone.utc).isoformat(), 'evidence_reference': 'qa/rates-v7-plausibility.json', 'source_files': evidence['source_files'], 'scope': 'Repeat of the recorded V7 audit; not empirical validation.', 'recorded_results_match': True, 'scenarios': results, 'rate_ports': ports, 'summary': {'worlds': 9, 'world_months': 216, 'phases': 1080, 'independently_reconstructed_postings': count, 'isolated_ports': len(ports)}}, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: 9 worlds, 216 months, {count} postings, {len(ports)} isolated ports; recorded results match.')

if __name__ == '__main__':
    main()
