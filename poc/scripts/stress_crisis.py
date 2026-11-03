"""Reproducible long-horizon stress runs. Execute from the repository root."""
import sys,json,time
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--months',type=int,default=600)
parser.add_argument('--output',default='.framework-review/crisis-long-horizon.json')
args=parser.parse_args()
if args.months<36:parser.error('At least 36 months are needed for the closure and reopening comparison.')
out={'model':'illustrative_circular_flow_v11','purpose':'Long-horizon rule stress test; not a forecast or calibration','horizon_months':args.months,'runs':[]}
for name,rate in [('baseline',None),('closure_without_support',0),('closure_with_support',6000)]:
 w=World();rows=[];checkpoints=[];first={};beg=time.time()
 for month in range(1,args.months+1):
  if month==25 and rate is not None:w.crisis.queue(w,'werkstatt',3,rate)
  for _ in range(5):w.step()
  h=w.history[-1];f=w.treasury.monthly(w)
  row={'month':month,'household_cash_cents':h['household_cash_cents'],'firm_cash_cents':h['cash_by_sector']['firms'],'government_cash_cents':h['government_cash_cents'],'government_debt_cents':w.treasury.outstanding_cents,'foreign_cash_cents':w.nodes['ausland']['cash_cents'],'consumption_cents':h['consumption_cents'],'household_net_cents':sum(x['income_cents']-x['tax_cents'] for x in h['households']),'production_units':sum(w.nodes[k]['metrics']['produced_units'] for k in ('alltag','werkstatt')),'employment':h['employment'],'short_time_cents':w.crisis.snapshot(w)['monthly_paid_cents']}
  rows.append(row)
  for key,condition in [('state_cash_zero',row['government_cash_cents']==0),('credit_limit_reached',w.treasury.outstanding_cents==w.treasury.credit_limit_cents),('household_cash_below_10_percent',row['household_cash_cents']<180000),('production_zero',row['production_units']==0)]:
   if condition and key not in first:first[key]=month
  if month in (12,24,28,36,60,120,240,342,360,600):
   checkpoints.append(dict(**row,firms=[dict(id=k,cash_cents=w.nodes[k]['cash_cents'],status=w.nodes[k]['company']['status'],work_bps=w.nodes[k]['company']['plan']['work_bps'],staff=len(w.nodes[k]['employees']),profit_cents=w.nodes[k]['company']['result']['profit_before_tax_cents'],payout_cents=w.nodes[k]['company']['result']['distribution_cents'],reserve_cents=w.nodes[k]['company']['result']['reserve_cents']) for k in ('alltag','werkstatt')]))
  assert all(n['cash_cents']>=0 for n in w.nodes.values())
  if month%120==0:print(name,month,round(time.time()-beg,1),flush=True)
 flows=defaultdict(int)
 for t in w.journal:
  for sector in ('households','firms','government'):
   if w.nodes[t['target']]['sector']==sector:flows[sector+':in:'+t['kind']]+=t['amount_cents']
   if w.nodes[t['source']]['sector']==sector:flows[sector+':out:'+t['kind']]+=t['amount_cents']
 out['runs'].append(dict(name=name,closure=None if rate is None else dict(firm='werkstatt',start_month=25,duration=3,replacement_bps=rate),first_thresholds=first,checkpoints=checkpoints,monthly=rows,cumulative_flows_cents=dict(sorted(flows.items())),open_obligations_cents=sum(o['amount_cents'] for o in w.obligations),negative_household_accounts=False))
 Path(args.output).parent.mkdir(parents=True,exist_ok=True)
 Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(name,'complete',flush=True)
