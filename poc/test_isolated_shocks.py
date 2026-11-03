"""Observation neutrality, fork isolation and individual intervention timing."""
from copy import deepcopy
from unittest.mock import patch
import unittest
from world import World
from scripts import isolated_shocks as experiment


def month(w):
    for _ in range(5):w.step(False)


class IsolatedShockTests(unittest.TestCase):
    def test_observation_does_not_change_world_or_journal(self):
        plain,observed=World.stable(),World.stable()
        for _ in range(16):
            month(plain);start=len(observed.journal);month(observed)
            before=deepcopy(observed.nodes)
            experiment.record(observed,observed.journal[start:])
            self.assertEqual(observed.nodes,before)
            self.assertEqual(observed.journal,plain.journal)
            self.assertEqual(observed.history,plain.history)

    def test_policy_rate_changes_before_variable_contract_and_leaves_fixed_rate(self):
        w=World.stable();month(w)
        experiment.intervention(w,'rate',1);month(w)
        self.assertEqual((w.monetary.rate_bps,w.nodes['alltag']['loan_rate_bps'],w.nodes['werkstatt']['loan_rate_bps']),(500,200,200))
        month(w);self.assertEqual(w.nodes['alltag']['loan_rate_bps'],500)
        experiment.intervention(w,'rate',13);month(w)
        self.assertEqual((w.monetary.rate_bps,w.nodes['alltag']['loan_rate_bps']),(200,500))
        month(w);self.assertEqual(w.nodes['alltag']['loan_rate_bps'],200)

    def test_energy_cost_precedes_price_response_and_can_be_reversed(self):
        w=World.stable();month(w)
        experiment.intervention(w,'energy',1);month(w)
        self.assertEqual((w.energy_multiplier,w.nodes['alltag']['price']),(2,100))
        month(w);self.assertGreater(w.nodes['alltag']['price'],100)
        experiment.intervention(w,'energy',13);month(w)
        self.assertEqual(w.energy_multiplier,1)
        for _ in range(5):month(w)
        self.assertEqual((w.nodes['alltag']['price'],w.nodes['werkstatt']['price']),(100,150))

    def test_closure_ends_after_three_months_with_identical_preserved_contracts(self):
        base=World.stable()
        for _ in range(12):month(base)
        for case,supported in [('closure_no_support',False),('closure_support60',True)]:
            w=deepcopy(base);workers=list(w.nodes['alltag']['employees'])
            experiment.intervention(w,case,1)
            for relative in (1,2,3):
                month(w)
                self.assertTrue(w.crisis.closed(w,'alltag'))
                self.assertEqual(w.nodes['alltag']['employees'],workers)
                self.assertEqual(w.nodes['alltag']['metrics']['wages'],0)
                self.assertGreater(w.nodes['werkstatt']['metrics']['produced_units'],0)
                self.assertEqual(sum(h['metrics']['short_time'] for h in w.households())>0,supported)
            month(w);self.assertFalse(w.crisis.closed(w,'alltag'))
            self.assertGreater(w.nodes['alltag']['metrics']['produced_units'],0)
        self.assertEqual(base.month,12)

    def test_control_fork_is_neutral_and_matches_same_continuation(self):
        base=World.stable();month(base);month(base)
        reference=[None,None];plain=deepcopy(base)
        for _ in range(2):month(plain);reference.append(experiment.signature(plain))
        before=experiment.signature(base)
        with patch.object(experiment,'ANCHOR_MONTH',2),patch.object(experiment,'FOLLOWUP_MONTHS',2):
            result=experiment.simulate_branch(base,'control',reference)
        self.assertTrue(result['checks']['control_matches_archive'])
        self.assertEqual(result['checks']['phases_checked'],10)
        self.assertEqual(experiment.signature(base),before)


if __name__=='__main__':unittest.main()
