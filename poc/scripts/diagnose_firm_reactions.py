"""Read-only decision traces for the two archived consumption profiles."""
import argparse,hashlib,json,sys
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World
from firms import forecast,staffing,work_target,outlook,MIN_WORK_BPS,WORK_STEP_BPS

class TracedWorld(World):
 def __init__(self,quota):
  super().__init__();self.propensity=quota;self.firm_traces=[]
 def close_company(self,n):
  before=deepcopy(n);c=before['company'];m=before['metrics'];old_staff=len(before['employees'])
  # Reconstruct the same forecast on a detached copy, without changing the world.
  probe=deepcopy(before)
  if not self.crisis.closed(self,n['id']):forecast(probe['company'],m['sold_units']+m['unmet_units'])
  desired,_=staffing(probe,self.energy_multiplier,self.machine_due(n['id'],True))
  tax_due=max(0,m['sales']-m['cost_of_sales']-m['idle_cost']-m['unpaid_wages']-m['interest_expense']-m['closure_cost'])*20//100
  options=[]
  for staff in (1,2,3,4):
   target=work_target(probe,staff)
   work=max(MIN_WORK_BPS,min(c['work_bps']+WORK_STEP_BPS,max(c['work_bps']-WORK_STEP_BPS,target)))
   opt=outlook(probe,self.energy_multiplier,staff,work,self.machine_due(n['id'],True))
   options.append(dict(staff=staff,target_work_bps=target,allowed_work_bps=work,fte_bps=staff*work,**opt))
  super().close_company(n)
  after=n['company'];result=after['result']
  self.firm_traces.append(dict(month=self.month,id=n['id'],staff_current=old_staff,work_bps_current=c['work_bps'],fte_bps_current=old_staff*c['work_bps'],staff_signal_before=c['staff_signal'],staff_signal_after=after['staff_signal'],staff_desired=desired,staff_next=len(n['employees']),work_bps_next=after['next_work_bps'],fte_bps_next=len(n['employees'])*after['next_work_bps'],forecast_before_milli=c['forecast_milli'],forecast_after_milli=after['forecast_milli'],full_time_units_per_worker=n['productivity'],capital_units=n['capital']*4*self.goods_unit_scale,inventory_units=n['inventory'],inventory_value_cents=after['inventory_value_cents'],cash_before_close_cents=before['cash_cents'],cash_after_tax_cents=before['cash_cents']-min(tax_due,before['cash_cents']),cash_after_close_cents=n['cash_cents'],sales_cents=m['sales'],sold_units=m['sold_units'],unmet_units=m['unmet_units'],profit_before_tax_cents=result['profit_before_tax_cents'],status_current=c['status'],status_next=after['next_status'],reason=result['staff_reason'],plan=deepcopy(c['plan']),result=deepcopy(result),staff_options=options))

def trace(months,quota,reference):
 w=TracedWorld(quota);rows=[]
 for month in range(1,months+1):
  for _ in range(5):w.step(False)
  h=w.history[-1];g=w.treasury.monthly(w);b=w.budget.monthly(w);ref=reference[month-1]
  row=dict(month=month,consumption_cents=h['consumption_cents'],employment=h['employment'],public_budget=b,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,taxes_cents=g['taxes_cents'],households=deepcopy(h['households']),firms=deepcopy(w.firm_traces[-2:]))
  for k in ('consumption_cents','employment','public_budget','household_cash_cents','firm_cash_cents','government_cash_cents','foreign_cash_cents','government_debt_cents','taxes_cents'):assert row[k]==ref[k],(quota,month,k)
  rows.append(row)
  if month%120==0:print('trace',quota,month,flush=True)
 return dict(consumption_percent=quota,reference_exact_monthly_match=True,monthly=rows)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--months',type=int,default=600);p.add_argument('--output',default='.framework-review/firm-reaction-traces.json');a=p.parse_args()
 if not 1<=a.months<=600:p.error('Choose 1..600 months.')
 source=Path('qa/consumption-v16-comparison-2026-11-03.json');ref=json.loads(source.read_text())
 files=('poc/world.py','poc/firms.py','poc/public_budget.py','poc/systems.py','poc/scripts/diagnose_firm_reactions.py')
 data=dict(model='illustrative_circular_flow_v16',purpose='Read-only company decision diagnosis; no rule change or behavioral intervention',goods_unit_scale=100,months=a.months,reference=str(source),reference_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},runs=[])
 for quota,original in zip((95,100),ref['runs']):
  data['runs'].append(trace(a.months,quota,original['monthly']));out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
