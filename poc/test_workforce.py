import unittest
from world import World
from workforce import choose,options

class WorkforceTests(unittest.TestCase):
 def firm(self):
  w=World();n=w.nodes['werkstatt'];c=n['company'];c['profitable_months']=2
  return w,n,c
 def test_two_part_time_workers_are_retained_below_one_full_time_threshold(self):
  w,n,c=self.firm();n['inventory']=444;c.update(forecast_milli=1995635,work_bps=4633,next_work_bps=4633,staff_signal=-1)
  p=choose(n,1,available_worker=True)
  self.assertEqual(p['desired_staff'],2);self.assertEqual(p['selected']['staff'],2)
  self.assertEqual(p['selected']['work_bps'],5128);self.assertEqual(p['signal'],0)
  self.assertEqual(p['required_units'],2051)
 def test_hire_redistributes_total_work_without_the_old_fte_jump(self):
  w,n,c=self.firm();c.update(forecast_milli=4000000,work_bps=10000,next_work_bps=10000,staff_signal=1)
  p=choose(n,1,available_worker=True);o=p['selected']
  self.assertEqual(o['staff'],3)
  self.assertLessEqual(o['fte_bps']-20000,2*2500+o['staff']-1)
  self.assertTrue(o['reserve_ok']);self.assertTrue(o['transition_ok'])
 def test_unavailable_or_unfunded_worker_cannot_be_hired(self):
  w,n,c=self.firm();c.update(forecast_milli=4000000,staff_signal=1)
  self.assertEqual(choose(n,1,available_worker=False)['selected']['staff'],2)
  n['cash_cents']=0
  self.assertEqual(choose(n,1,available_worker=True)['selected']['staff'],2)
 def test_cut_requires_confirmed_need_below_minimum_hours(self):
  w,n,c=self.firm();c.update(forecast_milli=400000,work_bps=2500,next_work_bps=2500,staff_signal=0)
  first=choose(n,1,available_worker=True);self.assertEqual(first['selected']['staff'],2)
  c['staff_signal']=first['signal'];second=choose(n,1,available_worker=True)
  self.assertEqual(second['selected']['staff'],1);self.assertEqual(second['selected']['work_bps'],2500)
 def test_impossible_aggregate_transition_defers_headcount_reduction(self):
  w,n,c=self.firm();n['employees'].append('h5');c.update(forecast_milli=0,work_bps=10000,next_work_bps=10000,staff_signal=-1)
  p=choose(n,1,available_worker=True);self.assertEqual(p['desired_staff'],2);self.assertEqual(p['selected']['staff'],3)
  self.assertFalse(next(o for o in p['options'] if o['staff']==2)['transition_ok'])
 def test_joint_world_conserves_accounts_under_rate_energy_and_closure(self):
  w=World(workforce_policy='joint');w.banking.request(w)
  accounts=dict(w.initial);last=0
  for step in range(120):
   if step==20:w.queue('energy');w.monetary.queue(w,500)
   if step==40:w.crisis.queue(w,'both',2,6000)
   w.step(False)
   for t in w.journal[last:]:
    self.assertEqual(accounts[t['source']],t['source_before']);self.assertEqual(accounts[t['target']],t['target_before'])
    if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
    if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
    self.assertEqual(accounts[t['source']],t['source_after']);self.assertEqual(accounts[t['target']],t['target_after'])
   self.assertEqual(accounts,{k:n['cash_cents'] for k,n in w.nodes.items()});last=len(w.journal)
  for d in w.workforce_history:
   self.assertEqual(d['selected_fte_bps'],d['selected_staff']*d['selected_work_bps'])
   if d['current_staff'] and d['selected_staff'] and not d['closed'] and d['next_status'] in ('operating','buffered'):
    self.assertLessEqual(abs(d['selected_fte_bps']-d['current_fte_bps']),d['current_staff']*2500+d['selected_staff']-1)
