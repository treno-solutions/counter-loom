"""Controlled goods-resolution experiment; no behavioral or fiscal policy change."""
import argparse,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

def run(months,scale,reference):
 w=World(goods_unit_scale=scale);rows=[];first={};start=time.monotonic()
 for month in range(1,months+1):
  for _ in range(5):w.step(emit_snapshot=False)
  h=w.history[-1];g=w.treasury.monthly(w);budget=w.budget.monthly(w);people=h['households']
  row=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,government_budget_balance_cents=g['budget_balance_cents'],public_wage_arrears_cents=g['public_wage_arrears_cents'],government_interest_arrears_cents=w.treasury.overdue_interest_cents,consumption_cents=h['consumption_cents'],production_subunits=sum(w.nodes[f]['metrics']['produced_units'] for f in ('alltag','werkstatt')),employment=h['employment'],public_budget=budget,taxes_cents=g['taxes_cents'],taxes_by_kind={k:sum(t['amount_cents'] for t in w.journal if t['month']==month and t['kind']==k) for k in ('income_tax','arrears_income_tax','profit_tax','distribution_tax')},purchase_totals={k:sum(p[k] for p in people) for k in ('desired_cents','funded_cents','paid_cents','funding_gap_cents','stock_gap_cents','unit_remainder_cents')},households=[dict(**p,closing_cash_cents=w.nodes[p['id']]['cash_cents']) for p in people],firms=[dict(id=f,price_cents=w.nodes[f]['price'],productivity_subunits=w.nodes[f]['productivity'],cash_cents=w.nodes[f]['cash_cents'],inventory_subunits=w.nodes[f]['inventory'],capital=w.nodes[f]['capital'],company=w.nodes[f]['company'].copy()) for f in ('alltag','werkstatt')])
  # Copy nested current-month dictionaries: future company updates must not rewrite history.
  row=json.loads(json.dumps(row))
  if scale==1:
   for key in ('household_cash_cents','firm_cash_cents','government_cash_cents','government_debt_cents','foreign_cash_cents','consumption_cents','employment','public_wage_arrears_cents','government_budget_balance_cents','taxes_cents','public_budget','taxes_by_kind'):
    assert row[key]==reference[month-1][key],(month,key)
   assert row['production_subunits']==reference[month-1]['production_units']
  assert g['closing_cash_cents']==h['government_cash_cents']
  assert row['taxes_cents']==sum(row['taxes_by_kind'].values())
  p=row['purchase_totals'];assert p['funded_cents']==p['paid_cents']+p['stock_gap_cents']+p['unit_remainder_cents']
  assert p['desired_cents']==p['funded_cents']+p['funding_gap_cents']
  for key,condition in [('credit_limit_reached',w.treasury.outstanding_cents==w.treasury.credit_limit_cents),('public_job_reduction',budget['approved_staff']<2),('social_funding_gap',budget['social_unfunded_cents']>0)]:
   if condition and key not in first:first[key]=month
  rows.append(row)
  if month%120==0:print(scale,month,round(time.monotonic()-start,1),flush=True)
 return dict(goods_unit_scale=scale,reference_monthly_match=scale==1,first_thresholds=first,monthly=rows,final_bank_balance=w.banking.balance(w))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--months',type=int,default=600);p.add_argument('--output',default='.framework-review/goods-granularity-comparison.json');args=p.parse_args()
 if not 1<=args.months<=600:p.error('Choose 1..600 months.')
 archive=Path('qa/tax-v14-comparison-2026-11-03.json');reference=json.loads(archive.read_text())['runs'][1]['monthly']
 files=('poc/world.py','poc/firms.py','poc/banking.py','poc/foreign.py','poc/pricing.py','poc/systems.py','poc/public_budget.py','poc/treasury.py','poc/distribution_tax.py','poc/profit_distribution.py','poc/scripts/compare_goods_granularity.py')
 data=dict(model='illustrative_circular_flow_v15',experiment='goods_granularity_100',months=args.months,initial_parameters=dict(fiscal_policy='adaptive',distribution_policy='surplus',distribution_tax_bps=2500,government_initial_cash_cents=8000000,government_credit_limit_cents=5000000,essential_budget_cents=100000),intervention='100 subunits replace one original goods unit. Prices and unit energy costs divided by 100; physical capacities, forecast quantities, export orders, machine inputs and machine productivity multiplied by 100. All money stocks, tax, wages, transfer, consumption and policy rules unchanged. All-goods resolution test including inventory and production rounding, not household-checkout-only. No shocks.',reference=str(archive),reference_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},runs=[])
 for scale in (1,100):
  data['runs'].append(run(args.months,scale,reference));target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
