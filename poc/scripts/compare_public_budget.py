"""Controlled fiscal-policy comparison with identical V12 surplus distribution."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World


def run(months,policy,reference=None):
    w=World(distribution_tax_bps=0,distribution_policy='surplus',fiscal_policy=policy)
    rows=[];first={};beg=time.monotonic()
    for month in range(1,months+1):
        for _ in range(5):w.step(emit_snapshot=False)
        h=w.history[-1];g=w.treasury.monthly(w);budget=w.budget.monthly(w)
        tx=[t for t in w.journal if t['month']==month]
        row=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],
                 government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],
                 government_debt_cents=w.treasury.outstanding_cents,government_budget_balance_cents=g['budget_balance_cents'],
                 public_wage_arrears_cents=g['public_wage_arrears_cents'],government_interest_arrears_cents=w.treasury.overdue_interest_cents,
                 consumption_cents=h['consumption_cents'],production_units=sum(w.nodes[f]['metrics']['produced_units'] for f in ('alltag','werkstatt')),
                 employment=h['employment'],paid_jobs=sum(n['metrics']['income']>n['metrics']['transfers'] for n in w.households()),public_budget=budget,
                 households=[dict(id=n['id'],employer=n['employer'],cash_cents=n['cash_cents'],income_cents=n['metrics']['income'],tax_cents=n['metrics']['tax'],transfers_cents=n['metrics']['transfers']) for n in w.households()])
        if reference:
            for key in ('household_cash_cents','firm_cash_cents','government_cash_cents','government_debt_cents','foreign_cash_cents','consumption_cents','employment','production_units','public_wage_arrears_cents'):
                assert row[key]==reference[month-1][key],(month,key,row[key],reference[month-1][key])
        for key,condition in [('credit_limit_reached',w.treasury.outstanding_cents==w.treasury.credit_limit_cents),('state_cash_zero',w.nodes['staat']['cash_cents']==0),('public_job_reduction',budget['approved_staff']<2),('social_funding_gap',budget['social_unfunded_cents']>0)]:
            if condition and key not in first:first[key]=month
        rows.append(row)
        if month%120==0:print(policy,month,round(time.monotonic()-beg,1),flush=True)
    return dict(policy=policy,reference_monthly_match=reference is not None,first_thresholds=first,monthly=rows,
                cumulative_social_gap_cents=sum(r['public_budget']['social_unfunded_cents'] for r in rows),
                cumulative_procurement_paid_cents=sum(r['public_budget']['procurement_paid_cents'] for r in rows),
                public_job_months=sum(r['public_budget']['approved_staff'] for r in rows),
                final_bank_balance=w.banking.balance(w))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--months',type=int,default=600)
    parser.add_argument('--output',default='.framework-review/public-budget-comparison.json')
    args=parser.parse_args()
    if not 1<=args.months<=600:parser.error('Choose 1..600 months.')
    path=Path('qa/profit-v12-comparison-2026-11-03.json')
    reference=json.loads(path.read_text())['runs'][1]['monthly'] if path.exists() else None
    data=dict(model='illustrative_circular_flow_v14',months=args.months,distribution_policy='surplus',
              intervention='Only public budget policy differs; identical starting conditions, tax, credit limit, prices and private company rules. No shocks.',
              reference=str(path) if reference else None,source_sha256={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('poc/world.py','poc/treasury.py','poc/public_budget.py','poc/profit_distribution.py')},runs=[])
    for policy in ('legacy','adaptive'):
        data['runs'].append(run(args.months,policy,reference if policy=='legacy' else None))
        target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
