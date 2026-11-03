"""Check observation neutrality and monetary reconciliation of the diagnosis."""
import unittest
from world import World
from scripts.diagnose_saving_investment import InvestmentTraceWorld, investment_gate, reconcile


class SavingInvestmentDiagnosisTests(unittest.TestCase):
    def test_observer_keeps_journal_and_history_identical(self):
        plain, traced = World(), InvestmentTraceWorld()
        for _ in range(45 * 5):
            plain.step(False)
            traced.step(False)
        self.assertEqual(plain.journal, traced.journal)
        self.assertEqual(plain.history, traced.history)
        self.assertEqual(len(traced.investment_gates), 45)

    def test_credit_and_repayment_are_not_bank_cash_transfers(self):
        w = World()
        w.treasury.issue(w, 10000)
        w.treasury.repay(w, 3000)
        result = reconcile(w, w.journal)
        self.assertEqual(result['cash_change_cents']['bank'], 0)
        self.assertEqual(result['cash_change_cents']['government'], 7000)

    def test_funded_machine_still_requires_shortage_and_stock(self):
        w = World()
        w.month = 4
        f = w.nodes['alltag']
        f['company']['short_months'] = 2
        before = investment_gate(w)
        self.assertTrue(before['checks']['cash'])
        self.assertFalse(before['checks']['stock'])
        w.nodes['werkstatt']['inventory'] = 8 * w.goods_unit_scale
        self.assertTrue(investment_gate(w)['all_pass'])
        f['company']['short_months'] = 0
        self.assertFalse(investment_gate(w)['all_pass'])


if __name__ == '__main__':
    unittest.main()
