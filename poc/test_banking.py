"""Independent accounting of money creation, payments, interest and amortization."""
import unittest
from world import World, world_request, WORLDS

class BankingTests(unittest.TestCase):
    def issue(self):
        w=World(goods_unit_scale=1);w.banking.request(w)
        for _ in range(4):w.step()
        self.assertEqual(w.banking.loan.status,'credited')
        return w

    def test_initial_bank_balance_separates_customer_money_and_equity(self):
        w=World();b=w.banking.balance(w)
        self.assertEqual(b['customer_deposits_cents'],14600000)
        self.assertEqual(b['equity_cents'],1000000)
        self.assertEqual(b['reserves_cents'],13200000)
        self.assertEqual(b['assets_cents'],b['liabilities_and_equity_cents'])

    def test_origination_then_separate_delivery(self):
        w=self.issue();t=w.journal[-1]
        self.assertEqual(t['kind'],'machine_credit')
        self.assertEqual(t['source_before'],t['source_after'])
        self.assertEqual(t['target_after']-t['target_before'],120000)
        self.assertEqual(t['deposit_delta_cents'],120000)
        self.assertEqual(t['loan_delta_cents'],120000)
        self.assertEqual(w.nodes['alltag']['capital'],0)
        self.assertEqual(w.nodes['werkstatt']['reserved_units'],8)
        buyer=w.nodes['alltag']['cash_cents'];supplier=w.nodes['werkstatt']['cash_cents'];inventory=w.nodes['werkstatt']['inventory']
        w.step()
        payment=next(t for t in w.journal if t['kind']=='machine_purchase')
        self.assertEqual(payment['deposit_delta_cents'],0)
        self.assertEqual(payment['source_before']-payment['source_after'],120000)
        self.assertEqual(payment['target_after']-payment['target_before'],120000)
        self.assertEqual(w.nodes['werkstatt']['inventory'],inventory-8)
        self.assertEqual(w.nodes['werkstatt']['reserved_units'],0)
        self.assertEqual(w.nodes['alltag']['capital'],1)
        self.assertEqual(w.nodes['alltag']['metrics']['produced_units'],72)
        self.assertEqual(w.banking.loan.interest_paid_cents,0)

    def test_twelve_instalments_interest_39_and_no_thirteenth_payment(self):
        w=self.issue()
        while w.month<13 or w.phase<4:w.step()
        interest=[t for t in w.journal if t['kind']=='machine_interest']
        principal=[t for t in w.journal if t['kind']=='machine_principal']
        self.assertEqual([t['amount_cents'] for t in principal],[10000]*12)
        self.assertEqual([t['amount_cents'] for t in interest],list(range(600,0,-50)))
        self.assertEqual(sum(t['amount_cents'] for t in interest),3900)
        self.assertEqual(w.banking.loan.outstanding_cents,0)
        self.assertEqual(w.banking.loan.status,'repaid')
        self.assertEqual(w.banking.balance(w)['customer_deposits_cents'],14600000+w.treasury.outstanding_cents-w.bank_profit.retained)
        old=len(interest)+len(principal)
        for _ in range(5):w.step()
        self.assertEqual(len([t for t in w.journal if t['kind'] in ('machine_interest','machine_principal')]),old)

    def test_independent_reconstruction_including_bank_balance_every_posting(self):
        w=World();accounts=dict(w.initial);loans=2400000;reserves=13200000;last=0
        w.banking.request(w)
        for step in range(100):
            w.step()
            for t in w.journal[last:]:
                a=t['amount_cents'];effect=t['ledger_effect']
                self.assertEqual(accounts[t['source']],t['source_before'])
                self.assertEqual(accounts[t['target']],t['target_before'])
                if effect!='loan_creation':accounts[t['source']]-=a
                if effect!='principal_repayment':accounts[t['target']]+=a
                if effect=='loan_creation':loans+=a
                if effect=='principal_repayment':loans-=a
                deposits=sum(v for k,v in accounts.items() if k!='bank')
                self.assertEqual(reserves+loans,deposits+accounts['bank'])
                self.assertEqual(t['bank_after']['customer_deposits_cents'],deposits)
                self.assertEqual(t['bank_after']['loan_assets_cents'],loans)
                self.assertEqual(t['bank_after']['equity_cents'],accounts['bank'])
            last=len(w.journal)
            self.assertEqual(accounts,{k:n['cash_cents'] for k,n in w.nodes.items()})

    def test_no_cash_arrears_and_catchup_do_not_duplicate_debt(self):
        w=self.issue();w.step()
        # Isolated servicing port: move cash to another customer's account, not out of the world.
        w.pay('alltag','ausland',w.nodes['alltag']['cash_cents'],'fixture','Testanschluss')
        w.month=2;w.phase=0;w.banking.service(w)
        self.assertEqual(w.banking.loan.outstanding_cents,120000)
        self.assertEqual(w.banking.loan.overdue_interest_cents,600)
        self.assertEqual(w.banking.loan.overdue_principal_cents,10000)
        before=len(w.journal);w.banking.service(w);self.assertEqual(len(w.journal),before)
        w.month=3;w.banking.service(w)
        self.assertEqual(w.banking.loan.overdue_interest_cents,1200)
        self.assertEqual(w.banking.loan.overdue_principal_cents,20000)
        w.pay('ausland','alltag',30000,'fixture','Explizite Testfinanzierung')
        w.month=4;w.banking.service(w)
        self.assertEqual(w.banking.loan.interest_paid_cents,1800)
        self.assertEqual(w.banking.loan.principal_paid_cents,28200)
        self.assertEqual(w.banking.loan.outstanding_cents,91800)
        self.assertEqual(w.banking.loan.overdue_principal_cents,1800)
        self.assertEqual(w.nodes['alltag']['cash_cents'],0)
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000+w.bank_profit.retained+1800)
        w.check()

    def test_duplicate_request_and_api_revision_guard(self):
        s=world_request('create',{});payload={'world_id':s['world_id'],'revision':s['revision']}
        s=world_request('credit',payload)
        self.assertEqual(s['banking']['loan']['status'],'requested')
        with self.assertRaises(ValueError):world_request('credit',payload)
        with self.assertRaises(ValueError):world_request('credit',{'world_id':s['world_id'],'revision':s['revision']})
        self.assertEqual(WORLDS[s['world_id']].banking.created,0)

    def test_insufficient_goods_defer_without_money_creation(self):
        w=World();w.banking.request(w)
        w.nodes['werkstatt']['inventory']=0;w.phase=3;w.banking.originate(w)
        self.assertEqual(w.banking.loan.status,'requested')
        self.assertEqual(w.banking.created,0)
        self.assertEqual(w.banking.loan.outstanding_cents,0)

class PlausibilityRegressionTests(unittest.TestCase):
    def test_unfunded_public_wish_does_not_become_effective_demand(self):
        w=World(goods_unit_scale=1,government_credit_limit_cents=0);w.pay('staat','ausland',8000000,'fixture','Testanschluss')
        w.nodes['alltag']['inventory']=100
        self.assertEqual(w.buy('staat','alltag',120000,'procurement'),0)
        self.assertEqual(w.nodes['alltag']['metrics']['unmet_units'],0)
        self.assertEqual(w.nodes['alltag']['metrics']['unfunded_units'],12)

    def test_zero_cash_does_not_produce_without_paid_energy(self):
        w=World(goods_unit_scale=1);w.pay('alltag','ausland',2400000,'fixture','Testanschluss');w.phase=0;w.month=1
        w.act('alltag')
        self.assertEqual(w.nodes['alltag']['metrics']['production_plan'],72)
        self.assertEqual(w.nodes['alltag']['metrics']['produced_units'],0)
        self.assertEqual(w.nodes['alltag']['inventory'],0)
        self.assertEqual(w.nodes['alltag']['metrics']['wages'],0)
        w.check()
