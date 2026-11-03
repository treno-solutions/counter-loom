"""Identical 600-month worlds with 95 vs 100 percent household consumption."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

def run(months,quota,reference):
 w=World();w.propensity=quota;rows=[];first={}
 for month in range(1,months+1):
  for _ in range(5):w.step(emit_snapshot=False)
  assert w.propensity==quota
  h=w.history[-1];g=w.treasury.monthly(w);b=w.budget.monthly(w);tx=[t for t in w.journal if t['month']==month]
  row=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,consumption_cents=h['consumption_cents'],employment=h['employment'],public_budget=b,taxes_cents=g['taxes_cents'],cash_balance_cents=g['budget_balance_cents'],macro=w.macro.history[-1],purchase_totals={k:sum(p[k] for p in h['households']) for k in ('desired_cents','paid_cents','stock_gap_cents','unit_remainder_cents','funding_gap_cents')},planned_retention_cents=sum(p['income_cents']-p['tax_cents']+p['prior_dividend_cents']-p['desired_cents'] for p in h['households']),household_saving_cents=sum(n['cash_cents']-w.month_open[n['id']] for n in w.households()))
  if quota==95:
   for key in ('household_cash_cents','firm_cash_cents','government_cash_cents','foreign_cash_cents','government_debt_cents','consumption_cents','employment','public_budget','taxes_cents'):assert row[key]==reference[month-1][key],(month,key)
  for key,condition in [('credit_limit_reached',w.treasury.outstanding_cents==w.treasury.credit_limit_cents),('public_job_reduction',b['approved_staff']<2),('social_funding_gap',b['social_unfunded_cents']>0)]:
   if condition and key not in first:first[key]=month
  rows.append(row)
  if month%120==0:print(quota,month,flush=True)
 return dict(consumption_percent=quota,reference_monthly_match=quota==95,first_thresholds=first,monthly=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--months',type=int,default=600);p.add_argument('--output',default='.framework-review/consumption-comparison.json');a=p.parse_args()
 if not 1<=a.months<=600:p.error('Choose 1..600 months.')
 archive=Path('qa/goods-granularity-comparison-2026-11-03.json');ref=json.loads(archive.read_text())['runs'][1]['monthly']
 files=('poc/world.py','poc/macro.py','poc/systems.py','poc/firms.py','poc/public_budget.py','poc/treasury.py','poc/distribution_tax.py','poc/pricing.py','poc/banking.py','poc/foreign.py','poc/profit_distribution.py','poc/scripts/compare_consumption.py')
 data=dict(model='illustrative_circular_flow_v16',months=a.months,intervention='Only consumption_percent differs: 95 vs 100. Fine units, 25 percent distribution tax, adaptive public budget, identical initial accounts, wages, interest, transfers and company rules. No shocks. Macro accounts are read-only.',reference=str(archive),reference_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},runs=[])
 for quota in (95,100):
  data['runs'].append(run(a.months,quota,ref));target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
