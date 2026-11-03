"""Verify observation-only traces and the cost equivalence behind the critique."""
import unittest
from world import World
from firms import outlook
from scripts.diagnose_firm_reactions import TracedWorld

class FirmReactionDiagnosisTests(unittest.TestCase):
 def test_trace_does_not_change_the_economic_path(self):
  a,b=World(),TracedWorld(95)
  for _ in range(45*5):a.step(False);b.step(False)
  self.assertEqual(a.journal,b.journal)
  self.assertEqual(a.history,b.history)
  self.assertEqual(len(b.firm_traces),90)

 def test_one_full_worker_and_two_half_workers_have_equal_modeled_cost(self):
  w=World();firm=w.nodes['werkstatt']
  self.assertEqual(outlook(firm,1,1,10000),outlook(firm,1,2,5000))

 def test_traced_actual_staff_option_matches_the_executed_plan(self):
  w=TracedWorld(95)
  for _ in range(45*5):w.step(False)
  for f in w.firm_traces:
   self.assertEqual(f['plan']['staff'],f['staff_current'])
   if f['status_next']=='operating' and f['staff_next']:
    option=next(o for o in f['staff_options'] if o['staff']==f['staff_next'])
    self.assertEqual(option['allowed_work_bps'],f['work_bps_next'])
    self.assertEqual(option['reserve_cents'],f['result']['reserve_cents'])
  cut=next(f for f in w.firm_traces if f['staff_next']<f['staff_current'])
  self.assertEqual((cut['month'],cut['id']),(34,'werkstatt'))
  self.assertGreater(cut['profit_before_tax_cents'],0)
  self.assertLess(cut['fte_bps_next'],cut['fte_bps_current'])
