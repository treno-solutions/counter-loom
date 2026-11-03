"""Reproduce the fine default and account for the remaining state deficit."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

REVENUES=('income_tax','arrears_income_tax','profit_tax','distribution_tax')

def purchase_bridge(people,current_net_distribution,actual_saving):
 basis=sum(h['income_cents']-h['tax_cents']+h['prior_dividend_cents'] for h in people)
 wish=sum(h['desired_cents'] for h in people)
 result=dict(income_basis_cents=basis,desired_cents=wish,paid_cents=sum(h['paid_cents'] for h in people),
  planned_retention_cents=basis-wish,funding_gap_cents=sum(h['funding_gap_cents'] for h in people),
  stock_gap_cents=sum(h['stock_gap_cents'] for h in people),unit_remainder_cents=sum(h['unit_remainder_cents'] for h in people),
  distribution_timing_cents=current_net_distribution-sum(h['prior_dividend_cents'] for h in people),actual_saving_cents=actual_saving)
 assert actual_saving==sum(result[k] for k in ('planned_retention_cents','funding_gap_cents','stock_gap_cents','unit_remainder_cents','distribution_timing_cents'))
 return result

def diagnose(months=600,start=481):
 archive=Path('qa/goods-granularity-comparison-2026-11-03.json');reference=json.loads(archive.read_text())['runs'][1]['monthly']
 w=World();assert w.goods_unit_scale==100;rows=[]
 for month in range(1,months+1):
  for _ in range(5):w.step(emit_snapshot=False)
  h=w.history[-1];budget=w.budget.monthly(w);fiscal=w.treasury.monthly(w)
  old=reference[month-1]
  for key,value in dict(household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,consumption_cents=h['consumption_cents'],employment=h['employment'],public_budget=budget,taxes_cents=fiscal['taxes_cents']).items():
   assert value==old[key],(month,key)
  tx=[t for t in w.journal if t['month']==month]
  taxes={kind:sum(t['amount_cents'] for t in tx if t['kind']==kind and t['target']=='staat') for kind in REVENUES}
  assert sum(taxes.values())==fiscal['taxes_cents']
  delta={sector:sum(n['cash_cents']-w.month_open[n['id']] for n in w.nodes.values() if n['sector']==sector) for sector in ('households','firms','external','bank')}
  assert delta['bank']==0
  assert -fiscal['budget_balance_cents']==delta['households']+delta['firms']+delta['external']
  assert not any(t['kind']=='machine_credit' for t in tx)
  receipts=[r for r in w.distribution_tax.receipts if r['month']==month]
  people=h['households'];bridge=purchase_bridge(people,sum(r['net_cents'] for r in receipts),delta['households'])
  households=[]
  for person in people:
   node=w.nodes[person['id']];net=sum(r['net_cents'] for r in receipts if r['recipient']==node['id'])
   saving=node['cash_cents']-w.month_open[node['id']]
   households.append(dict(id=node['id'],employer_at_purchase=person['employer'],closing_cash_cents=node['cash_cents'],transfer_cents=person['transfers_cents'],net_distribution_cents=net,**purchase_bridge([person],net,saving)))
  row=dict(month=month,taxes_by_kind=taxes,total_taxes_cents=fiscal['taxes_cents'],public_payroll_cents=budget['payroll_cents'],procurement_budget_cents=budget['procurement_cents'],social_need_cents=budget['social_need_cents'],social_paid_cents=budget['social_paid_cents'],social_unfunded_cents=budget['social_unfunded_cents'],interest_due_cents=w.treasury.month_interest_charge_cents,interest_paid_cents=fiscal['interest_paid_cents'],committed_spending_cents=budget['committed_spending_cents'],need_deficit_cents=-budget['commitment_balance_cents'],cash_deficit_cents=-fiscal['budget_balance_cents'],primary_need_deficit_cents=budget['committed_spending_cents']-w.treasury.month_interest_charge_cents-fiscal['taxes_cents'],opening_state_cash_cents=w.month_open['staat'],closing_state_cash_cents=w.nodes['staat']['cash_cents'],closing_state_debt_cents=w.treasury.outstanding_cents,sector_cash_change_cents=delta,household_bridge=bridge,households=households,employment_end=h['employment'],public_staff=budget['approved_staff'],firms=[dict(id=f,staff_at_production=w.nodes[f]['company']['plan']['staff'],work_bps_at_production=w.nodes[f]['company']['plan']['work_bps'],staff_next_month=w.nodes[f]['company']['result']['next_staff'],work_bps_next_month=w.nodes[f]['company']['result']['next_work_bps']) for f in ('alltag','werkstatt')])
  rows.append(row)
  if month%120==0:print('default',month,flush=True)
 window=rows[start-1:months];assert window
 assert all(r['cash_deficit_cents']==r['need_deficit_cents'] and r['social_unfunded_cents']==0 for r in window)
 fields=('total_taxes_cents','public_payroll_cents','procurement_budget_cents','social_need_cents','social_paid_cents','interest_due_cents','interest_paid_cents','committed_spending_cents','need_deficit_cents','cash_deficit_cents','primary_need_deficit_cents')
 sums={k:sum(r[k] for r in window) for k in fields}
 sums['taxes_by_kind']={k:sum(r['taxes_by_kind'][k] for r in window) for k in REVENUES}
 sums['sector_cash_change_cents']={k:sum(r['sector_cash_change_cents'][k] for r in window) for k in window[0]['sector_cash_change_cents']}
 sums['household_bridge']={k:sum(r['household_bridge'][k] for r in window) for k in window[0]['household_bridge']}
 households=[dict(id=f'h{i}',opening_cash_cents=reference[start-2]['households'][i-1]['closing_cash_cents'] if start>1 else 300000,closing_cash_cents=w.nodes[f'h{i}']['cash_cents'],**{k:sum(next(h for h in r['households'] if h['id']==f'h{i}')[k] for r in window) for k in ('transfer_cents','actual_saving_cents','planned_retention_cents','stock_gap_cents','unit_remainder_cents','distribution_timing_cents')}) for i in range(1,7)]
 files=('poc/world.py','poc/systems.py','poc/public_budget.py','poc/distribution_tax.py','poc/treasury.py','poc/firms.py','poc/pricing.py','poc/foreign.py','poc/banking.py','poc/profit_distribution.py','poc/scripts/diagnose_fiscal_balance.py')
 return dict(model='illustrative_circular_flow_v15',scope='Unchanged-policy fine default; exact accounting diagnosis, no behavioral intervention',months=months,goods_unit_scale=100,reference=str(archive),reference_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),reference_profile='goods_unit_scale=100',reference_exact_monthly_match=True,source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},window=dict(start=start,end=months,count=len(window),totals=sums,households=households),monthly=rows)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--months',type=int,default=600);p.add_argument('--start',type=int,default=481);p.add_argument('--output',default='.framework-review/fiscal-balance-diagnosis.json');a=p.parse_args()
 if not 1<=a.start<=a.months<=600:p.error('Require 1 <= start <= months <= 600.')
 data=diagnose(a.months,a.start);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
