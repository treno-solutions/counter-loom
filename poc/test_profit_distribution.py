"""Profit/cash separation, loss absorption and actual household counterpart payments."""
import unittest
from profit_distribution import allocation
from world import World

class ProfitTests(unittest.TestCase):
    def test_initial_cash_and_credit_are_not_profits(self):
        a=allocation(0,0,9000000,100000,120000,True,3,'surplus')
        self.assertEqual(a['total_paid_cents'],0)

    def test_cash_and_profit_both_limit_quarterly_distribution(self):
        a=allocation(90000,10000,180000,100000,20000,True,3,'surplus')
        self.assertEqual((a['regular_paid_cents'],a['extra_paid_cents']),(5000,55000))
        self.assertEqual(a['closing_retained_cents'],40000)
        self.assertEqual(a['cash_before_cents']-a['total_paid_cents'],a['protected_cash_cents'])
        b=allocation(90000,10000,9000000,100000,0,True,3,'surplus')
        self.assertEqual(b['total_paid_cents'],100000)

    def test_losses_remain_signed_and_must_be_recovered(self):
        a=allocation(-100000,40000,1000000,100000,0,True,3,'surplus')
        self.assertEqual(a['total_paid_cents'],0)
        self.assertEqual(a['closing_retained_cents'],-60000)
        b=allocation(-60000,100000,1000000,100000,0,True,6,'surplus')
        self.assertEqual(b['total_paid_cents'],40000)
        self.assertEqual(b['closing_retained_cents'],0)

    def test_extra_is_quarterly_and_blocks_cover_all_payments(self):
        a=allocation(90000,10000,1000000,100000,0,True,2,'surplus')
        self.assertEqual((a['regular_paid_cents'],a['extra_paid_cents']),(5000,0))
        a=allocation(90000,10000,1000000,100000,0,False,3,'surplus')
        self.assertEqual(a['total_paid_cents'],0)

    def test_legacy_keeps_original_regular_rule_even_after_prior_losses(self):
        a=allocation(-100000,40000,1000000,100000,120000,True,3,'legacy')
        self.assertEqual(a['regular_paid_cents'],20000)
        self.assertEqual(a['extra_paid_cents'],0)
        self.assertEqual(a['investment_buffer_cents'],0)

    def test_real_ledger_and_loss_pool_reconstruction_with_shocks(self):
        for case in ('baseline','energy','closure','loan'):
            w=World();earnings={f:0 for f in ('alltag','werkstatt')};paid={f:0 for f in earnings}
            if case=='closure':w.crisis.queue(w,'alltag',3,6000)
            if case=='loan':w.banking.request(w)
            if case=='energy':w.queue('energy')
            for _ in range(90):
                w.step()
                if w.phase!=4:continue
                for f in earnings:
                    c=w.nodes[f]['company'];a=c['profit_allocation'];earnings[f]+=c['result']['after_tax_cents']
                    tx=[t for t in w.journal if t['month']==w.month and t['source']==f and t['kind'] in ('company_dividend','company_extra_dividend')]
                    amount=sum(t['amount_cents'] for t in tx);paid[f]+=amount
                    self.assertEqual(amount,a['total_paid_cents'])
                    self.assertEqual(c['retained_earnings_cents'],earnings[f]-paid[f])
                    self.assertTrue(all(t['target'].startswith('h') and t['deposit_delta_cents']==0 for t in tx))
                    if amount:self.assertGreaterEqual(w.nodes[f]['cash_cents'],a['protected_cash_cents'])
                    if a['extra_paid_cents']:self.assertEqual(w.month%3,0)
                    self.assertEqual(sum(t['amount_cents'] for t in tx if t['kind']=='company_extra_dividend'),a['extra_paid_cents'])

    def test_additional_payout_enters_next_purchase_plan(self):
        w=World()
        for _ in range(15):w.step()
        extra=[t for t in w.journal if t['month']==3 and t['kind']=='company_extra_dividend']
        self.assertGreater(sum(t['amount_cents'] for t in extra),0)
        carries={h['id']:h['dividend_carry'] for h in w.households()}
        for _ in range(3):w.step()
        for h in w.household_month:self.assertEqual(h['prior_dividend_cents'],carries[h['id']])

    def test_credited_machine_amount_is_protected_in_real_closure_overlap(self):
        w=World();w.banking.request(w)
        for _ in range(4):w.step()
        self.assertEqual(w.banking.loan.status,'credited')
        # Controlled delivery port: supplier is externally closed before delivery.
        w.crisis.episodes.append(dict(firms=['werkstatt'],start_month=1,end_month=1,replacement_bps=0,workers=[]))
        w.step();a=w.nodes['alltag']['company']['profit_allocation']
        self.assertEqual(a['investment_buffer_cents'],w.banking.loan.amount_cents)
        self.assertEqual(w.banking.loan.status,'credited')

    def test_batch_advancement_is_identical_to_interactive_steps(self):
        a,b=World(),World()
        for _ in range(35):
            a.step();self.assertIsNone(b.step(emit_snapshot=False))
        left,right=a.snapshot(export=True),b.snapshot(export=True)
        left.pop('world_id');right.pop('world_id')
        self.assertEqual(left,right)

    def test_default_and_reference_policy_explicit_and_validated(self):
        self.assertEqual(World().distribution_policy,'surplus')
        self.assertEqual(World(distribution_policy='legacy').distribution_policy,'legacy')
        with self.assertRaises(ValueError):World(distribution_policy='unknown')
