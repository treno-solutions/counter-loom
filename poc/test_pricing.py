"""Price timing, real quantities, contracts and ledger consistency under energy shocks."""
import unittest
from copy import deepcopy
from world import World
from pricing import BASE_PRICES

class PricingTests(unittest.TestCase):
    def finish(self,w):
        for _ in range(5):w.step()

    def test_no_energy_change_keeps_starting_prices_and_index(self):
        w=World(goods_unit_scale=1)
        for _ in range(24):
            self.finish(w);m=w.history[-1]['market']
            self.assertEqual([f['unit_price_cents'] for f in m['firms']],[10000,15000])
            self.assertEqual((m['price_index_bps'],m['purchasing_power_bps']),(10000,10000))

    def test_lag_limit_and_partial_energy_cost_target(self):
        w=World(goods_unit_scale=1);self.finish(w);w.queue('energy');self.finish(w)
        self.assertEqual([w.nodes[k]['price'] for k in BASE_PRICES],[10000,15000])
        self.assertEqual(w.history[-1]['market']['firms'][0]['energy_unit_cents'],1000)
        for expected in ([10100,15150],[10201,15301],[10250,15450]):
            self.finish(w)
            self.assertEqual([w.nodes[k]['price'] for k in BASE_PRICES],expected)
        for _ in range(3):self.finish(w)
        self.assertEqual([w.nodes[k]['price'] for k in BASE_PRICES],[10250,15450])
        self.assertEqual(w.pricing.market(w)['price_index_bps'],10272)
        self.assertLess(w.pricing.market(w)['purchasing_power_bps'],10000)

    def test_price_change_does_not_revalue_existing_inventory_or_create_money(self):
        w=World();self.finish(w);w.queue('energy');self.finish(w)
        stock={k:(n['inventory'],n['company']['inventory_value_cents']) for k,n in w.nodes.items() if k in BASE_PRICES}
        cash={k:n['cash_cents'] for k,n in w.nodes.items()};journal=deepcopy(w.journal)
        w.month+=1;w.pricing.begin_month(w)
        self.assertEqual(cash,{k:n['cash_cents'] for k,n in w.nodes.items()})
        self.assertEqual(journal,w.journal)
        self.assertEqual(stock,{k:(w.nodes[k]['inventory'],w.nodes[k]['company']['inventory_value_cents']) for k in BASE_PRICES})

    def test_higher_prices_buy_less_with_identical_budget_and_available_stock(self):
        w=World(goods_unit_scale=1);n=w.nodes['alltag'];n['inventory']=100;n['company']['inventory_value_cents']=500000
        before=w.buy('h1','alltag',100000)
        n['price']=10250
        after=w.buy('h2','alltag',100000)
        self.assertEqual((before,after),(10,9))
        self.assertEqual(w.journal[-1]['amount_cents'],9*10250)

    def test_foreign_plan_uses_the_new_month_prices(self):
        w=World(goods_unit_scale=1);w.queue('energy');self.finish(w);w.step()
        for o in w.foreign.plan['orders']:
            self.assertEqual(o['desired_cents'],o['desired_units']*w.nodes[o['seller']]['price'])
        self.assertEqual(w.foreign.plan['desired_cents'],6*10100+2*15150)

    def test_machine_quote_locks_actual_eight_unit_cost_and_last_repayment(self):
        w=World(goods_unit_scale=1);w.nodes['werkstatt']['price']=15451
        quote=w.banking.snapshot(w)['loan'];self.assertEqual(quote['amount_cents'],8*15451)
        w.nodes['werkstatt']['inventory']=8;w.nodes['werkstatt']['company']['inventory_value_cents']=100000
        w.month=1;w.phase=3;w.banking.request(w);w.banking.originate(w)
        loan=w.banking.loan;self.assertEqual(loan.amount_cents,123608)
        self.assertEqual(loan.monthly_principal_cents,10301)
        w.phase=4;w.banking.deliver(w)
        self.assertEqual(w.journal[-1]['amount_cents'],123608)
        for month in range(2,14):
            w.month=month;w.banking.service(w)
        self.assertEqual((loan.outstanding_cents,loan.overdue_principal_cents),(0,0))
        self.assertEqual(loan.principal_paid_cents,123608)
        self.assertEqual([t['amount_cents'] for t in w.journal if t['kind']=='machine_principal'][-1],10297)

    def test_history_goods_reconcile_under_24_month_energy_shock(self):
        w=World(goods_unit_scale=1);w.queue('energy')
        for _ in range(24):
            self.finish(w);m=w.history[-1]
            for h in m['households']:
                self.assertEqual(h['paid_cents'],sum(g['paid_units']*g['unit_price_cents'] for g in h['goods']))
                self.assertEqual(h['paid_real_cents'],sum(g['paid_units']*g['base_price_cents'] for g in h['goods']))
                self.assertEqual(h['desired_real_cents'],sum(g['desired_units']*g['base_price_cents'] for g in h['goods']))
                self.assertLessEqual(h['paid_real_cents'],h['paid_cents'])
                self.assertEqual(h['desired_cents'],h['paid_cents']+h['funding_gap_cents']+h['stock_gap_cents']+h['unit_remainder_cents'])
                for g in h['goods']:self.assertEqual(g['unit_price_cents'],next(f for f in m['market']['firms'] if f['id']==g['seller'])['unit_price_cents'])
        exported=w.snapshot(export=True);exported['all_history'][0]['market']['firms'][0]['unit_price_cents']=1
        self.assertEqual(w.history[0]['market']['firms'][0]['unit_price_cents'],10000)

    def test_reference_and_price_caps_apply_to_decreases_too(self):
        w=World(goods_unit_scale=1);w.queue('energy')
        for _ in range(5):self.finish(w)
        w.energy_multiplier=1;w.month+=1;w.pricing.begin_month(w)
        self.assertEqual(w.nodes['alltag']['price'],10250)
        w.pricing.begin_month(w)
        self.assertEqual(w.nodes['alltag']['price'],10250)
        w.month+=1;w.pricing.begin_month(w)
        self.assertEqual(w.nodes['alltag']['price'],10148)

    def test_delayed_machine_delivery_keeps_original_unit_price(self):
        w=World(goods_unit_scale=1);w.nodes['werkstatt']['inventory']=8
        w.nodes['werkstatt']['company']['inventory_value_cents']=100000
        w.month=1;w.phase=3;w.banking.request(w);w.banking.originate(w)
        w.nodes['werkstatt']['price']=15450
        w.month=2;w.phase=4;w.banking.deliver(w)
        self.assertEqual(w.banking.loan.amount_cents,120000)
        self.assertEqual(w.nodes['werkstatt']['inventory'],0)
        self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(w.journal[-1]['amount_cents'],120000)
