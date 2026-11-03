"""Public spending decisions, real financing and explicit costs of adjustment."""
import unittest
from copy import deepcopy
from world import World


def months(w,n):
    for _ in range(5*n):w.step(emit_snapshot=False)

class PublicBudgetTests(unittest.TestCase):
    def test_three_deficits_cut_procurement_only_from_next_month(self):
        w=World();months(w,3)
        a=w.budget.monthly(w)
        self.assertEqual(a['procurement_bps'],10000)
        self.assertEqual(a['next_procurement_bps'],7500)
        self.assertEqual(a['decision'],'cut_procurement')
        self.assertEqual(a['decision_effective_month'],4)
        w.step()
        self.assertEqual(w.budget.plan['procurement_bps'],7500)
        self.assertEqual(w.budget.plan['payroll_cents'],480000)

    def test_no_funds_no_work_promises_and_released_workers_are_visible(self):
        w=World(government_initial_cash_cents=0,government_credit_limit_cents=0)
        w.step()
        self.assertEqual(w.budget.plan['approved_staff'],0)
        self.assertEqual(w.nodes['staat']['employees'],[])
        self.assertIsNone(w.nodes['h5']['employer']);self.assertIsNone(w.nodes['h6']['employer'])
        self.assertEqual(w.nodes['staat']['metrics']['wages'],0)
        self.assertFalse(any(o['source']=='staat' and o['kind']=='wage' for o in w.obligations))
        self.assertEqual(w.budget.plan['procurement_bps'],0)

    def test_partial_funding_creates_whole_fully_paid_job_not_partial_wage(self):
        w=World(government_initial_cash_cents=400000,government_credit_limit_cents=0)
        w.step()
        self.assertEqual(w.budget.plan['approved_staff'],1)
        self.assertEqual(w.nodes['staat']['metrics']['wages'],240000)
        paid=[t['amount_cents'] for t in w.journal if t['source']=='staat' and t['kind']=='wage']
        self.assertEqual(paid,[240000])
        self.assertEqual(w.budget.plan['social_need_cents'],100000)
        w.step();self.assertEqual(w.nodes['h6']['metrics']['transfers'],100000)

    def test_credit_must_be_confirmed_before_funded_work(self):
        w=World(government_initial_cash_cents=0,government_credit_limit_cents=500000)
        w.step()
        credits=[t for t in w.journal if t['kind']=='government_credit']
        wages=[t for t in w.journal if t['source']=='staat' and t['kind']=='wage']
        self.assertEqual(w.budget.plan['approved_staff'],2)
        self.assertTrue(credits and wages)
        self.assertLess(credits[0]['id'],wages[0]['id'])
        self.assertEqual(sum(t['amount_cents'] for t in wages),480000)

    def test_social_shortage_is_proportional_and_kug_claim_is_not_erased(self):
        w=World(government_initial_cash_cents=100000,government_credit_limit_cents=0)
        w.crisis.queue(w,'both',1,6000);w.step();w.step()
        paid=[w.nodes[h]['metrics']['transfers'] for h in ('h1','h2','h3','h4','h5','h6')]
        self.assertLessEqual(max(paid[:4])-min(paid[:4]),1)
        self.assertLessEqual(abs(paid[4]-paid[5]),1)
        self.assertEqual(sum(paid),100000)
        self.assertGreater(w.budget.monthly(w)['social_unfunded_cents'],0)
        self.assertGreater(w.crisis.snapshot(w)['unpaid_cents'],0)
        self.assertEqual(w.nodes['staat']['metrics']['wages'],0)

    def test_old_wage_claims_repaid_with_counterparty_and_tax(self):
        w=World()
        w.obligations=[dict(month=0,source='staat',target='h5',amount_cents=120000,kind='wage')]
        w.step();w.step()
        self.assertFalse(any(o['source']=='staat' and o['kind']=='wage' for o in w.obligations))
        self.assertEqual(w.budget.monthly(w)['wage_arrears_paid_cents'],120000)
        self.assertTrue(any(t['kind']=='public_wage_arrears' and t['target']=='h5' and t['amount_cents']==120000 for t in w.journal))
        self.assertTrue(any(t['kind']=='arrears_income_tax' and t['amount_cents']==36000 for t in w.journal))
        m=w.treasury.monthly(w)
        self.assertEqual(m['closing_cash_cents'],m['opening_cash_cents']-m['cash_deficit_cents']+m['credit_cents']-m['principal_repaid_cents'])

    def test_partial_old_wage_repayment_keeps_remaining_claim(self):
        w=World(government_initial_cash_cents=100000,government_credit_limit_cents=0)
        w.obligations=[dict(month=0,source='staat',target='h5',amount_cents=300000,kind='wage')]
        w.step();w.step()
        remaining=sum(o['amount_cents'] for o in w.obligations if o['source']=='staat' and o['kind']=='wage')
        paid=sum(t['amount_cents'] for t in w.journal if t['kind']=='public_wage_arrears')
        self.assertEqual((paid,remaining),(188000,112000))
        self.assertEqual(paid+remaining,300000)
        w.check()

    def test_unpaid_social_need_does_not_look_like_structural_surplus(self):
        w=World(distribution_tax_bps=0,government_initial_cash_cents=0,government_credit_limit_cents=0)
        w.crisis.queue(w,'both',3,6000);months(w,1)
        a=w.budget.monthly(w)
        self.assertEqual(w.treasury.monthly(w)['budget_balance_cents'],w.bank_profit.monthly['profit_tax_paid_cents'])
        self.assertLess(a['commitment_balance_cents'],0)
        self.assertGreater(a['social_unfunded_cents'],0)

    def test_public_restoration_requires_three_surpluses_and_recurring_coverage(self):
        w=World();w.budget.next_target_staff=1;w.budget.next_procurement_bps=0
        w.nodes['staat']['employees'].remove('h6');w.nodes['h6']['employer']=None
        for month in range(1,4):
            w.month=month;w.phase=4;w.budget.begin_month(w)
            w.pay('alltag','staat',600000,'profit_tax','Controlled recurring tax')
            w.budget.review(w)
            if month<3:self.assertEqual(w.budget.decision,'hold')
        self.assertEqual(w.budget.decision,'restore_staff')
        self.assertEqual(w.budget.next_target_staff,2)
        # No same-month hiring: changed target is applied at the next boundary.
        self.assertEqual(len(w.nodes['staat']['employees']),1)
        w.month=4;w.budget.begin_month(w)
        self.assertEqual(len(w.nodes['staat']['employees']),2)

    def test_legacy_mode_keeps_unfunded_wage_claims_for_reference(self):
        w=World(fiscal_policy='legacy',government_initial_cash_cents=0,government_credit_limit_cents=0)
        w.step()
        self.assertEqual(len(w.nodes['staat']['employees']),2)
        self.assertEqual(sum(o['amount_cents'] for o in w.obligations if o['source']=='staat' and o['kind']=='wage'),480000)

    def test_adaptive_no_new_wage_arrears_in_baseline_and_crises(self):
        for case in ('baseline','energy','demand','closure','zero_credit'):
            w=World(government_credit_limit_cents=0 if case=='zero_credit' else 5000000)
            if case in ('energy','demand'):w.queue(case)
            if case=='closure':w.crisis.queue(w,'both',6,6000)
            for _ in range(60):
                w.step()
                self.assertFalse(any(o['source']=='staat' and o['kind']=='wage' for o in w.obligations))
                self.assertEqual(w.nodes['staat']['metrics']['wages'],w.budget.plan['payroll_cents'])
                w.check()

    def test_history_is_frozen_and_review_idempotent(self):
        w=World();months(w,3);history=deepcopy(w.budget.history)
        before=w.snapshot();w.budget.review(w);self.assertEqual(before,w.snapshot())
        months(w,1);self.assertEqual(w.budget.history[:3],history)
        out=w.snapshot(export=True);out['all_budget_history'][0]['approved_staff']=99
        self.assertEqual(w.budget.history[0],history[0])

    def test_invalid_budget_mode_rejected(self):
        with self.assertRaises(ValueError):World(fiscal_policy='unknown')
