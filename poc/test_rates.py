"""Policy timing, fixed contracts, origination pricing and state rate cohorts."""
import unittest
from world import World, world_request, WORLDS

class RateTests(unittest.TestCase):
    def finish_month(self,w):
        for _ in range(5):w.step()

    def test_initial_contracts_and_offers(self):
        w=World();p=w.monetary.snapshot(w)
        self.assertEqual((p['rate_bps'],p['machine_offer_bps'],p['state_offer_bps']),(200,600,300))
        self.assertEqual([x['annual_rate_bps'] for x in p['contracts']],[200,200])
        self.assertEqual([x['monthly_interest_due_cents'] for x in p['contracts']],[2000,2000])

    def test_policy_next_month_variable_one_more_month_fixed_unchanged(self):
        w=World();self.finish_month(w);w.monetary.queue(w,400)
        self.assertEqual(w.monetary.rate_bps,200)
        w.step()
        self.assertEqual((w.month,w.monetary.rate_bps),(2,400))
        self.assertEqual(w.nodes['alltag']['loan_rate_bps'],200)
        self.assertEqual(w.nodes['alltag']['loan_next_rate_bps'],400)
        self.assertEqual(w.nodes['werkstatt']['loan_rate_bps'],200)
        self.assertEqual(w.nodes['alltag']['company']['plan']['interest_due_cents'],2000)
        for _ in range(5):w.step()
        self.assertEqual(w.nodes['alltag']['loan_rate_bps'],400)
        self.assertEqual(w.nodes['alltag']['company']['plan']['interest_due_cents'],4000)
        self.assertEqual(w.nodes['werkstatt']['company']['plan']['interest_due_cents'],2000)

    def test_existing_machine_is_fixed_and_offer_updates(self):
        w=World();w.banking.request(w);self.finish_month(w)
        w.monetary.queue(w,400);w.step()
        self.assertEqual(w.banking.loan.annual_rate_bps,600)
        self.assertEqual(w.monetary.machine_offer(),800)
        self.assertEqual(w.banking.loan.interest_paid_cents,600)
        self.assertEqual(w.banking.loan.policy_rate_at_issue_bps,200)

    def test_new_machine_locks_rate_at_issue_not_request(self):
        w=World();w.banking.request(w);w.monetary.queue(w,400)
        self.finish_month(w)
        self.assertEqual(w.banking.loan.annual_rate_bps,800)
        self.assertEqual(w.banking.loan.policy_rate_at_issue_bps,400)
        w.monetary.queue(w,0);w.step()
        self.assertEqual(w.banking.loan.interest_paid_cents,800)
        self.assertEqual(w.banking.loan.annual_rate_bps,800)
        self.assertEqual(w.monetary.machine_offer(),400)

    def test_waiting_machine_request_is_not_a_rate_lock(self):
        w=World();w.banking.request(w)
        w.nodes['werkstatt']['inventory']=0;w.phase=3;w.month=1
        w.banking.originate(w)
        self.assertEqual(w.banking.loan.status,'requested')
        w.monetary.queue(w,400);w.month=2;w.monetary.begin_month(w)
        w.nodes['werkstatt']['inventory']=8
        w.banking.originate(w)
        self.assertEqual(w.banking.loan.annual_rate_bps,800)

    def test_new_state_tranches_keep_old_and_new_fixed_rates(self):
        w=World(government_initial_cash_cents=720000);self.finish_month(w);old=w.treasury.tranches[0].copy()
        w.monetary.queue(w,400);self.finish_month(w)
        self.assertEqual(w.treasury.tranches[0]['annual_rate_bps'],300)
        self.assertEqual(w.treasury.tranches[-1]['annual_rate_bps'],500)
        expected=sum(t['outstanding_cents']*t['annual_rate_bps'] for t in w.treasury.tranches)//120000
        before=w.treasury.interest_charged_cents;w.step()
        self.assertEqual(w.treasury.interest_charged_cents-before,expected)
        self.assertEqual(sum(x['interest_cents'] for x in w.treasury.month_interest_basis),expected)
        self.assertEqual(w.treasury.tranches[0]['annual_rate_bps'],old['annual_rate_bps'])

    def test_state_fifo_repayment_and_interest_rounding(self):
        w=World();w.month=1;w.treasury.issue(w,100001)
        w.monetary.queue(w,400);w.month=2;w.monetary.begin_month(w)
        w.treasury.issue(w,200003);w.treasury.repay(w,150000)
        self.assertEqual([t['outstanding_cents'] for t in w.treasury.tranches],[0,150004])
        self.assertEqual([t['annual_rate_bps'] for t in w.treasury.tranches],[300,500])
        w.month=3;w.monetary.begin_month(w);w.treasury.begin_month(w)
        self.assertEqual(w.treasury.month_interest_charge_cents,150004*500//120000)
        w.check()

    def test_same_rates_aggregate_cents_instead_of_losing_fractional_cents(self):
        w=World();w.month=1
        for _ in range(3):w.treasury.issue(w,200)
        w.month=2;w.monetary.begin_month(w);w.treasury.begin_month(w)
        self.assertEqual(w.treasury.month_interest_charge_cents,1)
        self.assertEqual(sum(b['interest_cents'] for b in w.treasury.month_interest_basis),1)

    def test_cut_is_delayed_for_variable_and_does_not_reprice_fixed_state(self):
        w=World(government_initial_cash_cents=720000);self.finish_month(w);w.monetary.queue(w,0);self.finish_month(w)
        self.assertEqual(w.nodes['alltag']['loan_rate_bps'],200)
        self.assertEqual(w.treasury.tranches[0]['annual_rate_bps'],300)
        self.assertEqual(w.treasury.tranches[-1]['annual_rate_bps'],100)
        w.step()
        self.assertEqual(w.nodes['alltag']['loan_rate_bps'],0)
        self.assertEqual(w.nodes['werkstatt']['loan_rate_bps'],200)

    def test_pending_can_be_replaced_and_cancelled_without_effective_change(self):
        w=World();w.monetary.queue(w,400);w.monetary.queue(w,300)
        self.assertEqual(w.monetary.pending_rate_bps,300)
        w.monetary.queue(w,200)
        self.assertIsNone(w.monetary.pending_rate_bps)
        w.step();self.assertEqual(w.monetary.changes,[])

    def test_invalid_rates_and_final_month_do_not_mutate_state(self):
        w=World(horizon_months=24)
        for value in (-1,1001,True,2.5,'400',None):
            before=w.snapshot()
            with self.assertRaises(ValueError):w.monetary.queue(w,value)
            self.assertEqual(before,w.snapshot())
        for _ in range(120):w.step()
        before=w.snapshot()
        with self.assertRaises(ValueError):w.monetary.queue(w,400)
        self.assertEqual(before,w.snapshot())

    def test_rate_api_revision_guard_and_required_fields(self):
        s=world_request('create',{});p={'world_id':s['world_id'],'revision':s['revision'],'annual_rate_bps':400}
        updated=world_request('rate',p)
        self.assertEqual(updated['monetary_policy']['pending_rate_bps'],400)
        with self.assertRaises(ValueError):world_request('rate',p)
        with self.assertRaises(ValueError):world_request('rate',{'world_id':s['world_id'],'revision':updated['revision'],'event':'rate'})

    def test_rate_changes_do_not_reprice_existing_unpaid_interest(self):
        w=World();w.pay('alltag','h1',2400000,'fixture','Testanschluss')
        w.step();old=[o.copy() for o in w.obligations if o['source']=='alltag' and o['kind']=='interest']
        self.assertEqual(old[0]['amount_cents'],2000)
        w.monetary.queue(w,400)
        for _ in range(10):w.step()
        self.assertEqual(w.nodes['alltag']['loan_rate_bps'],400)
        self.assertEqual([o for o in w.obligations if o['month']==1 and o['source']=='alltag' and o['kind']=='interest'],old)
