#!/usr/bin/env python3
"""Reproduce the independent V3 bank-plausibility audit already recorded in qa/.

Runs the same nine 240-month worlds and six isolated 24-month payment paths.
Requires the POC Python dependencies. Source hashes must match the recorded V3
kernel; original evidence is never overwritten. No UI, network or LLM is used.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'qa/bank-plausibility-review-2026-11-02.json'

def run_world(name, events=None, credit_month=None, months=240):
    """Reconstruct all counterpart accounts and bank balances from individual postings."""
    w = World()
    accounts = dict(w.initial)
    loans = 2400000
    reserves = 13200000
    pos = 0
    checkpoints = []
    bank_checked = 0
    for month in range(1, months + 1):
        if credit_month == month:
            w.banking.request(w)
        for (when, e) in events or []:
            if month == when:
                w.queue(e)
        contracts = {worker for n in w.nodes.values() for worker in n.get('employees', [])}
        for _ in range(5):
            w.step()
            for t in w.journal[pos:]:
                amount = t['amount_cents']
                effect = t['ledger_effect']
                old_loans = loans
                old_equity = accounts['bank']
                old_deposits = sum((v for (k, v) in accounts.items() if k != 'bank'))
                assert t['source_before'] == accounts[t['source']]
                assert t['target_before'] == accounts[t['target']]
                if effect == 'loan_creation':
                    accounts[t['target']] += amount
                    loans += amount
                elif effect == 'principal_repayment':
                    accounts[t['source']] -= amount
                    loans -= amount
                else:
                    accounts[t['source']] -= amount
                    accounts[t['target']] += amount
                assert accounts[t['source']] == t['source_after']
                assert accounts[t['target']] == t['target_after']
                deposits = sum((v for (k, v) in accounts.items() if k != 'bank'))
                equity = accounts['bank']
                assert reserves + loans == deposits + equity
                assert t['deposit_delta_cents'] == deposits - old_deposits
                assert t['loan_delta_cents'] == loans - old_loans
                assert t['equity_delta_cents'] == equity - old_equity
                for (b, l, d, e) in [(t['bank_before'], old_loans, old_deposits, old_equity), (t['bank_after'], loans, deposits, equity)]:
                    assert b['reserves_cents'] == reserves and b['loan_assets_cents'] == l and (b['customer_deposits_cents'] == d) and (b['equity_cents'] == e)
                    assert b['assets_cents'] == reserves + l and b['liabilities_and_equity_cents'] == d + e
                bank_checked += 1
            pos = len(w.journal)
            assert accounts == {k: n['cash_cents'] for (k, n) in w.nodes.items()}
        if month in [1, 6, 12, 13, 24, 36, 60, 97, 120, 240]:
            h = w.households()
            loan = w.banking.loan
            checkpoints.append({'month': month, 'customer_deposits_eur': sum((v for (k, v) in accounts.items() if k != 'bank')) / 100, 'equity_eur': accounts['bank'] / 100, 'cash_eur': {s: sum((n['cash_cents'] for n in w.nodes.values() if n['sector'] == s)) / 100 for s in ['households', 'firms', 'government', 'bank', 'external']}, 'consumption_eur': w.history[-1]['consumption_cents'] / 100, 'inventory': {f: w.nodes[f]['inventory'] for f in ['alltag', 'werkstatt']}, 'staff': {f: len(w.nodes[f]['employees']) for f in ['alltag', 'werkstatt']}, 'positions_at_wage_phase': len(contracts), 'positions_after_review': sum((x['employer'] is not None for x in h)), 'wage_paid_households': sum((x['metrics']['income'] - x['metrics']['transfers'] > 0 for x in h)), 'loan_status': loan.status, 'loan_balance_eur': loan.outstanding_cents / 100, 'loan_principal_paid_eur': loan.principal_paid_cents / 100, 'loan_interest_paid_eur': loan.interest_paid_cents / 100, 'loan_interest_charged_eur': loan.interest_charged_cents / 100, 'loan_overdue_interest_eur': loan.overdue_interest_cents / 100, 'loan_overdue_principal_eur': loan.overdue_principal_cents / 100})
    return {'name': name, 'events': [{'month': m, 'event': e} for (m, e) in events or []], 'credit_request_month': credit_month, 'months': months, 'independent_posting_count': bank_checked, 'independent_bank_balance_reconstruction_passed': True, 'snapshots': checkpoints, 'loan_issue_month': w.banking.loan.issue_month, 'loan_delivery_month': w.banking.loan.delivery_month, 'loan_interest_payments_cents': [t['amount_cents'] for t in w.journal if t['kind'] == 'machine_interest'], 'loan_principal_payments_cents': [t['amount_cents'] for t in w.journal if t['kind'] == 'machine_principal']}

def run_servicing_ports():
    paths = {'punctual': [10600] * 24, 'two_missed_then_catchup': [0, 0, 33000] + [10600] * 21, 'small_partial_payments': [500, 1500, 5000, 0, 200, 8000, 1000, 20000, 30000, 0, 60000] + [10600] * 13, 'no_payments': [0] * 24, 'late_large_payment': [0] * 18 + [150000] + [0] * 5, 'alternating': [0, 22000] * 12}
    results = []
    for (name, plan) in paths.items():
        w = World()
        w.banking.request(w)
        for _ in range(5):
            w.step()
        assert w.banking.loan.status == 'delivered'
        w.pay('alltag', 'ausland', w.nodes['alltag']['cash_cents'], 'oracle_fixture', 'Explicit isolated funding port')
        outstanding = 120000
        principal_paid = 0
        interest_paid = 0
        interest_due = 0
        interest_charged = 0
        for (month, available) in enumerate(plan, 2):
            if w.nodes['alltag']['cash_cents']:
                w.pay('alltag', 'ausland', w.nodes['alltag']['cash_cents'], 'oracle_fixture', 'Explicit isolated funding port')
            if available:
                w.pay('ausland', 'alltag', available, 'oracle_fixture', 'Explicit isolated funding port')
            cash = available
            if outstanding or interest_due:
                charge = outstanding * 600 // 120000
                interest_due += charge
                interest_charged += charge
                paid = min(cash, interest_due)
                cash -= paid
                interest_due -= paid
                interest_paid += paid
                due = min(outstanding, max(0, min(12, month - 1) * 10000 - principal_paid))
                p = min(cash, due)
                cash -= p
                principal_paid += p
                outstanding -= p
            w.month = month
            w.phase = 0
            w.banking.service(w)
            loan = w.banking.loan
            assert (loan.outstanding_cents, loan.principal_paid_cents, loan.interest_paid_cents, loan.overdue_interest_cents, loan.interest_charged_cents) == (outstanding, principal_paid, interest_paid, interest_due, interest_charged)
            assert loan.overdue_principal_cents == max(0, min(12, month - 1) * 10000 - principal_paid)
            assert w.nodes['alltag']['cash_cents'] == cash
            w.check()
        results.append({'case': name, 'months_serviced': 24, 'independent_recurrence_passed': True, 'principal_paid_eur': principal_paid / 100, 'remaining_principal_eur': outstanding / 100, 'interest_paid_eur': interest_paid / 100, 'unpaid_interest_eur': interest_due / 100, 'bank_equity_eur': w.nodes['bank']['cash_cents'] / 100})
        print(name, 'servicing recurrence passed', flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write this repeat to a new JSON file; original QA evidence is preserved.')
    args = parser.parse_args()
    if not __debug__:
        parser.error('Assertions must be enabled; do not run Python with -O.')
    output = args.output.resolve() if args.output else None
    if output and output.exists():
        parser.error('The output file already exists. Select a new path for the repeat.')
    evidence = json.loads(EVIDENCE.read_text())['v3']
    source_files = evidence['source_files']
    for item in source_files:
        actual = hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            parser.error('Source differs from the recorded V3 audit: ' + item['path'])
    # BPTK can create a local log; keep generated runtime files out of source.
    runtime = ROOT / 'poc/.runtime/bank-plausibility'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    sys.path.insert(0, str(ROOT / 'poc'))
    global World
    from world import World
    specs = [
        ('v3_baseline', [], None),
        ('v3_energy', [(1, 'energy')], None),
        ('v3_demand', [(1, 'demand')], None),
        ('v3_both', [(1, 'energy'), (1, 'demand')], None),
        ('v3_credit_month1', [], 1),
        ('v3_credit_both_month1', [(1, 'energy'), (1, 'demand')], 1),
        ('v3_credit_month24', [], 24),
        ('v3_credit_month60', [], 60),
        ('v3_credit_month97', [], 97),
    ]
    results = []
    for name, events, credit_month in specs:
        result = run_world(name, events, credit_month, months=240)
        results.append(result)
        print(name, result['independent_posting_count'], 'postings reconstructed', flush=True)
    ports = run_servicing_ports()
    if results != evidence['results']:
        raise AssertionError('Repeated scenario results differ from the recorded V3 evidence.')
    if ports != evidence['independent_servicing_oracle']:
        raise AssertionError('Repeated payment-port results differ from the recorded V3 evidence.')
    postings = sum(r['independent_posting_count'] for r in results)
    report = {
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'evidence_reference': 'qa/bank-plausibility-review-2026-11-02.json',
        'source_files': source_files,
        'scope': 'Repeat of the recorded independent V3 audit; not a new empirical validation.',
        'recorded_results_match': True,
        'worlds': len(results), 'world_months': 2160,
        'independently_reconstructed_journal_entries': postings,
        'results': results, 'independent_servicing_oracle': ports,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: {len(results)} worlds, {postings} postings, {len(ports)} isolated payment paths; recorded results match.')


if __name__ == '__main__':
    main()
