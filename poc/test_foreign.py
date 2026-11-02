"""Counterparty, goods, working budget and inland/external bridges."""
import unittest
from world import World

class ForeignTradeTests(unittest.TestCase):
    def test_first_month_receipts_do_not_fund_same_month_exports(self):
        w=World()
        for _ in range(5):w.step()
        trade=w.foreign.snapshot(w)
        self.assertEqual(trade['month_imports_cents'],72000)
        self.assertEqual(trade['month_exports_cents'],0)
        self.assertEqual(trade['foreign_cash_cents'],72000)
        self.assertEqual(trade['domestic_cash_cents'],14528000)
        self.assertEqual(trade['plan']['budget_cents'],0)
        self.assertTrue(all(o['funded_units']==0 for o in trade['plan']['orders']))

    def test_next_month_exports_pay_and_deliver_whole_goods(self):
        w=World()
        for _ in range(10):w.step()
        t=w.foreign.snapshot(w);rows=t['deliveries']
        self.assertEqual(t['plan']['budget_cents'],72000)
        self.assertEqual(sum(d['amount_cents'] for d in rows),55000)
        self.assertEqual([(d['seller'],d['units']) for d in rows],[('alltag',4),('werkstatt',1)])
        for d in rows:
            payment=next(p for p in w.journal if p['id']==d['transaction_id'])
            self.assertEqual(payment['source'],'ausland')
            self.assertEqual(payment['target'],d['seller'])
            self.assertEqual(payment['amount_cents'],d['amount_cents'])
            self.assertEqual(d['inventory_before']-d['inventory_after'],d['units'])
            self.assertEqual(payment['deposit_delta_cents'],0)
            self.assertGreater(d['cost_cents'],0)

    def test_cash_available_but_no_stock_means_no_export(self):
        w=World();w.pay('staat','ausland',100000,'fixture','Expliziter Testanschluss')
        w.month=1;w.phase=2;w.foreign.begin_month(w)
        w.foreign.purchase(w)
        self.assertEqual(w.foreign.deliveries,[])
        self.assertEqual(w.nodes['ausland']['cash_cents'],100000)
        self.assertEqual(w.nodes['alltag']['metrics']['unmet_units'],6)
        self.assertEqual(w.nodes['werkstatt']['metrics']['unmet_units'],2)
        w.check()

    def test_reserved_goods_are_not_exported_and_execution_is_once_per_month(self):
        w=World();w.pay('staat','ausland',100000,'fixture','Expliziter Testanschluss')
        n=w.nodes['werkstatt'];n['inventory']=8;n['reserved_units']=8
        n['company']['inventory_value_cents']=80000
        w.month=1;w.phase=2;w.foreign.begin_month(w);w.foreign.purchase(w)
        self.assertEqual(n['inventory'],8)
        self.assertEqual(n['metrics']['unmet_units'],2)
        before=w.snapshot();w.foreign.purchase(w)
        self.assertEqual(before,w.snapshot())

    def test_budget_is_capped_even_when_energy_receipts_are_large(self):
        w=World();w.pay('staat','ausland',1000000,'fixture','Expliziter Testanschluss')
        w.step();p=w.foreign.plan
        self.assertEqual(p['budget_cents'],90000)
        self.assertEqual([x['allocated_cents'] for x in p['orders']],[60000,30000])

    def test_trade_and_domestic_bridges_and_goods_across_24_month_cases(self):
        for case in ('base','none','energy','demand','both','loan'):
            w=World(export_orders_units={'alltag':0,'werkstatt':0}) if case=='none' else World()
            if case=='loan':w.banking.request(w)
            for i in range(120):
                if i==10:
                    if case in ('energy','both'):w.queue('energy')
                    if case in ('demand','both'):w.queue('demand')
                w.step();t=w.foreign.snapshot(w);b=w.banking
                self.assertEqual(t['foreign_cash_cents'],t['cumulative_imports_cents']-t['cumulative_exports_cents'])
                self.assertEqual(t['domestic_cash_cents'],14600000+t['cumulative_net_inflow_cents']+b.created-b.repaid-b.interest_received+b.distributed)
                rows=[d for d in t['deliveries'] if d['month']==w.month]
                self.assertLessEqual(sum(d['amount_cents'] for d in rows),t['plan']['opening_cash_cents'])
            self.assertTrue(w.snapshot()['completed'])
            if case=='none':self.assertEqual(t['cumulative_exports_cents'],0)
            else:self.assertGreater(t['cumulative_exports_cents'],0)

    def test_export_quantity_enters_funded_demand_forecast(self):
        w=World()
        for _ in range(10):w.step()
        for key in ('alltag','werkstatt'):
            n=w.nodes[key];r=n['company']['result']
            self.assertEqual(r['funded_orders_units'],n['metrics']['sold_units']+n['metrics']['unmet_units'])
            self.assertTrue(any(d['seller']==key for d in w.foreign.deliveries))

    def test_invalid_order_configuration_rejected(self):
        for orders in ({'alltag':-1,'werkstatt':2},{'alltag':True,'werkstatt':2},{'alltag':6}):
            with self.assertRaises(ValueError):World(export_orders_units=orders)
