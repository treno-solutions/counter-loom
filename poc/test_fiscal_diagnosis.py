"""Checks of the explanatory cash bridge, including drawdown and distribution timing."""
import unittest
from scripts.diagnose_fiscal_balance import purchase_bridge
from world import World

class FiscalDiagnosisTests(unittest.TestCase):
    def test_planned_retention_goods_gaps_and_current_distribution_reconcile(self):
        h=dict(income_cents=10000,tax_cents=1000,prior_dividend_cents=100,desired_cents=8000,paid_cents=7700,funding_gap_cents=0,stock_gap_cents=200,unit_remainder_cents=100)
        b=purchase_bridge([h],150,1450)
        self.assertEqual(b['planned_retention_cents'],1100)
        self.assertEqual(b['distribution_timing_cents'],50)
        self.assertEqual(b['actual_saving_cents'],1450)
        with self.assertRaises(AssertionError):purchase_bridge([h],150,1451)

    def test_minimum_consumption_can_draw_down_existing_savings(self):
        h=dict(income_cents=0,tax_cents=0,prior_dividend_cents=0,desired_cents=10000,paid_cents=10000,funding_gap_cents=0,stock_gap_cents=0,unit_remainder_cents=0)
        self.assertEqual(purchase_bridge([h],0,-10000)['planned_retention_cents'],-10000)

    def test_current_default_energy_and_closure_preserve_cash_and_goods_accounting(self):
        w=World();self.assertEqual(w.goods_unit_scale,100)
        for _ in range(10):w.step(False)
        w.queue('energy');w.monetary.queue(w,500)
        for _ in range(10):w.step(False)
        w.crisis.queue(w,'both',2,6000)
        for _ in range(80):
            w.step(False)
            self.assertTrue(all(n['cash_cents']>=0 for n in w.nodes.values()))
        self.assertGreater(w.nodes['alltag']['price'],100)
        self.assertGreater(w.nodes['werkstatt']['price'],150)
        self.assertGreater(w.crisis.snapshot(w)['episodes'][0]['replacement_bps'],0)
