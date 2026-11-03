"""Bank tax, income/equity bridge, payout timing and fiscal cash feedback."""
import unittest
from world import World


def month(w):
    for _ in range(5):w.step(False)


class BankProfitTests(unittest.TestCase):
    def test_monthly_tax_half_payout_and_quarterly_release(self):
        w=World()
        month(w);m=w.bank_profit.monthly
        self.assertEqual((m['interest_income_cents'],m['profit_tax_paid_cents'],m['after_tax_cents']),(4000,800,3200))
        self.assertEqual((m['distribution_cents'],m['retained_earnings_cents']),(1600,1600))
        self.assertEqual(w.nodes['bank']['cash_cents'],1001600)
        month(w);self.assertEqual(w.bank_profit.retained,3200)
        month(w);m=w.bank_profit.monthly
        self.assertEqual((m['regular_distribution_cents'],m['extra_distribution_cents'],m['retained_earnings_cents']),(1600,4800,0))
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000)
        count=len(w.journal);w.bank_profit.close(w);self.assertEqual(count,len(w.journal))

    def test_interest_is_profit_but_credit_and_principal_are_not(self):
        w=World();w.banking.request(w)
        for _ in range(20):month(w)
        for m in w.bank_profit.history:
            tx=[t for t in w.journal if t['month']==m['month']]
            self.assertEqual(m['profit_before_tax_cents'],sum(t['amount_cents'] for t in tx if t['target']=='bank' and t['kind'] in ('interest','machine_interest','government_interest')))
            self.assertEqual(m['profit_tax_paid_cents'],m['profit_before_tax_cents']//5)
        self.assertGreater(w.banking.repaid,0)
        self.assertEqual(w.banking.distributed,sum(t['amount_cents'] for t in w.journal if t['source']=='bank' and t['kind']=='dividend'))
        self.assertEqual(w.banking.profit_tax_paid,sum(t['amount_cents'] for t in w.journal if t['source']=='bank' and t['kind']=='profit_tax'))

    def test_cumulative_tax_rounding_and_deposit_reconciliation(self):
        w=World();w.month=1;w.phase=4
        w.pay('alltag','bank',1003,'interest','Fixture')
        w.bank_profit.close(w)
        self.assertEqual(w.bank_profit.monthly['profit_tax_paid_cents'],200)
        self.assertEqual(w.bank_profit.monthly['distribution_cents'],401)
        self.assertEqual(w.bank_profit.retained,402)
        self.assertEqual(w.banking.balance(w)['customer_deposits_cents'],w.banking.initial_deposits-402)
        w.check()

    def test_state_interest_feedback_is_taxed_once_and_retains_capital(self):
        w=World(distribution_tax_bps=5000,government_credit_limit_cents=0)
        w.month=1;w.phase=4
        w.pay('staat','ausland',w.nodes['staat']['cash_cents'],'fixture','Fixture')
        w.treasury.interest_charged_cents=10000;w.treasury.overdue_interest_cents=10000
        w.pay('alltag','bank',1000,'interest','Fixture')
        w.bank_profit.close(w);m=w.bank_profit.monthly
        self.assertGreater(w.treasury.interest_paid_cents,0)
        self.assertEqual(m['profit_before_tax_cents'],1000+w.treasury.interest_paid_cents)
        self.assertEqual(m['profit_tax_paid_cents'],m['profit_before_tax_cents']//5)
        self.assertGreaterEqual(w.nodes['bank']['cash_cents'],1000000)
        self.assertEqual(w.nodes['bank']['cash_cents']-1000000,m['retained_earnings_cents'])
        self.assertLess(len(w.journal),200)
        n=len(w.journal);w.bank_profit.close(w);self.assertEqual(n,len(w.journal));w.check()

    def test_zero_income_does_not_distribute_initial_equity(self):
        w=World();w.month=3;w.phase=4;w.bank_profit.close(w)
        self.assertEqual(w.bank_profit.monthly['distribution_cents'],0)
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000)
        with self.assertRaises(ValueError):World(bank_profit_policy='invalid')

    def test_legacy_policy_reproduces_full_untaxed_payout(self):
        w=World(bank_profit_policy='legacy');month(w)
        self.assertEqual(w.bank_profit.monthly['distribution_cents'],4000)
        self.assertEqual(w.bank_profit.monthly['profit_tax_paid_cents'],0)
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000)
