"""Dimensional and accounting checks for the controlled goods-resolution experiment."""
import unittest
from world import World
from firms import plan,full_capacity,staffing

class GoodsGranularityTests(unittest.TestCase):
    def test_new_world_defaults_to_fine_units(self):
        w=World()
        self.assertEqual(w.goods_unit_scale,100)
        self.assertEqual(w.nodes['alltag']['price'],100)
        self.assertEqual(w.nodes['werkstatt']['price'],150)
        self.assertEqual(w.banking.loan.units,800)
        self.assertEqual(w.snapshot()['classification'],'illustrative_circular_flow_v20')
        self.assertIn('800 Werkstatteinheiten',w.snapshot()['rules']['bank'])
        self.assertIn('600 Alltags- und 200 Werkstatteinheiten',w.snapshot()['rules']['external'])

    def test_supported_scales_and_unchanged_money_stocks(self):
        for bad in (0,2,-1,True,100.0,'100'):
            with self.assertRaises(ValueError):World(goods_unit_scale=bad)
        original=World(goods_unit_scale=1)
        for scale in (10,100):
            w=World(goods_unit_scale=scale)
            self.assertEqual(w.initial,original.initial)
            self.assertEqual(w.banking.balance(w),original.banking.balance(original))
            self.assertEqual(w.distribution_tax.rate_bps,2500)
            for f in ('alltag','werkstatt'):
                self.assertEqual(w.nodes[f]['price']*scale,original.nodes[f]['price'])
                self.assertEqual(w.nodes[f]['productivity'],original.nodes[f]['productivity']*scale)
                self.assertEqual(w.foreign.orders[f],original.foreign.orders[f]*scale)
            self.assertEqual(w.pricing.market(w)['basket_cost_cents'],original.pricing.market(original)['basket_cost_cents'])
            self.assertEqual(w.pricing.market(w)['price_index_bps'],10000)

    def test_initial_physical_capacity_energy_and_cash_plans_are_equivalent(self):
        a,b=World(goods_unit_scale=1),World(goods_unit_scale=100)
        for f in ('alltag','werkstatt'):
            na,nb=a.nodes[f],b.nodes[f]
            pa,pb=plan(na,1),plan(nb,1)
            for key in ('capacity_units','production_units','funded_units','demand_units','target_units'):
                self.assertEqual(pb[key],100*pa[key],key)
            self.assertEqual(pb['production_units']*pb['energy_unit_cents'],pa['production_units']*pa['energy_unit_cents'])
            self.assertEqual(staffing(na,1),staffing(nb,1))
            na['capital']=nb['capital']=1
            self.assertEqual(full_capacity(nb,2),100*full_capacity(na,2))
        for _ in range(2):a.step(False);b.step(False)
        self.assertEqual({k:n['cash_cents'] for k,n in a.nodes.items()},{k:n['cash_cents'] for k,n in b.nodes.items()})

    def test_first_purchase_reduces_unit_remainder_without_altering_budget(self):
        a,b=World(goods_unit_scale=1),World(goods_unit_scale=100)
        for _ in range(3):a.step(False);b.step(False)
        for ha,hb in zip(a.household_month,b.household_month):
            self.assertEqual(ha['desired_cents'],hb['desired_cents'])
            self.assertEqual(ha['funded_cents'],hb['funded_cents'])
            self.assertEqual(ha['unit_remainder_cents'],19600)
            self.assertEqual(hb['unit_remainder_cents'],200)
            self.assertEqual(hb['stock_gap_cents'],0)
            self.assertEqual(hb['funded_cents'],hb['paid_cents']+hb['unit_remainder_cents'])
            self.assertEqual(hb['paid_real_cents'],hb['paid_cents'])

    def test_machine_price_quantity_and_capacity_are_converted_together(self):
        # Controlled zero-consumption port keeps supplier stock available in both resolutions.
        w=World(goods_unit_scale=100,essential_budget_cents=0);w.propensity=0;w.banking.request(w)
        for _ in range(4):w.step(False)
        self.assertEqual(w.banking.loan.status,'credited')
        self.assertEqual(w.banking.loan.amount_cents,120000)
        self.assertEqual(w.banking.loan.units,800)
        stock=w.nodes['werkstatt']['inventory'];w.step(False)
        self.assertEqual(w.nodes['werkstatt']['inventory'],stock-800)
        self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(w.nodes['werkstatt']['reserved_units'],0)
        self.assertEqual(full_capacity(w.nodes['alltag'],1),4000)
        self.assertEqual(next(t['amount_cents'] for t in w.journal if t['kind']=='machine_purchase'),120000)

    def test_every_posting_reconciles_with_fine_units_and_crisis(self):
        w=World(goods_unit_scale=100);w.banking.request(w)
        accounts=dict(w.initial);last=0
        for step in range(100):
            if step==20:w.crisis.queue(w,'both',3,6000)
            w.step(False)
            for t in w.journal[last:]:
                self.assertEqual(accounts[t['source']],t['source_before'])
                self.assertEqual(accounts[t['target']],t['target_before'])
                if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                self.assertEqual(accounts[t['source']],t['source_after'])
                self.assertEqual(accounts[t['target']],t['target_after'])
            self.assertEqual(accounts,{k:n['cash_cents'] for k,n in w.nodes.items()})
            last=len(w.journal)
