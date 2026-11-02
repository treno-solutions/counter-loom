"""Independent conservation, boundaries, real stepping and integration checks."""
import json
import unittest
from world import World, world_request, WORLDS

class WorldTests(unittest.TestCase):
    def test_independent_ledger_reconstruction_across_120_phases(self):
        w=World(); accounts=dict(w.initial); last=0
        for phase in range(120):
            if phase==15:w.queue('demand')
            if phase==36:w.queue('energy')
            w.step()
            for tx in w.journal[last:]:
                amount=tx['amount_cents']
                self.assertGreater(amount,0)
                self.assertEqual(accounts[tx['source']],tx['source_before'])
                self.assertEqual(accounts[tx['target']],tx['target_before'])
                accounts[tx['source']]-=amount; accounts[tx['target']]+=amount
                self.assertEqual(accounts[tx['source']],tx['source_after'])
                self.assertEqual(accounts[tx['target']],tx['target_after'])
            last=len(w.journal)
            self.assertEqual(accounts,{k:n['cash_cents'] for k,n in w.nodes.items()})
            self.assertEqual(sum(accounts.values()),15600000)
            self.assertGreaterEqual(min(accounts.values()),0)
            self.assertTrue(all(w.nodes[f]['inventory']>=0 for f in ['alltag','werkstatt']))
        self.assertEqual(len(w.history),24)
        self.assertEqual(w.nodes['bank']['loan_assets'],2400000)

    def test_first_real_step_pays_counterparty_then_next_phase_taxes(self):
        w=World(); self.assertEqual(w.month,0);self.assertEqual(w.journal,[])
        w.step();self.assertEqual((w.month,w.phase),(1,0))
        self.assertEqual(w.nodes['h1']['cash_cents'],540000)
        self.assertEqual(w.nodes['h1']['metrics']['income'],240000)
        self.assertEqual(w.nodes['alltag']['cash_cents'],2400000-480000-36000-2000)
        w.step();self.assertEqual(w.nodes['h1']['cash_cents'],468000)
        self.assertEqual(w.nodes['h1']['metrics']['tax'],72000)
        self.assertTrue(any(t['source']=='h1' and t['target']=='staat' and t['amount_cents']==72000 for t in w.journal))

    def test_isolated_household_with_explicit_test_input(self):
        w=World();w.phase=0
        # Test connection into a single household; not an extra income source in the world.
        w.pay('staat','h1',100000,'test_input','Testanschluss')
        w.nodes['h1']['metrics']['income']=100000
        before=w.nodes['staat']['cash_cents'];w.phase=1;w.act('h1')
        self.assertEqual(w.nodes['h1']['metrics']['tax'],30000)
        self.assertEqual(w.nodes['staat']['cash_cents'],before+30000)

    def test_insufficient_funds_create_obligation_not_money(self):
        w=World();available=w.nodes['alltag']['cash_cents'];total=sum(n['cash_cents'] for n in w.nodes.values())
        paid=w.pay('alltag','h1',available+100,'wage','Testlohn',True)
        self.assertEqual(paid,available);self.assertEqual(w.nodes['alltag']['cash_cents'],0)
        self.assertEqual(w.obligations[-1]['amount_cents'],100)
        self.assertEqual(sum(n['cash_cents'] for n in w.nodes.values()),total)

    def test_investment_has_delivery_and_later_capacity_effect(self):
        w=World()
        for _ in range(3):w.step()
        stock=w.nodes['werkstatt']['inventory'];cash=w.nodes['werkstatt']['cash_cents'];produced=w.nodes['alltag']['metrics']['produced_units']
        w.step()
        self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(w.nodes['werkstatt']['inventory'],stock-8)
        self.assertEqual(w.nodes['werkstatt']['cash_cents'],cash+120000)
        self.assertEqual(w.nodes['alltag']['metrics']['produced_units'],produced)
        w.step();w.step()
        self.assertEqual(w.nodes['alltag']['metrics']['produced_units'],produced+4)

    def test_pending_event_waits_until_next_month_and_feedback_differs(self):
        base,shock=World(),World()
        for _ in range(7):base.step();shock.step()
        shock.queue('demand')
        self.assertEqual(shock.propensity,95)
        for _ in range(3):base.step();shock.step()
        self.assertEqual(shock.propensity,95)
        base.step();shock.step();self.assertEqual(shock.propensity,65)
        for _ in range(49):base.step();shock.step()
        self.assertLess(shock.history[3]['consumption_cents'],base.history[3]['consumption_cents'])
        self.assertTrue(any('Stelle' in n['text'] for n in shock.notices))
        self.assertNotEqual([x['employment'] for x in base.history],[x['employment'] for x in shock.history])

    def test_reconstruction_reproducible_without_llms(self):
        first,second=World(),World()
        for i in range(40):
            if i==9:first.queue('energy');second.queue('energy')
            first.step();second.step()
        for key in ['nodes','journal','history','obligations']:
            self.assertEqual(getattr(first,key),getattr(second,key))
        self.assertEqual(first.snapshot()['audit']['llm_calls'],0)

    def test_stale_revision_does_not_double_execute(self):
        data=world_request('create',{});request={'world_id':data['world_id'],'revision':0}
        stepped=world_request('step',request)
        self.assertEqual(stepped['month'],1)
        count=stepped['audit']['transaction_count']
        with self.assertRaises(ValueError):world_request('step',request)
        self.assertEqual(WORLDS[data['world_id']].snapshot()['audit']['transaction_count'],count)
        for invalid in [None,[],{'unknown':1}]:
            with self.assertRaises(ValueError):world_request('create',invalid)

