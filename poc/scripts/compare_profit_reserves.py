"""600-month controlled comparison. Run from the repository root with the POC environment."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World


def run(months, policy, reference=None):
    world=World(distribution_policy=policy)
    rows=[];thresholds={};beg=time.monotonic()
    for month in range(1,months+1):
        for _ in range(5):world.step(emit_snapshot=False)
        h=world.history[-1];g=world.treasury.monthly(world)
        tx=[t for t in world.journal if t['month']==month]
        dividend=sum(t['amount_cents'] for t in tx if t['kind'] in ('dividend','company_dividend','company_extra_dividend'))
        row=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],
                 government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],
                 government_debt_cents=world.treasury.outstanding_cents,government_budget_balance_cents=g['budget_balance_cents'],
                 public_wage_arrears_cents=g['public_wage_arrears_cents'],government_interest_arrears_cents=world.treasury.overdue_interest_cents,
                 consumption_cents=h['consumption_cents'],household_received_net_cents=sum(x['income_cents']-x['tax_cents'] for x in h['households'])+dividend,
                 production_units=sum(world.nodes[k]['metrics']['produced_units'] for k in ('alltag','werkstatt')),
                 households=[dict(id=n['id'],cash_cents=n['cash_cents'],employer=n['employer'],wage_and_transfer_cents=n['metrics']['income'],tax_cents=n['metrics']['tax'],owner_dividend_cents=sum(t['amount_cents'] for t in tx if t['target']==n['id'] and t['kind'] in ('company_dividend','company_extra_dividend'))) for n in world.households()],
                 employment=h['employment'],paid_jobs=sum(n['metrics']['income']>n['metrics']['transfers'] for n in world.households()),
                 regular_dividend_cents=sum(a['regular_paid_cents'] for a in h['profit_allocations']),
                 extra_dividend_cents=sum(a['extra_paid_cents'] for a in h['profit_allocations']),
                 retained_earnings_cents=sum(a['closing_retained_cents'] for a in h['profit_allocations']),
                 firms=[dict(id=f,cash_cents=world.nodes[f]['cash_cents'],**world.nodes[f]['company']['profit_allocation']) for f in ('alltag','werkstatt')])
        if reference:
            prior=reference[month-1]
            for key in ('household_cash_cents','firm_cash_cents','government_cash_cents','government_debt_cents','foreign_cash_cents','consumption_cents','employment','production_units'):
                assert row[key]==prior[key],(month,key,row[key],prior[key])
        for key,condition in [('state_cash_zero',row['government_cash_cents']==0),('credit_limit_reached',row['government_debt_cents']==world.treasury.credit_limit_cents),('household_cash_below_10_percent',row['household_cash_cents']<180000)]:
            if condition and key not in thresholds:thresholds[key]=month
        rows.append(row)
        if month%120==0:print(policy,month,round(time.monotonic()-beg,1),flush=True)
    return dict(policy=policy,first_thresholds=thresholds,monthly=rows,
                cumulative_regular_cents=sum(r['regular_dividend_cents'] for r in rows),
                cumulative_extra_cents=sum(r['extra_dividend_cents'] for r in rows),
                reference_monthly_match=bool(reference),
                initial_balances=world.initial,final_bank_balance=world.banking.balance(world))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--months',type=int,default=600)
    parser.add_argument('--output',default='.framework-review/profit-reserves-comparison.json')
    args=parser.parse_args()
    if not 1<=args.months<=600:parser.error('Choose 1..600 months.')
    reference_path=Path('qa/crisis-v11-long-horizon-2026-11-03.json')
    reference=json.loads(reference_path.read_text())['runs'][0]['monthly'] if reference_path.exists() else None
    result=dict(model='illustrative_circular_flow_v12',months=args.months,
                intervention='Only profit distribution policy; unchanged rules for state finance, tax, prices, employment and credit; identical initial conditions; no shocks.',
                reference='qa/crisis-v11-long-horizon-2026-11-03.json' if reference else None,
                source_sha256={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('poc/world.py','poc/firms.py','poc/profit_distribution.py','poc/treasury.py')},runs=[])
    for policy in ('legacy','surplus'):
        result['runs'].append(run(args.months,policy,reference if policy=='legacy' else None))
        target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
