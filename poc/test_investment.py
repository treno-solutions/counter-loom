"""Economic project appraisal, rate boundary and real order/credit settlement."""
from copy import deepcopy
import unittest
from investment import appraise,present_value
from world import World


def month(w):
    for _ in range(5):w.step(False)


class InvestmentTests(unittest.TestCase):
    def test_discounting_and_no_double_counting_loan_principal(self):
        self.assertEqual(present_value([(0,-10000),(1,11000)],12000),0)
        w=World.stable();f=w.nodes['alltag']
        a=appraise(f,120000,1,0,0)
        self.assertEqual(a['cash_npv_cents'],a['monthly_after_tax_cents']*24-120000)
        self.assertEqual(a['loan_npv_cents'],a['cash_npv_cents'])
        self.assertEqual(sum(r['principal_cents'] for r in a['loan_schedule']),120000)
        self.assertEqual(a['loan_interest_cents'],0)

    def test_boundary_project_changes_sign_without_changing_cashflows(self):
        w=World.stable();f=w.nodes['alltag'];f['capital']=15
        low=appraise(f,120000,1,200,600);high=appraise(f,120000,1,500,900)
        self.assertEqual(low['monthly_after_tax_cents'],high['monthly_after_tax_cents'])
        self.assertGreater(low['cash_npv_cents'],0);self.assertLess(high['cash_npv_cents'],0)
        self.assertLess(high['loan_npv_cents'],low['loan_npv_cents'])
        self.assertGreater(high['loan_interest_cents'],low['loan_interest_cents'])

    def test_no_demand_or_no_workers_does_not_create_returns(self):
        w=World.stable();f=w.nodes['alltag'];f['company']['forecast_milli']=0
        self.assertLess(appraise(f,120000,1,200,600)['cash_npv_cents'],0)
        f['employees']=[];f['company']['forecast_milli']=6000000
        a=appraise(f,120000,1,200,600)
        self.assertEqual(a['monthly_after_tax_cents'],0)
        self.assertLess(a['cash_npv_cents'],0)

    def test_real_cash_order_waits_for_goods_and_capacity_not_forecast_cash(self):
        w=World.stable();w.month=3;w.capital_orders.place_if_needed(w)
        p=w.capital_orders.pending;self.assertIsNotNone(p)
        self.assertEqual(w.nodes['alltag']['capital'],0)
        self.assertFalse(any(t['kind']=='investment' for t in w.journal))
        w.capital_orders.place_if_needed(w);self.assertEqual(len(w.capital_orders.orders),1)
        month(w);self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(sum(t['amount_cents'] for t in w.journal if t['kind']=='investment'),120000)
        w.check()

    def test_unprofitable_project_does_not_lock_cash_or_create_debt(self):
        w=World.stable();w.month=3;w.nodes['alltag']['capital']=15
        w.monetary.rate_bps=500
        a=w.capital_orders.review(w);self.assertEqual(a['decision'],'unprofitable')
        before=deepcopy(w.nodes);w.capital_orders.place_if_needed(w)
        self.assertIsNone(w.capital_orders.pending);self.assertEqual(w.nodes,before)
        w.banking.loan.status='requested';w.banking.originate(w)
        self.assertEqual(w.banking.loan.status,'available')
        self.assertEqual(w.banking.created,0)

    def test_cash_shortfall_requests_credit_with_debt_service_buffer(self):
        w=World.stable();w.month=3;f=w.nodes['alltag']
        _,reserve=w.company_staffing(f)
        w.pay('alltag','h1',f['cash_cents']-(reserve+40000),'fixture','Fixture financing port')
        a=w.capital_orders.review(w);self.assertEqual(a['decision'],'seek_credit')
        w.capital_orders.place_if_needed(w);self.assertEqual(w.banking.loan.status,'requested')
        w.nodes['werkstatt']['inventory']=800;w.nodes['werkstatt']['company']['inventory_value_cents']=0
        self.assertTrue(w.banking.originate(w));self.assertEqual(w.banking.created,120000)
        w.banking.deliver(w);self.assertEqual(f['capital'],1)
        self.assertEqual(w.banking.loan.outstanding_cents,120000)
        self.assertEqual(f['company']['last_investment_month'],w.month)
        self.assertIsNone(w.capital_orders.pending)
        w.check()

    def test_lead_time_and_higher_energy_reduce_economic_value(self):
        w=World.stable();f=w.nodes['alltag'];f['company']['forecast_milli']=10000000
        a=appraise(f,120000,1,200,600);delayed=appraise(f,120000,1,200,600,1)
        costly=appraise(f,120000,2,200,600)
        self.assertLess(delayed['cash_npv_cents'],a['cash_npv_cents'])
        self.assertLess(costly['cash_npv_cents'],a['cash_npv_cents'])
        self.assertGreater(a['additional_sales_cents'],0)

    def test_pending_closed_cooldown_and_floor_are_separate_from_profitability(self):
        w=World.stable();a=w.capital_orders.review(w);self.assertEqual(a['decision'],'cooldown')
        w.month=3;w.capital_orders.place_if_needed(w)
        self.assertEqual(w.capital_orders.review(w)['decision'],'pending')
        self.assertEqual(w.capital_orders.assessment['month'],3)
        self.assertEqual(len(w.capital_orders.assessments),2)
