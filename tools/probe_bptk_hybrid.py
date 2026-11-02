#!/usr/bin/env python3
"""Offline arithmetic/SD/event fixture, not a validated economic or investor model.
Install bptk-py==3.5.0. Run from repo root; no model API or network calls.
"""
import hashlib,json,time,platform
from importlib.metadata import version
from pathlib import Path
from BPTK_Py import Model,Agent,Event,SimultaneousScheduler
from BPTK_Py import sd_functions as sd
ROOT=Path(__file__).resolve().parents[1]
VERSION='3.5.0'
SOURCE='840fb9b61504c5a6e463e72a73c07e0b8cff6d5e'
assert version('bptk-py')==VERSION
CASES=[{'id':'variable_loan','label':'Variabler Kredit','loan':60000,'deposit':0,'variable':True},
       {'id':'fixed_loan','label':'Festzinskredit','loan':60000,'deposit':0,'variable':False},
       {'id':'deposit','label':'Verzinste Einlage','loan':0,'deposit':60000,'variable':True}]
class Household(Agent):
 def initialize(self):
  self.state='routine';self.register_event_handler(['routine','review_due'],'contract_repriced',self.review)
 def review(self,event):self.state='review_due'
 def act(self,time,round_no,step_no):
  case=CASES[self.id];prefix=case['id']
  get=lambda name,t=time:self.model.evaluate_equation(prefix+'_'+name,t)
  record={'period':int(time)+1,'case':prefix,'label':case['label'],'state':self.state,
    'annual_rate':self.model.evaluate_equation('policy_rate',time),'contract_rate':get('contract_rate'),
    'income':get('income'),'interest_cost':get('interest_cost'),'interest_income':get('interest_income'),
    'essential_expenses':2100,'planned_allocation':get('contribution'),'cash_open':get('cash'),
    'cash_close':get('cash',time+1),'earmarked_close':get('earmarked',time+1),'arrears_close':get('arrears',time+1)}
  self.model.trace.append(record)

def simulate(after_rate):
 m=Model(starttime=0,stoptime=6,dt=1,name='Offline parameter/event fixture',scheduler=SimultaneousScheduler());m.trace=[]
 rate=m.converter('policy_rate');rate.equation=.02+sd.step(after_rate-.02,2)
 m.register_agent_factory('household',lambda aid,model,properties:Household(aid,model,properties))
 for c in CASES:
  key=c['id'];make=lambda name,kind='converter':getattr(m,kind)(key+'_'+name)
  contract=make('contract_rate');contract.equation=rate if c['variable'] else .02
  inc=make('income');inc.equation=2400.0
  icost=make('interest_cost');icost.equation=c['loan']*contract/12
  iinc=make('interest_income');iinc.equation=c['deposit']*contract/12
  required=make('required');required.equation=2100+icost
  cash=make('cash','stock');cash.initial_value=1000
  earmarked=make('earmarked','stock');earmarked.initial_value=0
  arrears=make('arrears','stock');arrears.initial_value=0
  payment=make('payment','flow');payment.equation=sd.min(required,sd.max(0,cash+inc+iinc))
  contribution=make('contribution','flow');contribution.equation=sd.min(100,sd.max(0,inc+iinc-required))
  net=make('net','biflow');net.equation=inc+iinc-payment-contribution
  cash.equation=net;earmarked.equation=contribution;arrears.equation=sd.max(0,required-payment)
  m.create_agent('household',{})
 for period in range(6):
  if period==2 and after_rate!=.02:
   for a,c in zip(m.agents,CASES):
    if c['variable']:m.events.append(Event('contract_repriced',a.id,a.id,{'rate':after_rate}))
  m.scheduler.run_step(m,period,0,collect_data=False)
 return m.trace

def main():
 started=time.perf_counter();results={name:simulate(rate) for name,rate in [('unchanged',.02),('higher',.06),('lower',0.0)]}
 assert results['higher']==simulate(.06),'Independent construction/replay must match'
 for rows in results.values():
  for row in rows:
   assert row['cash_close']>=-1e-9 and row['planned_allocation']>=0
   previous=next((r for r in rows if r['case']==row['case'] and r['period']==row['period']-1),None)
   if previous:assert abs(previous['cash_close']-row['cash_open'])<1e-8
 # At month 3 contracts reprice. The state is a technical review marker, not panic.
 select=lambda scenario,case,p:next(r for r in results[scenario] if r['case']==case and r['period']==p)
 assert select('higher','variable_loan',3)['planned_allocation']==0
 assert select('unchanged','variable_loan',3)['planned_allocation']==100
 assert select('higher','fixed_loan',6)['cash_close']==select('unchanged','fixed_loan',6)['cash_close']
 assert select('higher','deposit',6)['cash_close']>select('unchanged','deposit',6)['cash_close']
 assert select('higher','fixed_loan',3)['state']=='routine'
 assert select('higher','variable_loan',3)['state']=='review_due'
 assert select('higher','deposit',3)['state']=='review_due'
 extreme=simulate(.50)
 assert min(r['cash_close'] for r in extreme)>=-1e-9
 assert max(r['arrears_close'] for r in extreme)>0
 report={'checked_on':'2026-11-02','classification':'offline_technical_fixture_not_empirical_economic_result','framework':'BPTK-Py','installed_version':VERSION,'reviewed_source_commit':SOURCE,'backend':'Python SD equations and native agent/event scheduler','python':platform.python_version(),'llm_calls':0,'network_calls_in_probe':0,'passed':True,'record_count':sum(map(len,results.values())),'checks':['SD parameter changes','native contract_repriced event and state transition','fixed contract unaffected','opposite interest cash-flow exposure','cash continuity','nonnegative cash and unpaid obligations in stress fixture','independently rebuilt run matches'],'elapsed_seconds':round(time.perf_counter()-started,3),'cases':CASES,'assumptions':['All cases are invented arithmetic fixtures, not empirical types or a proposed first workshop scenario.','Six monthly periods; rate changes at the start of month 3; simple annual interest divided by 12; no amortization.','Monthly income 2400; essential expenses 2100; opening spendable cash 1000; target allocation 100.','A separate 60000 principal asset or liability is fixed; repayment, bank balance sheets and counterpart accounts are outside this fixture.','Allocation is an internal earmarking of money, not an executed securities purchase.','Native agent state review_due only marks a contract event. Investment allocation is a predefined arithmetic rule, not a persona decision.','No rent pass-through, endogenous rate policy, inflation, macroeconomic feedback, uncertainty, workshop interface or LLM behavior validated.','Persistent checkpoints across processes and full SD/agent restoration remain untested.'],'results':results,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out=ROOT/'qa/bptk-technical-screen-2026-11-02.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['framework','installed_version','passed','record_count','llm_calls','elapsed_seconds']}))
if __name__=='__main__':main()
