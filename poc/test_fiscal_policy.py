"""Liquidity-buffer policy, rather than a fixed initial-cash restoration rule."""
import unittest
from copy import deepcopy
from world import World

class FiscalPolicyTests(unittest.TestCase):
    def finish(self,w):
        for _ in range(5):w.step()

    def test_default_spends_existing_cash_instead_of_restoring_eighty_thousand(self):
        w=World(goods_unit_scale=1,distribution_tax_bps=0);self.finish(w);m=w.treasury.monthly(w)
        self.assertEqual(m['reserve_target_cents'],720000)
        self.assertEqual(m['closing_cash_cents'],7759440)
        self.assertEqual(m['budget_balance_cents'],-240560)
        self.assertEqual(m['reserve_draw_cents'],240560)
        self.assertEqual(m['credit_cents'],0)
        self.assertEqual(m['decision'],'hold')
        self.assertEqual(w.treasury.outstanding_cents,0)

    def test_borrow_only_the_target_gap_after_all_actual_flows(self):
        w=World(goods_unit_scale=1,distribution_tax_bps=0,government_initial_cash_cents=720000);self.finish(w);m=w.treasury.monthly(w)
        self.assertEqual(m['policy_cash_before_cents'],479440)
        self.assertEqual(m['policy_credit_need_cents'],240560)
        self.assertEqual(m['closing_cash_cents'],720000)
        self.assertEqual(m['decision'],'borrow')
        self.assertEqual(m['credit_cents'],240560)

    def test_surplus_below_target_builds_cash_without_repaying_debt(self):
        w=World(government_initial_cash_cents=0,government_credit_limit_cents=100000)
        w.month=1;w.phase=4;w.treasury.begin_month(w);w.treasury.issue(w,100000)
        w.pay('h1','staat',10000,'income_tax','Controlled tax receipt')
        w.treasury.close(w);m=w.treasury.monthly(w)
        self.assertEqual(m['budget_balance_cents'],10000)
        self.assertEqual(m['principal_repaid_cents'],0)
        self.assertEqual(w.nodes['staat']['cash_cents'],110000)
        self.assertEqual(m['decision'],'limited')
        self.assertEqual(m['unfunded_financing_cents'],610000)

    def test_existing_excess_pays_debt_but_keeps_the_target(self):
        w=World(government_initial_cash_cents=720000);w.month=1;w.phase=4;w.treasury.begin_month(w)
        w.treasury.issue(w,100000);w.treasury.close(w)
        self.assertEqual(w.nodes['staat']['cash_cents'],720000)
        self.assertEqual(w.treasury.outstanding_cents,0)
        self.assertEqual(w.treasury.monthly(w)['decision'],'repay')
        self.assertEqual(w.treasury.monthly(w)['policy_repayment_capacity_cents'],100000)

    def test_target_uses_month_open_transfers_and_current_interest(self):
        w=World(government_initial_cash_cents=720000)
        self.finish(w);debt=w.treasury.outstanding_cents;w.step()
        self.assertEqual(w.treasury.reserve_target_cents,720000+debt*300//120000)
        # Preserve the pre-adaptation procurement envelope in this financing fixture.
        w=World(fiscal_policy='legacy');w.queue('demand')
        for _ in range(15):w.step()
        w.step()
        expected=720000+sum(h['employer'] is None for h in w.households())*100000+w.treasury.month_interest_charge_cents
        self.assertEqual(w.treasury.reserve_target_cents,expected)

    def test_target_is_not_a_blocked_account_and_limit_does_not_create_money(self):
        w=World(goods_unit_scale=1,distribution_tax_bps=0,government_initial_cash_cents=720000,government_credit_limit_cents=0)
        self.finish(w);m=w.treasury.monthly(w)
        self.assertEqual(w.treasury.outstanding_cents,0)
        self.assertEqual(m['closing_cash_cents'],479440)
        self.assertEqual(m['unfunded_financing_cents'],240560)
        self.assertEqual(m['decision'],'limited')
        self.assertEqual(m['interest_paid_cents'],0)
        self.assertEqual(sum(h['metrics']['income'] for h in w.households()),1440000)

    def test_reserve_months_zero_and_two_and_invalid_inputs(self):
        for months,target in ((0,0),(2,1440000)):
            w=World(government_reserve_months=months);self.finish(w)
            self.assertEqual(w.treasury.reserve_target_cents,target)
        for kwargs in ({'government_reserve_months':-1},{'government_reserve_months':7},{'government_reserve_months':True},{'government_initial_cash_cents':-1},{'government_initial_cash_cents':True}):
            with self.assertRaises(ValueError):World(**kwargs)

    def test_history_and_export_freeze_decisions_and_close_is_idempotent(self):
        w=World(government_initial_cash_cents=720000);self.finish(w)
        first=deepcopy(w.treasury.history[0]);state=w.snapshot()
        w.treasury.close(w);self.assertEqual(state,w.snapshot())
        w.queue('energy');self.finish(w)
        self.assertEqual(w.treasury.history[0],first)
        out=w.snapshot(export=True);out['public_finance']['history'][0]['reserve_target_cents']=0
        self.assertEqual(w.treasury.history[0],first)
