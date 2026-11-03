import unittest
from world import World
from macro import change_bps

class MacroTests(unittest.TestCase):
    def test_observation_does_not_change_economic_decisions(self):
        a,b=World(),World();b.macro.close=lambda world:None
        for _ in range(60):a.step(False);b.step(False)
        self.assertEqual(a.journal,b.journal)
        self.assertEqual(a.history,b.history)
        self.assertEqual({k:n['cash_cents'] for k,n in a.nodes.items()},{k:n['cash_cents'] for k,n in b.nodes.items()})

    def test_gdp_components_reconcile_and_financing_is_separate(self):
        w=World()
        for _ in range(5):w.step(False)
        r=w.macro.history[-1];c=r['components']
        self.assertEqual(r['gdp_proxy_cents'],c['consumption_cents']+c['public_goods_cents']+c['investment_cents']+c['exports_cents']-c['imports_cents']+c['inventory_change_cents']+c['public_services_cents'])
        self.assertEqual(c['public_services_cents'],480000)
        self.assertEqual(c['consumption_cents'],956400)
        self.assertEqual(c['inventory_change_cents'],sum(w.nodes[k]['company']['inventory_value_cents'] for k in ('alltag','werkstatt')))
        self.assertEqual(r['goods_output_index_bps'],10000)
        self.assertEqual(r['private_fte_bps'],40000)
        self.assertEqual(r['employment_at_production'],6)

    def test_growth_needs_a_positive_matching_base(self):
        self.assertIsNone(change_bps(1,0));self.assertIsNone(change_bps(1,-1))
        self.assertEqual(change_bps(110,100),1000)
        w=World()
        for _ in range(13*5):w.step(False)
        self.assertTrue(all(r['nominal_growth_yoy_bps'] is None for r in w.macro.history[:12]))
        self.assertEqual(w.macro.history[12]['nominal_growth_yoy_bps'],change_bps(w.macro.history[12]['gdp_proxy_cents'],w.macro.history[0]['gdp_proxy_cents']))

    def test_closed_firms_have_no_private_fte_or_productivity(self):
        w=World();w.crisis.queue(w,'both',2,6000)
        for _ in range(5):w.step(False)
        r=w.macro.history[-1]
        self.assertEqual(r['private_fte_bps'],0)
        self.assertEqual(r['goods_output_base_cents'],0)
        self.assertIsNone(r['goods_productivity_cents'])
        self.assertEqual(r['components']['public_services_cents'],480000)

    def test_history_rolls_but_export_preserves_all_months(self):
        w=World()
        for _ in range(125*5):w.step(False)
        self.assertEqual(len(w.snapshot()['macro']['history']),120)
        self.assertEqual(len(w.snapshot(export=True)['all_macro_history']),125)

    def test_no_birth_rate_is_invented(self):
        m=World().snapshot()['macro']
        self.assertFalse(m['demography_modeled']);self.assertIsNone(m['birth_rate_per_1000'])
        self.assertIsNone(m['monthly'])