class WorldApiTests(unittest.TestCase):
    def test_http_create_step_export(self):
        from server import Handler
        from http.server import ThreadingHTTPServer
        from threading import Thread
        from urllib.request import Request,urlopen
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        def request(path,payload):
            with urlopen(Request(f'http://127.0.0.1:{server.server_port}/api/world'+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}),timeout=5) as response:
                return json.load(response)
        try:
            w=request('',{})
            w=request('/step',{'world_id':w['world_id'],'revision':w['revision']})
            self.assertEqual(w['month'],1);self.assertGreater(w['audit']['transaction_count'],0)
            export=request('/export',{'world_id':w['world_id']})
            self.assertEqual(len(export['full_journal']),w['audit']['transaction_count'])
            self.assertIn('initial_balances',export)
        finally:server.shutdown();server.server_close();thread.join(timeout=3)

class StandaloneSystemTests(unittest.TestCase):
    def test_household_inputs_outputs_without_world_or_scheduler(self):
        from systems import HouseholdInput,HouseholdSystem
        wage=HouseholdSystem.outputs(HouseholdInput(240000,0,72000,0,300000))
        self.assertEqual(wage['tax_due'],72000)
        self.assertEqual(wage['alltag_budget']+wage['werkstatt_budget'],159600)
        benefit=HouseholdSystem.outputs(HouseholdInput(0,100000,0,0,300000))
        self.assertEqual(benefit['tax_due'],0)
        self.assertEqual(benefit['alltag_budget']+benefit['werkstatt_budget'],95000)

    def test_firm_and_finance_rules_without_world(self):
        from systems import FirmInput,FirmSystem,FinanceSystem
        weak=FirmSystem.outputs(FirmInput(2,36,1,100000,500000,1,0,2400000))
        self.assertEqual(weak['production'],76)
        self.assertEqual(weak['employment_action'],'release')
        self.assertEqual(sum(FinanceSystem.dividends(4000,6)),4000)

class LongRunTests(unittest.TestCase):
    def test_240_month_boundary_and_stress_conservation(self):
        w=World();w.queue('demand');w.queue('energy')
        for _ in range(1200):w.step()
        self.assertEqual((w.month,w.phase),(240,4))
        self.assertEqual(sum(n['cash_cents'] for n in w.nodes.values()),15600000)
        self.assertGreaterEqual(min(n['cash_cents'] for n in w.nodes.values()),0)
        before=len(w.journal)
        with self.assertRaises(ValueError):w.step()
        self.assertEqual(len(w.journal),before)

    def test_actual_unemployment_transfer_not_wage_taxed(self):
        w=World();w.queue('demand');found=False
        for _ in range(100):
            w.step()
            if w.phase==1:
                recipients=[h for h in w.households() if h['metrics']['transfers']>0]
                if recipients:
                    for h in recipients:
                        self.assertEqual(h['metrics']['tax'],0)
                        self.assertEqual(h['metrics']['income'],h['metrics']['transfers'])
                    found=True;break
        self.assertTrue(found)
