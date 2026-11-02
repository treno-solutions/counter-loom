"""Historical purchase decisions must reconcile and retain their original inputs."""
import unittest
from copy import deepcopy
from world import World

class ConsumptionHistoryTests(unittest.TestCase):
    def finish(self,w):
        for _ in range(5):w.step()

    def test_month_close_reconciles_each_household_with_journal(self):
        w=World();self.finish(w);m=w.history[0]
        self.assertEqual(len(m['households']),6)
        self.assertEqual(sum(h['paid_cents'] for h in m['households']),m['consumption_cents'])
        for h in m['households']:
            journal=sum(t['amount_cents'] for t in w.journal if t['kind']=='consumption' and t['source']==h['id'])
            self.assertEqual(h['paid_cents'],journal)
            self.assertEqual(h['desired_cents'],h['paid_cents']+h['funding_gap_cents']+h['stock_gap_cents']+h['unit_remainder_cents'])
        self.finish(w);self.finish(w)
        self.assertGreater(sum(h['stock_gap_cents'] for h in w.history[-1]['households']),0)
        self.assertGreater(sum(h['unit_remainder_cents'] for h in m['households']),0)

    def test_missing_money_is_distinct_from_missing_stock(self):
        w=World();w.step();w.step()
        w.pay('h1','h2',w.nodes['h1']['cash_cents'],'transfer','Fixture transfer')
        w.step();w.step();w.step()
        h=w.history[0]['households'][0]
        self.assertEqual(h['funded_cents'],0)
        self.assertEqual(h['funding_gap_cents'],h['desired_cents'])
        self.assertEqual((h['paid_cents'],h['stock_gap_cents'],h['unit_remainder_cents']),(0,0,0))

    def test_decision_inputs_are_captured_before_closing_distributions(self):
        w=World();w.step();w.step();w.step()
        at_purchase=deepcopy(w.household_month)
        w.step();w.step()
        self.assertEqual(w.history[0]['households'],sorted(at_purchase,key=lambda h:h['id']))
        self.assertGreater(sum(h['dividend_carry'] for h in w.households()),0)
        self.assertEqual(sum(h['prior_dividend_cents'] for h in w.history[0]['households']),0)

    def test_history_keeps_old_policy_and_is_exported_without_aliasing(self):
        w=World();self.finish(w);first=deepcopy(w.history[0])
        w.queue('demand');w.monetary.queue(w,400);self.finish(w)
        self.assertEqual(w.history[0],first)
        self.assertEqual([m['consumption_percent'] for m in w.history],[95,65])
        exported=w.snapshot(export=True)
        self.assertEqual(exported['all_history'],w.history)
        exported['all_history'][0]['households'][0]['paid_cents']=0
        self.assertEqual(w.history[0],first)

    def test_24_month_shocks_preserve_gaps_and_payment_reconciliation(self):
        for scenario in ('baseline','demand','energy','rate'):
            w=World()
            for month in range(1,25):
                if month==3:
                    if scenario=='rate':w.monetary.queue(w,800)
                    elif scenario!='baseline':w.queue(scenario)
                self.finish(w)
                m=w.history[-1]
                for h in m['households']:
                    self.assertTrue(all(h[k]>=0 for k in ('funding_gap_cents','stock_gap_cents','unit_remainder_cents')))
                    self.assertEqual(h['desired_cents'],h['paid_cents']+h['funding_gap_cents']+h['stock_gap_cents']+h['unit_remainder_cents'])
                    self.assertEqual(h['paid_cents'],sum(t['amount_cents'] for t in w.journal if t['month']==month and t['source']==h['id'] and t['kind']=='consumption'))
