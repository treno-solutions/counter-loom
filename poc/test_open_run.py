"""Open observation horizon and repeatable external events beyond month 24."""
import unittest
from world import World

class OpenRunTests(unittest.TestCase):
    def finish(self,w):
        for _ in range(5):w.step()

    def test_default_continues_past_24_and_accepts_late_rate_and_machine_request(self):
        w=World()
        for _ in range(25):self.finish(w)
        self.assertFalse(w.snapshot()['completed'])
        self.assertIsNone(w.snapshot()['horizon_months'])
        w.monetary.queue(w,400);w.banking.request(w);self.finish(w)
        self.assertEqual(w.month,26)
        self.assertEqual(w.monetary.rate_bps,400)

    def test_energy_and_demand_can_be_reversed_and_applied_again(self):
        w=World()
        for _ in range(25):self.finish(w)
        for _ in range(2):
            w.queue('energy');w.queue('demand');self.finish(w)
            self.assertEqual((w.energy_multiplier,w.propensity),(2,65))
            w.queue('energy_recovery');w.queue('demand_recovery');self.finish(w)
            self.assertEqual((w.energy_multiplier,w.propensity),(1,95))
        self.assertEqual([e['event'] for e in w.active],['energy','demand','energy_recovery','demand_recovery']*2)

    def test_duplicate_opposing_or_already_effective_events_do_not_mutate(self):
        w=World();w.queue('energy')
        for event in ('energy','energy_recovery','demand_recovery','missing'):
            before=w.snapshot()
            with self.assertRaises(ValueError):w.queue(event)
            self.assertEqual(before,w.snapshot())

    def test_snapshot_rolls_while_export_retains_all_months(self):
        w=World()
        for _ in range(38):self.finish(w)
        view=w.snapshot();export=w.snapshot(export=True)
        self.assertEqual([h['month'] for h in view['history']],list(range(3,39)))
        self.assertEqual(len(export['all_history']),38)
        self.assertEqual(len(export['public_finance']['history']),38)
        self.assertFalse(export['completed'])

    def test_optional_bounded_horizon_still_stops_and_invalid_horizons_rejected(self):
        w=World(horizon_months=2);self.finish(w);self.finish(w)
        self.assertTrue(w.snapshot()['completed'])
        with self.assertRaises(ValueError):w.step()
        with self.assertRaises(ValueError):w.queue('energy')
        for value in (0,-1,True,1.5):
            with self.assertRaises(ValueError):World(horizon_months=value)

    def test_public_wage_arrears_are_actual_claims_not_a_reserve_target_gap(self):
        # The reference branch retains these claims; adaptive funded-work tests are separate.
        w=World(fiscal_policy='legacy',government_initial_cash_cents=0,government_credit_limit_cents=0)
        self.finish(w);m=w.treasury.monthly(w)
        self.assertEqual(m['public_wage_arrears_cents'],480000)
        self.assertEqual(m['unfunded_financing_cents'],m['reserve_target_cents']-m['closing_cash_cents'])
        self.assertEqual(m['public_wage_arrears_cents'],sum(o['amount_cents'] for o in w.obligations if o['source']=='staat' and o['kind']=='wage'))
