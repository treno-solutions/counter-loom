"""Mechanism checks for household reserves, fiscal timing and financed orders."""
import unittest
from unittest.mock import patch
from world import World
from systems import HouseholdInput,HouseholdSystem
from firms import plan,outlook


class StabilizationTests(unittest.TestCase):
    def household(self,opening):
        return HouseholdSystem.outputs(HouseholdInput(240000,0,72000,0,opening+168000,100,100000,'liquidity_target',opening,3,12))

    def test_opening_reserve_does_not_count_current_wages_twice(self):
        self.assertEqual(self.household(300000)['desired_budget'],168000)
        self.assertEqual(self.household(420000)['desired_budget'],178000)
        self.assertEqual(self.household(180000)['desired_budget'],158000)

    def test_income_rules_keep_original_95_and_100_percent_meaning(self):
        for quota,expected in [(95,159600),(100,168000)]:
            self.assertEqual(HouseholdSystem.outputs(HouseholdInput(240000,0,72000,0,999999,quota))['desired_budget'],expected)

    def review_sequence(self,policy,balances,**kwargs):
        w=World(fiscal_policy=policy,**kwargs)
        base=w.budget.amounts(w)
        for m,balance in enumerate(balances,1):
            w.month=m
            a=dict(base,commitment_balance_cents=balance,recurring_taxes_cents=base['committed_spending_cents']+balance)
            with patch.object(w.budget,'amounts',return_value=a):w.budget.review(w)
        return w

    def test_same_quarter_totals_have_same_structural_decision(self):
        a=self.review_sequence('quarterly',[-20000,-20000,10000])
        b=self.review_sequence('quarterly',[10000,-20000,-20000])
        self.assertEqual(a.budget.decision,b.budget.decision)
        self.assertEqual(a.budget.next_procurement_bps,7500)

    def test_small_deficit_does_not_trigger_cut_when_financed(self):
        w=self.review_sequence('buffered_quarterly',[-100,-100,-100])
        self.assertEqual(w.budget.decision,'hold')
        self.assertEqual(w.budget.projected_deficit_cents,1200)
        self.assertGreater(w.budget.financing_headroom_cents,1200)

    def test_structural_cut_when_projected_gap_exceeds_available_financing(self):
        w=self.review_sequence('buffered_quarterly',[-10000]*3,government_initial_cash_cents=0,government_credit_limit_cents=0)
        self.assertEqual(w.budget.decision,'cut_procurement')

    def test_bank_without_equity_is_not_counted_as_available_credit(self):
        w=World(fiscal_policy='buffered_quarterly')
        w.pay('bank','h1',w.nodes['bank']['cash_cents'],'fixture','Explicit test transfer')
        base=w.budget.amounts(w)
        for m in (1,2,3):
            w.month=m
            with patch.object(w.budget,'amounts',return_value=dict(base,commitment_balance_cents=-100)):
                w.budget.review(w)
        self.assertEqual(w.budget.review_credit_cents,0)

    def order_world(self):
        w=World.stable();w.month=3
        w.nodes['alltag']['company']['short_months']=2
        w.capital_orders.place_if_needed(w)
        return w

    def test_financed_order_increases_supplier_production_and_is_not_duplicated(self):
        w=self.order_world();supplier=w.nodes['werkstatt']
        supplier['company']['forecast_milli']=0
        self.assertEqual(plan(supplier,1)['needed_units'],800)
        w.capital_orders.place_if_needed(w)
        self.assertEqual(len(w.capital_orders.orders),1)
        self.assertEqual(w.nodes['alltag']['capital'],0)
        for _ in range(5):w.step(False)
        p=w.capital_orders.orders[0]
        self.assertEqual(p['delivery_month'],4)
        self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(w.nodes['alltag']['company']['plan']['capacity_units'],7200)
        self.assertEqual(len([t for t in w.journal if t['kind']=='investment']),1)
        w.step(False)
        self.assertEqual(w.nodes['alltag']['company']['plan']['capacity_units'],7600*w.nodes['alltag']['company']['work_bps']//10000)

    def test_order_cash_cannot_be_distributed_or_used_for_other_payments(self):
        w=self.order_world();locked=w.capital_orders.locked('alltag')
        w.pay('alltag','h1',w.nodes['alltag']['cash_cents'],'fixture','Explicit test transfer')
        self.assertEqual(w.nodes['alltag']['cash_cents'],locked)
        w.capital_orders.check(w)
        with self.assertRaises(ValueError):w.banking.request(w)

    def test_order_waits_through_closure_without_early_payment_or_capacity(self):
        w=self.order_world();w.crisis.queue(w,'both',1,6000)
        for _ in range(5):w.step(False)
        self.assertIsNotNone(w.capital_orders.pending)
        self.assertEqual(w.nodes['alltag']['capital'],0)
        self.assertFalse(any(t['kind']=='investment' for t in w.journal))
        for _ in range(5):w.step(False)
        self.assertEqual(w.nodes['alltag']['capital'],1)

    def test_order_uses_bound_price_and_no_partial_delivery_receipts(self):
        w=self.order_world();n=w.nodes['werkstatt'];n['company']['forecast_milli']=0
        n['employees'].remove('h4');w.nodes['h4']['employer']=None
        self.assertEqual(outlook(n,1,1,2500)['expected_receipts_cents'],0)
        n['price']=300
        self.assertEqual(outlook(n,1,1,5000)['expected_receipts_cents'],120000)

    def test_profitable_order_can_restart_mothballed_supplier(self):
        w=World.stable();w.month=3;w.phase=4
        n=w.nodes['werkstatt'];c=n['company']
        for worker in n['employees']:w.nodes[worker]['employer']=None
        n['employees']=[]
        c.update(status='mothballed',next_status='mothballed',work_bps=0,next_work_bps=0,forecast_milli=0)
        w.nodes['alltag']['company']['short_months']=2
        w.capital_orders.place_if_needed(w)
        for month in (3,4):
            w.month=month;w.close_company(n)
        self.assertEqual(c['next_status'],'restarting')
        self.assertEqual(c['restart_signal'],2)
        self.assertEqual(len(n['employees']),1)

    def test_quarterly_review_preserves_actual_observation_month(self):
        w=self.review_sequence('buffered_quarterly',[-100]*4)
        review=w.budget.review_snapshot(w)
        self.assertEqual(review['month'],4)
        self.assertEqual(review['as_of_month'],3)
        self.assertEqual(review['basis_kind'],'quarter_financing')

    def test_reference_inputs_and_demand_recovery_are_explicit(self):
        w=World.stable()
        self.assertEqual(w.propensity,100)
        w.queue('demand')
        for _ in range(5):w.step(False)
        self.assertEqual(w.propensity,65)
        w.queue('demand_recovery');w.step(False)
        self.assertEqual(w.propensity,100)


if __name__=='__main__':unittest.main()
