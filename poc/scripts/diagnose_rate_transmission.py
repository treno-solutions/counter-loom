"""Read-only decomposition of the archived v18 rate shock; no rule changes."""
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path

SOURCE = Path('qa/isolated-shocks-v18-2026-11-03.json')
OUTPUT = Path('qa/rate-transmission-v18-diagnosis.json')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def window(run, months):
    rows = run['monthly'][:months]
    end = rows[-1]['month']
    tx = [t for t in run['transactions'] if t['month'] <= end]
    flows = defaultdict(int)
    bank_net = bank_tax = 0
    monthly = defaultdict(lambda: defaultdict(int))
    for i, t in enumerate(tx):
        flows[t['kind']] += t['amount_cents']
        monthly[t['month']][t['kind']] += t['amount_cents']
        if t['kind'] == 'dividend':
            tax = tx[i+1] if i+1 < len(tx) else None
            assert tax and tax['kind'] == 'distribution_tax' and tax['source'] == t['target']
            bank_net += t['amount_cents']-tax['amount_cents']
            bank_tax += tax['amount_cents']
    for month, f in monthly.items():
        assert f['dividend'] == f['interest']+f['machine_interest']+f['government_interest'], month
    owner = sum(h['owner_payout_net_cents'] for r in rows for h in r['households'])
    income = sum(r['disposable_received_cents'] for r in rows)
    other = sum(h['income_before_owner_payout_cents'] for r in rows for h in r['households'])
    assert other+owner == income
    return dict(flows_cents=dict(flows), bank_net_cents=bank_net, bank_withholding_cents=bank_tax,
        firm_net_cents=owner-bank_net, non_owner_net_cents=other, household_income_cents=income,
        purchases_cents=sum(r['consumption_cents'] for r in rows),
        firm_sales_cents=sum(f['sales_cents'] for r in rows for f in r['firms']),
        firm_profit_cents=sum(f['profit_before_tax_cents'] for r in rows for f in r['firms']),
        government_net_cents=rows[-1]['stocks_cents']['government_net'])


def run():
    data = json.loads(SOURCE.read_text())
    for path, expected in data['source_sha256'].items():
        assert digest(path) == expected, path
    cases = {r['case']: r for r in data['runs']}
    result = dict(date='2026-11-03', model=data['model'], model_rules_changed=False,
        method='Archived transaction decomposition and source inspection; no new counterfactual simulation',
        source=str(SOURCE), source_sha256=digest(SOURCE),
        source_code_sha256=data['source_sha256'], diagnostic_script_sha256=digest(__file__),
        windows={}, checks=dict(source_hashes_match=True, bank_pays_all_monthly_received_interest=True,
            household_income_decomposition_exact=True))
    for months in (12, 13, 60):
        control, shock = (window(cases[k], months) for k in ('control', 'rate'))
        delta = {k: shock[k]-control[k] for k in control if k != 'flows_cents'}
        delta['flows_cents'] = {k: shock['flows_cents'].get(k, 0)-control['flows_cents'].get(k, 0)
            for k in sorted(set(control['flows_cents']) | set(shock['flows_cents']))}
        assert delta['household_income_cents'] == sum(delta[k] for k in ('bank_net_cents','firm_net_cents','non_owner_net_cents'))
        result['windows'][str(months)] = dict(control=control, shock=shock, delta=delta,
            extra_interest_as_percent_control_firm_sales=100*delta['flows_cents']['interest']/control['firm_sales_cents'],
            purchases_delta_percent=100*delta['purchases_cents']/control['purchases_cents'])
    exposure = dict(variable_principal_cents=1200000, fixed_principal_cents=1200000,
        additional_monthly_interest_cents=1200000*300//120000,
        higher_variable_rate_relative_months=[r['relative_month'] for r in cases['rate']['monthly'] if r['variable_rate_bps']==500],
        first_policy_change_relative_month=1, first_variable_change_relative_month=2,
        principal_new_credit_cents={k:sum(t['amount_cents'] for t in cases[k]['transactions'] if t['ledger_effect']=='loan_creation') for k in ('control','rate')},
        investment_payments_cents={k:sum(t['amount_cents'] for t in cases[k]['transactions'] if t['kind'] in ('investment','machine_purchase')) for k in ('control','rate')},
        bank_equity_cents=sorted({r['stocks_cents']['bank'] for k in ('control','rate') for r in cases[k]['monthly']}),
        government_debt_cents=sorted({r['stocks_cents']['government_debt'] for k in ('control','rate') for r in cases[k]['monthly']}))
    assert exposure['higher_variable_rate_relative_months']==list(range(2,14))
    assert result['windows']['13']['delta']['flows_cents']['interest']==36000
    assert all(v==0 for v in exposure['principal_new_credit_cents'].values())
    assert all(v==0 for v in exposure['investment_payments_cents'].values())
    result['exposure'] = exposure
    # Conditional accounting illustration, not a new simulation or effect estimate:
    # freeze activity, assume positive taxable profit and eventual full firm payout.
    interest = Fraction(3000)
    bank = interest*Fraction(3,4)
    firm = -interest*Fraction(4,5)*Fraction(3,4)
    state = -interest*Fraction(1,5)+(interest-interest*Fraction(4,5))*Fraction(1,4)
    assert bank+firm+state == 0
    result['conditional_accounting_example_cents'] = dict(extra_interest=int(interest),
        bank_owner_net=int(bank), firm_owner_net=int(firm), household_net=int(bank+firm),
        state_net=int(state), assumes='Frozen activity, positive firm profit, eventual full distribution, no rounding; not observed causal attribution')
    OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(exposure=exposure,window12_delta=result['windows']['12']['delta'],
        conditional_example=result['conditional_accounting_example_cents']),indent=2))


if __name__ == '__main__':
    run()
