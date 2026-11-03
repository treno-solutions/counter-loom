"""Controlled 600-month distribution-tax comparison against the V13 archive."""
import argparse,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

def run(months,rate,reference):
    w=World(goods_unit_scale=1,distribution_tax_bps=rate);rows=[];first={};start=time.monotonic()
    for month in range(1,months+1):
        for _ in range(5):w.step(emit_snapshot=False)
        h=w.history[-1];g=w.treasury.monthly(w);budget=w.budget.monthly(w)
        row=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,government_budget_balance_cents=g['budget_balance_cents'],public_wage_arrears_cents=g['public_wage_arrears_cents'],government_interest_arrears_cents=w.treasury.overdue_interest_cents,consumption_cents=h['consumption_cents'],production_units=sum(w.nodes[f]['metrics']['produced_units'] for f in ('alltag','werkstatt')),employment=h['employment'],public_budget=budget,distribution=w.distribution_tax.monthly(w),taxes_cents=g['taxes_cents'],taxes_by_kind={k:sum(t['amount_cents'] for t in w.journal if t['month']==month and t['kind']==k) for k in ('income_tax','arrears_income_tax','profit_tax','distribution_tax')},households=[dict(id=n['id'],employer=n['employer'],cash_cents=n['cash_cents'],income_cents=n['metrics']['income'],tax_cents=n['metrics']['tax'],transfers_cents=n['metrics']['transfers']) for n in w.households()])
        if rate==0:
            for key in ('household_cash_cents','firm_cash_cents','government_cash_cents','government_debt_cents','foreign_cash_cents','consumption_cents','employment','production_units','public_wage_arrears_cents'):
                assert row[key]==reference[month-1][key],(month,key,row[key],reference[month-1][key])
        assert g['taxes_cents']==sum(row['taxes_by_kind'].values())
        assert g['closing_cash_cents']==h['government_cash_cents']
        assert budget['recurring_taxes_cents']==g['taxes_cents']-row['taxes_by_kind']['arrears_income_tax']
        for key,condition in [('credit_limit_reached',w.treasury.outstanding_cents==w.treasury.credit_limit_cents),('public_job_reduction',budget['approved_staff']<2),('social_funding_gap',budget['social_unfunded_cents']>0)]:
            if condition and key not in first:first[key]=month
        rows.append(row)
        if month%120==0:print(rate,month,round(time.monotonic()-start,1),flush=True)
    return dict(distribution_tax_bps=rate,reference_monthly_match=rate==0,first_thresholds=first,monthly=rows,final_bank_balance=w.banking.balance(w))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--months',type=int,default=600);p.add_argument('--output',default='.framework-review/distribution-tax-comparison.json');args=p.parse_args()
    if not 1<=args.months<=600:p.error('Choose 1..600 months.')
    archive=Path('qa/fiscal-v13-comparison-2026-11-03.json');reference=json.loads(archive.read_text())['runs'][1]['monthly']
    files=('poc/world.py','poc/treasury.py','poc/public_budget.py','poc/distribution_tax.py','poc/profit_distribution.py','poc/scripts/compare_distribution_tax.py')
    data=dict(model='illustrative_circular_flow_v15',months=args.months,fiscal_policy='adaptive',distribution_policy='surplus',intervention='Only distribution withholding differs: 0 vs 2500 basis points. Identical initial conditions; no shocks. Illustrative assumption, no statutory tax claim.',reference=str(archive),reference_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},runs=[])
    for rate in (0,2500):
        data['runs'].append(run(args.months,rate,reference));target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
