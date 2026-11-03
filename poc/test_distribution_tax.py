import unittest
from world import World
from distribution_tax import DistributionTax

class DistributionTaxTests(unittest.TestCase):
    def test_rate_validation(self):
        for bad in (-1,5001,True,25.5,'2500'):
            with self.assertRaises(ValueError):DistributionTax(bad)
        self.assertEqual(World().distribution_tax.rate_bps,2500)

    def test_only_actual_payment_is_taxed_and_wage_tax_is_untouched(self):
        w=World();w.month=1;w.phase=4;h=w.nodes['h1']
        amount=w.nodes['alltag']['cash_cents']+100
        gross=w.distribution_tax.pay(w,'alltag',h,amount,'company_dividend','Fixture')
        self.assertEqual(gross,2400000)
        self.assertEqual(h['metrics']['distribution_tax'],600000)
        self.assertEqual(h['metrics']['tax'],0)
        self.assertEqual(h['dividend_carry'],1800000)
        self.assertEqual(w.journal[-1]['kind'],'distribution_tax')
        self.assertEqual(w.distribution_tax.pay(w,'alltag',h,100,'company_dividend','Unfunded'),0)
        self.assertEqual(len(w.distribution_tax.receipts),1)
        w.check()

    def test_rounding_combines_sources_and_payment_splits_per_household_month(self):
        w=World();w.month=1;w.phase=4;h=w.nodes['h1']
        for source,kind in [('alltag','company_dividend'),('werkstatt','company_extra_dividend'),('bank','dividend'),('alltag','company_dividend')]:
            w.distribution_tax.pay(w,source,h,1,kind,'Cent fixture')
        self.assertEqual(h['metrics']['distribution_tax'],1)
        self.assertEqual(h['metrics']['distribution_net'],3)
        self.assertEqual(sum(r['tax_cents'] for r in w.distribution_tax.receipts),1)
        w.check()

    def test_zero_tax_keeps_gross_as_net(self):
        w=World(distribution_tax_bps=0);w.month=1;w.phase=4
        w.distribution_tax.pay(w,'alltag',w.nodes['h1'],101,'company_dividend','Fixture')
        self.assertEqual(w.nodes['h1']['dividend_carry'],101)
        self.assertFalse(any(t['kind']=='distribution_tax' for t in w.journal))

    def test_company_accounting_is_gross_and_tax_is_not_an_operating_expense(self):
        a,b=World(distribution_tax_bps=0),World()
        for _ in range(5):a.step(False);b.step(False)
        for f in ('alltag','werkstatt'):
            self.assertEqual(a.nodes[f]['company']['profit_allocation'],b.nodes[f]['company']['profit_allocation'])
            self.assertEqual(a.nodes[f]['cash_cents'],b.nodes[f]['cash_cents'])
        m=b.distribution_tax.monthly(b)
        self.assertEqual(b.nodes['staat']['cash_cents']-a.nodes['staat']['cash_cents'],m['tax_cents'])
        self.assertEqual(sum(a.nodes[h['id']]['cash_cents']-h['cash_cents'] for h in b.households()),m['tax_cents'])

    def test_net_carry_used_once_in_next_purchase_and_monthly_tax_resets(self):
        w=World()
        for _ in range(15):w.step(False)
        carries={h['id']:h['dividend_carry'] for h in w.households()}
        self.assertGreater(w.distribution_tax.monthly(w)['tax_cents'],0)
        for _ in range(3):w.step(False)
        for h in w.household_month:self.assertEqual(h['prior_dividend_cents'],carries[h['id']])
        for h in w.households():
            self.assertEqual(h['dividend_carry'],0)
            self.assertEqual(h['metrics']['distribution_tax'],0)

    def test_fiscal_history_and_review_include_all_withholding(self):
        w=World()
        for _ in range(20):w.step(False)
        for g,b,t in zip(w.treasury.history,w.budget.history,w.distribution_tax.history):
            tx=[r for r in w.journal if r['month']==g['month'] and r['target']=='staat']
            self.assertEqual(g['taxes_cents'],sum(r['amount_cents'] for r in tx if r['kind'] in ('income_tax','arrears_income_tax','profit_tax','distribution_tax')))
            self.assertEqual(b['recurring_taxes_cents'],g['taxes_cents'])
            self.assertEqual(t['tax_cents'],sum(r['amount_cents'] for r in tx if r['kind']=='distribution_tax'))
            self.assertEqual(g['closing_cash_cents'],w.history[g['month']-1]['government_cash_cents'])

    def test_overdue_interest_cash_feedback_terminates_and_preserves_capital(self):
        w=World(distribution_tax_bps=5000,government_credit_limit_cents=0)
        w.month=1;w.phase=4
        w.pay('staat','ausland',w.nodes['staat']['cash_cents'],'fixture','Fixture')
        w.treasury.interest_charged_cents=10000;w.treasury.overdue_interest_cents=10000
        paid=w.pay('alltag','bank',1000,'interest','Fixture interest');w.nodes['bank']['metrics']['interest']+=paid
        w.distribution_tax.settle_bank(w)
        self.assertGreater(w.treasury.interest_paid_cents,0)
        self.assertLess(w.treasury.interest_paid_cents,1000)
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000+w.bank_profit.retained)
        self.assertLess(len(w.distribution_tax.receipts),100)
        self.assertEqual(sum(t['amount_cents'] for t in w.journal if t['kind']=='dividend'),w.bank_profit.monthly['after_tax_cents']//2)
        self.assertEqual(w.bank_profit.monthly['profit_before_tax_cents'],1000+w.treasury.interest_paid_cents)
        w.check()
        count=len(w.journal);w.distribution_tax.settle_bank(w);self.assertEqual(len(w.journal),count)

    def test_export_receipts_match_journal_and_totals_under_crisis(self):
        w=World();w.crisis.queue(w,'both',3,6000)
        for _ in range(60):w.step(False)
        e=w.snapshot(export=True);tx={t['id']:t for t in e['full_journal']}
        for r in e['all_distribution_receipts']:
            self.assertEqual(tx[r['gross_transaction_id']]['amount_cents'],r['gross_cents'])
            if r['tax_cents']:self.assertEqual(tx[r['tax_transaction_id']]['amount_cents'],r['tax_cents'])
            self.assertEqual(r['gross_cents'],r['tax_cents']+r['net_cents'])
        self.assertEqual(sum(r['tax_cents'] for r in e['all_distribution_history']),sum(t['amount_cents'] for t in e['full_journal'] if t['kind']=='distribution_tax'))
