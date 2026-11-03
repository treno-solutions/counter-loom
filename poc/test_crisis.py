"""Mandated closure: contracts, accounting, real goods and paired continuations."""
import json
import unittest
from world import World, world_request, WORLDS
from crisis import compare


def months(w,n):
    for _ in range(n*5):w.step()


class ClosureTests(unittest.TestCase):
    def test_next_boundary_duration_contracts_sales_and_reopening(self):
        w=World();months(w,2)
        f=w.nodes['werkstatt'];workers=list(f['employees']);old_work=f['company']['next_work_bps']
        w.crisis.queue(w,'werkstatt',2,6000)
        self.assertFalse(w.crisis.closed(w,'werkstatt'))
        for month in (3,4):
            months(w,1)
            self.assertTrue(w.crisis.closed(w,'werkstatt'))
            self.assertEqual(f['employees'],workers)
            self.assertEqual((f['metrics']['wages'],f['metrics']['sales'],f['metrics']['produced_units']),(0,0,0))
            self.assertEqual(f['company']['plan']['work_bps'],0)
            self.assertEqual(f['company']['next_work_bps'],old_work)
            self.assertEqual(f['metrics']['closure_cost'],30000)
            self.assertGreater(f['metrics']['interest_expense'],0)
            self.assertFalse(any(t['month']==month and t['kind']=='company_dividend' and t['source']=='werkstatt' for t in w.journal))
        w.step();self.assertFalse(w.crisis.closed(w,'werkstatt'))
        self.assertEqual(f['company']['plan']['work_bps'],old_work)
        self.assertGreater(f['metrics']['wages'],0)

    def test_reference_net_and_actual_transfer_tax_and_primary_balance(self):
        w=World();w.crisis.queue(w,'werkstatt',1,6000);w.step();w.step()
        for key in ('h3','h4'):
            self.assertEqual(w.nodes[key]['metrics']['short_time'],100800)
            self.assertEqual(w.nodes[key]['metrics']['tax'],0)
            self.assertEqual(w.nodes[key]['metrics']['income'],100800)
        self.assertEqual(w.crisis.snapshot(w)['monthly_paid_cents'],201600)
        fiscal=w.treasury.monthly(w)
        primary=sum(t['amount_cents'] for t in w.journal if t['source']=='staat' and t['kind'] in ('wage','transfer','short_time','procurement'))
        self.assertEqual(fiscal['primary_spending_cents'],primary)
        self.assertEqual(w.treasury.planned_primary_cents,720000+201600)

    def test_reference_uses_part_time_not_full_time_and_midmonth_queue_waits(self):
        w=World();w.nodes['werkstatt']['company']['next_work_bps']=2500
        w.step();w.step()
        before=w.nodes['h3']['metrics']['income']
        w.crisis.queue(w,'werkstatt',1,6000)
        self.assertFalse(w.crisis.closed(w,'werkstatt'))
        self.assertEqual(w.nodes['h3']['metrics']['income'],before)
        while w.phase!=4:w.step()
        next_work=w.nodes['werkstatt']['company']['next_work_bps']
        w.step();w.step()
        gross=240000*next_work//10000
        self.assertEqual(w.nodes['h3']['metrics']['short_time'],(gross-gross*30//100)*6000//10000)

    def test_blocked_public_purchase_does_not_originate_a_payment_loan(self):
        w=World(government_initial_cash_cents=0)
        w.crisis.queue(w,'werkstatt',1,0)
        w.month=1;w.crisis.begin_month(w)
        w.nodes['werkstatt']['inventory']=10
        w.nodes['werkstatt']['company']['inventory_value_cents']=100000
        self.assertEqual(w.buy('staat','werkstatt',120000,'procurement'),0)
        self.assertEqual(w.treasury.outstanding_cents,0)
        self.assertFalse(w.journal)

    def test_no_support_and_no_automatic_unemployment_transfer(self):
        w=World();w.crisis.queue(w,'both',3,0);months(w,3)
        for key in ('h1','h2','h3','h4'):
            self.assertEqual(w.nodes[key]['metrics']['income'],0)
            self.assertIsNotNone(w.nodes[key]['employer'])
        self.assertFalse(any(t['kind']=='short_time' for t in w.journal))
        self.assertTrue(all(h['closure_gap_cents']<=h['stock_gap_cents'] for m in w.history for h in m['households']))

    def test_unfunded_state_payment_is_visible_not_invented_income(self):
        w=World(government_initial_cash_cents=0,government_credit_limit_cents=0)
        w.crisis.queue(w,'both',1,6000);w.step();w.step()
        self.assertEqual(w.crisis.snapshot(w)['monthly_paid_cents'],0)
        self.assertEqual(w.crisis.snapshot(w)['unpaid_cents'],403200)
        self.assertTrue(all(w.nodes[h]['metrics']['short_time']==0 for h in ('h1','h2','h3','h4')))
        w.check()

    def test_machine_reservation_survives_closed_supplier(self):
        w=World(goods_unit_scale=1);w.banking.request(w)
        for _ in range(4):w.step()
        self.assertEqual(w.banking.loan.status,'credited')
        # Queue normally takes effect next month; a credited contract awaiting funds
        # can span the boundary and must keep its protected stock.
        w.crisis.episodes.append(dict(firms=['werkstatt'],start_month=1,end_month=1,replacement_bps=0,workers=[]))
        reserved=w.nodes['werkstatt']['reserved_units'];cash=w.nodes['alltag']['cash_cents']
        w.banking.deliver(w)
        self.assertEqual(w.banking.loan.status,'credited')
        self.assertEqual(w.nodes['werkstatt']['reserved_units'],reserved)
        self.assertEqual(w.nodes['alltag']['cash_cents'],cash)

    def test_paired_continuations_identical_start_unmodified_source_and_determinism(self):
        w=World();months(w,3);before=json.dumps(w.snapshot(export=True),sort_keys=True)
        result=compare(w,'werkstatt',2,6000)
        self.assertEqual(before,json.dumps(w.snapshot(export=True),sort_keys=True))
        self.assertEqual(result,compare(w,'werkstatt',2,6000))
        a,b=result['branches'];self.assertEqual(len(a['rows']),8)
        self.assertEqual(a['total_short_time_cents'],0)
        self.assertGreater(b['total_short_time_cents'],0)
        self.assertGreater(b['rows'][0]['household_net_cents'],a['rows'][0]['household_net_cents'])
        self.assertEqual(a['rows'][0]['employment'],b['rows'][0]['employment'])

    def test_api_validation_conflicts_and_repeat_episode(self):
        w=World();WORLDS[w.id]=w
        for bad in [True,0,13,1.5]:
            with self.assertRaises(ValueError):w.crisis.queue(w,'werkstatt',bad,6000)
        with self.assertRaises(ValueError):w.crisis.queue(w,'other',1,6000)
        with self.assertRaises(ValueError):w.crisis.queue(w,'werkstatt',1,10001)
        w.crisis.queue(w,'werkstatt',1,0)
        with self.assertRaises(ValueError):w.crisis.queue(w,'alltag',1,0)
        months(w,2);w.crisis.queue(w,'alltag',1,6000);months(w,1)
        self.assertEqual(len(w.crisis.episodes),2)
        with self.assertRaises(ValueError):world_request('closure',dict(world_id=w.id,revision=-1,firm='both',duration=1,replacement_bps=0))
        with self.assertRaises(ValueError):world_request('closure',dict(world_id=w.id,revision=w.revision,firm='both',duration=1,replacement_bps=0,extra=True))

    def test_independent_ledger_and_inventory_reconstruction_during_and_after_crisis(self):
        for rate in (0,6000,10000):
            w=World();w.crisis.queue(w,'both',3,rate);accounts=dict(w.initial);seen=0
            for _ in range(60):
                w.step()
                for t in w.journal[seen:]:
                    self.assertEqual(accounts[t['source']],t['source_before'])
                    self.assertEqual(accounts[t['target']],t['target_before'])
                    if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                    if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                    self.assertEqual(accounts[t['source']],t['source_after'])
                    self.assertEqual(accounts[t['target']],t['target_after'])
                seen=len(w.journal)
                self.assertEqual(accounts,{k:n['cash_cents'] for k,n in w.nodes.items()})
                for f in ('alltag','werkstatt'):
                    n=w.nodes[f];p=n['company']['plan'];m=n['metrics']
                    self.assertEqual(n['inventory'],p['opening_units']+m['produced_units']-m['sold_units'])
                    self.assertEqual(n['company']['inventory_value_cents'],p['opening_value_cents']+m['production_cost']-m['cost_of_sales'])
