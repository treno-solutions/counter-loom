"""State financing, interest basis, repayment and budget bounds."""
import unittest
from world import World

class TreasuryTests(unittest.TestCase):
    def test_buffer_shortfall_is_financed_without_debiting_bank_capital(self):
        w=World(government_initial_cash_cents=720000)
        for _ in range(5):w.step()
        f=w.treasury.snapshot(w);m=f['monthly']
        self.assertEqual(m['cash_deficit_cents'],241360)
        self.assertEqual(m['credit_cents'],241360)
        self.assertEqual(f['outstanding_cents'],241360)
        self.assertEqual(m['interest_paid_cents'],0)
        self.assertEqual(w.nodes['staat']['cash_cents'],720000)
        t=next(t for t in w.journal if t['kind']=='government_credit')
        self.assertEqual(t['source_before'],t['source_after'])
        self.assertEqual(t['deposit_delta_cents'],241360)
        self.assertEqual(t['loan_delta_cents'],241360)
        self.assertEqual(t['equity_delta_cents'],0)

    def test_interest_starts_next_month_uses_opening_debt_and_charges_once(self):
        w=World(government_initial_cash_cents=720000)
        for _ in range(5):w.step()
        debt=w.treasury.outstanding_cents
        w.step()
        self.assertEqual(w.treasury.interest_paid_cents,debt*300//120000)
        self.assertEqual(w.treasury.interest_charged_cents,603)
        before=w.snapshot();w.treasury.service(w)
        self.assertEqual(before,w.snapshot())
        while w.phase!=4:w.step()
        self.assertEqual(w.treasury.interest_charged_cents,603)
        self.assertEqual(w.nodes['bank']['cash_cents'],1000000)
        self.assertTrue(any(t['kind']=='government_interest' for t in w.journal))

    def test_interim_credit_is_not_financed_twice_after_taxes(self):
        w=World(government_reserve_months=0);w.pay('staat','h1',8000000,'fixture','Expliziter Testanschluss')
        w.step()
        self.assertEqual(w.treasury.outstanding_cents,480000)
        for _ in range(4):w.step()
        m=w.treasury.monthly(w)
        self.assertEqual(m['cash_deficit_cents'],241360)
        self.assertEqual(m['credit_cents']-m['principal_repaid_cents'],241360)
        self.assertEqual(w.treasury.outstanding_cents,241360)
        self.assertEqual(w.nodes['staat']['cash_cents'],0)

    def test_surplus_reduces_claim_and_debt_without_bank_income(self):
        w=World();w.month=1;w.phase=4;w.treasury.begin_month(w)
        w.treasury.issue(w,100000)
        w.pay('h1','staat',200000,'income_tax','Test-Steuereingang')
        equity=w.nodes['bank']['cash_cents'];income=w.banking.interest_received
        w.treasury.close(w)
        self.assertEqual(w.treasury.outstanding_cents,0)
        self.assertEqual(w.nodes['bank']['cash_cents'],equity)
        self.assertEqual(w.banking.interest_received,income)
        self.assertEqual(w.nodes['staat']['cash_cents'],8200000)
        t=next(t for t in w.journal if t['kind']=='government_principal')
        self.assertEqual(t['deposit_delta_cents'],-100000)
        self.assertEqual(t['equity_delta_cents'],0)
        w.check()

    def test_limit_binding_preserves_explicit_unfunded_interest(self):
        w=World(government_credit_limit_cents=100000)
        w.month=1;w.phase=0;w.treasury.issue(w,100000)
        w.pay('staat','h1',w.nodes['staat']['cash_cents'],'fixture','Testanschluss')
        w.month=2;w.month_open={k:n['cash_cents'] for k,n in w.nodes.items()};w.treasury.begin_month(w)
        w.treasury.service(w)
        self.assertEqual(w.treasury.outstanding_cents,100000)
        self.assertEqual(w.treasury.overdue_interest_cents,250)
        self.assertEqual(w.treasury.interest_paid_cents,0)
        self.assertEqual(w.nodes['staat']['cash_cents'],0)
        w.check()

    def test_late_tax_receipt_pays_interest_arrears_before_principal(self):
        w=World(government_credit_limit_cents=100000,government_reserve_months=0)
        w.month=1;w.treasury.issue(w,100000)
        w.pay('staat','h1',w.nodes['staat']['cash_cents'],'fixture','Testanschluss')
        w.month=2;w.phase=0;w.month_open={k:n['cash_cents'] for k,n in w.nodes.items()};w.treasury.begin_month(w);w.treasury.service(w)
        w.pay('h1','staat',10000,'income_tax','Später Test-Steuereingang')
        w.phase=4;w.treasury.close(w)
        self.assertEqual(w.treasury.overdue_interest_cents,0)
        self.assertEqual(w.treasury.interest_paid_cents,250)
        self.assertEqual(w.treasury.outstanding_cents,90250)
        w.check()

    def test_no_goods_does_not_trigger_procurement_credit(self):
        w=World();w.pay('staat','h1',8000000,'fixture','Testanschluss')
        self.assertEqual(w.buy('staat','alltag',120000,'procurement'),0)
        self.assertEqual(w.treasury.credit_created_cents,0)

    def test_close_is_idempotent_and_history_matches_cash_and_debt(self):
        w=World()
        for _ in range(120):
            w.step()
            if w.phase==4:
                m=w.treasury.monthly(w)
                self.assertEqual(m['closing_cash_cents'],m['opening_cash_cents']-m['cash_deficit_cents']+m['credit_cents']-m['principal_repaid_cents'])
                self.assertEqual(m['closing_principal_cents'],m['opening_principal_cents']+m['credit_cents']-m['principal_repaid_cents'])
        self.assertEqual(len(w.treasury.history),24)
        before=w.snapshot();w.treasury.close(w);w.treasury.service(w)
        self.assertEqual(before,w.snapshot())

    def test_zero_limit_uses_existing_cash_and_creates_no_state_money(self):
        w=World(government_credit_limit_cents=0)
        for _ in range(5):w.step()
        self.assertEqual(w.treasury.outstanding_cents,0)
        self.assertEqual(w.nodes['staat']['cash_cents'],8000000-241360)
        self.assertEqual(w.treasury.unfunded_financing_cents,0)
        self.assertEqual(w.treasury.monthly(w)['reserve_draw_cents'],241360)

    def test_invalid_contract_rejected(self):
        for kwargs in ({'government_credit_limit_cents':-1},{'government_annual_rate_bps':True}):
            with self.assertRaises(ValueError):World(**kwargs)
