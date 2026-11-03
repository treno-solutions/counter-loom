"""Business identities and boundary behaviour, separate from bank assertions."""
import unittest
from world import World
from firms import plan, staffing, forecast

class FirmTests(unittest.TestCase):
    def test_full_stock_stops_production_but_not_payroll(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];n['inventory']=100
        w.step()
        self.assertEqual(n['metrics']['produced_units'],0)
        self.assertEqual(n['metrics']['wages'],480000)
        self.assertEqual(n['metrics']['idle_cost'],480000)
        self.assertEqual(n['metrics']['production_cost'],0)
        self.assertFalse(any(t['kind']=='energy' and t['source']==n['id'] for t in w.journal))

    def test_stock_cost_and_result_reconstructed_across_scenarios(self):
        for case in ('baseline','energy','demand','both','recovery','loan'):
            w=World()
            if case=='loan':w.banking.request(w)
            for i in range(120):
                if i==15:
                    if case in ('energy','both'):w.queue('energy')
                    if case in ('demand','both','recovery'):w.queue('demand')
                if i==60 and case=='recovery':w.queue('demand_recovery')
                w.step()
                for key in ('alltag','werkstatt'):
                    n=w.nodes[key];c=n['company'];m=n['metrics'];p=c['plan']
                    self.assertEqual(n['inventory'],p['opening_units']+m['produced_units']-m['sold_units'])
                    self.assertEqual(c['inventory_value_cents'],p['opening_value_cents']+m['production_cost']-m['cost_of_sales'])
                    if w.phase==4:
                        r=c['result'];tx=[t for t in w.journal if t['month']==w.month and t['source']==key and t['kind'] in ('company_dividend','company_extra_dividend')]
                        self.assertEqual(r['profit_before_tax_cents'],m['sales']-m['cost_of_sales']-m['idle_cost']-m['unpaid_wages']-m['interest_expense'])
                        self.assertEqual(r['distribution_cents'],sum(t['amount_cents'] for t in tx))
                        self.assertLessEqual(c['profit_allocation']['regular_paid_cents'],max(0,r['after_tax_cents'])//2)
                        self.assertLessEqual(r['distribution_cents'],c['profit_allocation']['eligible_profit_cents'])
                        self.assertEqual(r['after_tax_cents'],r['distribution_cents']+r['retained_result_cents'])
                        if r['distribution_cents']:self.assertGreaterEqual(n['cash_cents'],r['reserve_cents'])

    def test_cost_remainder_leaves_with_last_unit(self):
        w=World();n=w.nodes['alltag'];n['inventory']=3;n['company']['inventory_value_cents']=100
        for _ in range(3):w.buy('h1','alltag',10000)
        self.assertEqual(n['company']['inventory_value_cents'],0)
        self.assertEqual(n['metrics']['cost_of_sales'],100)

    def test_unfunded_orders_do_not_increase_forecast(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];c=n['company']
        forecast(c,0)
        self.assertEqual(c['forecast_milli'],45000)
        self.assertEqual(plan(n,1)['demand_units'],45)

    def test_existing_arrears_block_positive_profit_distribution(self):
        w=World()
        for _ in range(4):w.step()
        w.obligations.append(dict(month=1,source='alltag',target='h1',amount_cents=1,kind='wage'))
        w.step();r=w.nodes['alltag']['company']['result']
        self.assertGreater(r['profit_before_tax_cents'],0)
        self.assertEqual(r['distribution_cents'],0)

    def test_no_demand_and_exhausted_loss_budget_mothballs_from_next_month(self):
        w=World();n=w.nodes['alltag'];n['company']['forecast_milli']=0
        for _ in range(5):w.step()
        self.assertEqual(n['company']['plan']['staff'],2)
        self.assertEqual(len(n['employees']),0)
        self.assertEqual(n['company']['next_status'],'mothballed')
        w.step()
        self.assertEqual(n['company']['status'],'mothballed')
        self.assertEqual(n['metrics']['wages'],0)
        self.assertEqual(w.nodes['h2']['employer'],None)

    def test_recovery_only_after_shock_and_completed_world_rejects_mutations(self):
        w=World(horizon_months=24)
        with self.assertRaises(ValueError):w.queue('demand_recovery')
        w.queue('demand');w.step();w.queue('demand_recovery')
        for _ in range(119):w.step()
        before=w.snapshot()
        for event in ('energy','demand_recovery'):
            with self.assertRaises(ValueError):w.queue(event)
        with self.assertRaises(ValueError):w.banking.request(w)
        with self.assertRaises(ValueError):w.step()
        self.assertEqual(before,w.snapshot())

    def test_working_buffer_covers_retained_staff_and_next_loan_instalment(self):
        w=World(goods_unit_scale=1);w.banking.request(w)
        for _ in range(5):w.step()
        for key in ('alltag','werkstatt'):
            n=w.nodes[key];r=n['company']['result']
            self.assertGreaterEqual(r['reserve_cents'],2*len(n['employees'])*(240000*n['company']['next_work_bps']//10000))
        n=w.nodes['alltag'];r=n['company']['result']
        due=w.banking.due(w,2)
        self.assertEqual(due['total_cents'],10600)
        self.assertGreaterEqual(r['reserve_cents'],2*len(n['employees'])*(240000*n['company']['next_work_bps']//10000)+10600)

    def test_late_credit_request_is_allowed_before_final_close(self):
        # Preserve the V11 stock fixture; the surplus policy has a different demand path.
        w=World(goods_unit_scale=1,horizon_months=24,distribution_policy='legacy',fiscal_policy='legacy')
        for _ in range(116):w.step()
        self.assertEqual((w.month,w.phase),(24,0))
        w.banking.request(w)
        for _ in range(4):w.step()
        self.assertTrue(w.snapshot()['completed'])
        self.assertEqual(w.banking.loan.status,'delivered')
        self.assertEqual(w.banking.loan.outstanding_cents,120000)

    def test_credit_after_last_investment_phase_is_rejected_without_mutation(self):
        w=World(horizon_months=24)
        for _ in range(119):w.step()
        self.assertEqual((w.month,w.phase),(24,3))
        before=w.snapshot()
        with self.assertRaises(ValueError):w.banking.request(w)
        self.assertEqual(before,w.snapshot())


class OperatorConsistencyTests(unittest.TestCase):
    def test_capital_does_not_remove_every_required_operator(self):
        w=World();firm=w.nodes['alltag'];firm['capital']=10
        firm['company']['forecast_milli']=40000
        desired,_=staffing(firm,1)
        self.assertEqual(desired,1)
        firm['employees']=[]
        self.assertEqual(plan(firm,1)['capacity_units'],0)
        self.assertEqual(staffing(firm,1)[0],1)
