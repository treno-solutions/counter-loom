"""Hours, bounded bridge and restart: full steps plus isolated decision ports."""
import unittest
from copy import deepcopy
from world import World
from firms import outlook,staffing

class BusinessOperationTests(unittest.TestCase):
    def finish(self,w):
        for _ in range(5):w.step()

    def test_half_time_pays_half_wages_and_scales_capacity(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];n['company']['next_work_bps']=5000
        w.step();p=n['company']['plan']
        self.assertEqual((p['wage_per_worker_cents'],p['wages_due_cents']),(120000,240000))
        self.assertEqual((p['capacity_units'],n['metrics']['produced_units']),(36,36))
        self.assertEqual(w.nodes['h1']['metrics']['income'],120000)
        w.step();self.assertEqual(w.nodes['h1']['metrics']['tax'],36000)

    def test_capacity_rounds_combined_work_and_machine_once(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];n['employees'].remove('h2');w.nodes['h2']['employer']=None
        n['capital']=1;n['company']['forecast_milli']=10000;n['company']['next_work_bps']=3250
        w.step()
        self.assertEqual(n['company']['plan']['capacity_units'],13)
        self.assertEqual(n['metrics']['produced_units'],13)
        self.assertEqual(n['metrics']['wages'],78000)

    def test_low_demand_supports_fractional_work(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];n['company']['forecast_milli']=10000
        self.assertEqual(staffing(n,1)[0],1)
        option=outlook(n,1,1,3612)
        self.assertEqual(option['projected_gap_cents'],0)
        self.assertLess(option['wages_cents'],240000)

    def test_active_hours_change_at_most_25_points(self):
        w=World()
        for month in range(1,25):
            if month==5:w.queue('demand')
            self.finish(w)
            for key in ('alltag','werkstatt'):
                c=w.nodes[key]['company']
                if c['status']!='mothballed' and c['next_status']!='mothballed':
                    self.assertLessEqual(abs(c['next_work_bps']-c['work_bps']),2500)
                    self.assertGreaterEqual(c['next_work_bps'],2500)

    def test_exhausted_loss_budget_stops_next_month_but_keeps_assets_and_debt(self):
        w=World();n=w.nodes['alltag'];n['company']['forecast_milli']=0
        self.finish(w)
        self.assertEqual(n['company']['next_status'],'mothballed')
        self.assertEqual(n['employees'],[])
        self.assertGreater(n['company']['loss_used_cents'],n['company']['loss_budget_cents'])
        cash=n['cash_cents'];balances=(n['loan'],n['inventory'],n['capital'])
        w.step()
        self.assertEqual((n['metrics']['wages'],n['metrics']['produced_units']),(0,0))
        self.assertEqual((n['loan'],n['inventory'],n['capital']),balances)
        self.assertEqual(cash-n['cash_cents'],n['company']['plan']['interest_due_cents'])

    def suspend(self,w):
        n=w.nodes['alltag']
        for worker in n['employees']:w.nodes[worker]['employer']=None
        n['employees']=[];c=n['company'];c['status']=c['next_status']='mothballed';c['work_bps']=c['next_work_bps']=0
        w.month=1;w.phase=4
        return n

    def test_restart_needs_two_funded_checks_and_acts_next_month(self):
        w=World(goods_unit_scale=1);n=self.suspend(w);n['company']['forecast_milli']=60000;n['company']['bridge_months']=3
        w.close_company(n)
        self.assertEqual(n['company']['next_status'],'mothballed')
        self.assertEqual(n['company']['restart_signal'],1)
        n['company']['forecast_milli']=60000;w.month+=1;w.close_company(n)
        self.assertEqual(n['company']['next_status'],'restarting')
        self.assertEqual(len(n['employees']),1)
        self.assertEqual(n['company']['work_bps'],0)
        self.assertEqual(n['company']['bridge_months'],0)
        w.step();self.assertGreater(n['metrics']['produced_units'],0)

    def test_no_cash_prevents_restart_despite_orders(self):
        w=World();n=self.suspend(w)
        w.pay('alltag','h1',n['cash_cents'],'fixture','Explicit liquidity transfer')
        for month in (1,2,3):
            w.month=month;n['company']['forecast_milli']=60000;w.close_company(n)
        self.assertEqual(n['company']['next_status'],'mothballed')
        self.assertEqual(n['company']['restart_signal'],0)
        self.assertFalse(n['company']['result']['cash_ok'])

    def test_budget_and_three_consecutive_bridges_limit_continuation(self):
        for used,months,expected in ((0,0,'buffered'),(480000,0,'mothballed'),(0,3,'mothballed')):
            w=World();n=w.nodes['alltag'];w.month=1;w.phase=4
            n['company']['forecast_milli']=10000;n['company']['loss_used_cents']=used;n['company']['bridge_months']=months
            cash=n['cash_cents'];w.close_company(n)
            self.assertEqual(n['company']['next_status'],expected)
            self.assertEqual(n['cash_cents'],cash)
            self.assertGreater(n['company']['result']['projected_gap_cents'],0)

    def test_hiring_reserve_uses_step_limited_work_share(self):
        w=World();n=w.nodes['alltag'];w.nodes['h2']['employer']=None;n['employees'].remove('h2')
        n['company']['forecast_milli']=37000;n['metrics']['sold_units']=37;n['company']['staff_signal']=1
        w.pay('alltag','h1',n['cash_cents']-700000,'fixture','Explicit liquidity transfer')
        w.month=1;w.phase=4;w.close_company(n)
        self.assertEqual(len(n['employees']),1)

    def test_budget_reset_precedes_next_plan_decision(self):
        w=World();n=w.nodes['werkstatt'];c=n['company'];c['loss_used_cents']=480000;c['profitable_months']=1
        n['metrics']['sales']=10000;n['metrics']['sold_units']=32
        w.month=1;w.phase=4;w.close_company(n)
        self.assertEqual(c['loss_used_cents'],0)
        self.assertEqual(c['next_status'],'buffered')

    def test_export_freezes_historical_hours_and_states(self):
        w=World()
        for _ in range(3):self.finish(w)
        before=deepcopy(w.history[0]);out=w.snapshot(export=True)
        self.assertIn('work_bps',out['all_history'][0]['market']['firms'][0])
        out['all_history'][0]['market']['firms'][0]['work_bps']=0
        self.assertEqual(w.history[0],before)
