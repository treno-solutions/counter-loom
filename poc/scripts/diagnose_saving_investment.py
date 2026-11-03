"""Observe existing investment gates and reconcile cash flows; change no rules."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from world import World
from firms import staffing

REFERENCE = Path('qa/consumption-v16-comparison-2026-11-03.json')
FIRMS = ('alltag', 'werkstatt')


def investment_gate(world):
    """Detached record immediately before the existing investment decision."""
    buyer, seller = (world.nodes[k] for k in FIRMS)
    c = buyer['company']
    _, reserve = staffing(buyer, world.energy_multiplier, world.machine_due('alltag', True))
    units = 8 * world.goods_unit_scale
    cost = units * seller['price']
    checks = dict(
        open=not any(world.crisis.closed(world, k) for k in FIRMS),
        autonomous_branch=world.banking.loan.status not in ('requested', 'credited'),
        repeated_shortage=c['short_months'] >= 2,
        cooldown=world.month - c['last_investment_month'] >= 3,
        cash=buyer['cash_cents'] >= reserve + cost,
        stock=seller['inventory'] - seller.get('reserved_units', 0) >= units,
    )
    return dict(month=world.month, checks=checks, all_pass=all(checks.values()),
        shortage_months=c['short_months'], cash_cents=buyer['cash_cents'],
        reserve_cents=reserve, machine_cost_cents=cost, machine_units=units,
        supplier_free_units=seller['inventory'] - seller.get('reserved_units', 0),
        loan_status=world.banking.loan.status,
        firms=[dict(id=k, staff=len(world.nodes[k]['employees']),
            work_bps=world.nodes[k]['company']['work_bps'], capital=world.nodes[k]['capital'],
            plan=deepcopy(world.nodes[k]['company']['plan']),
            unmet_units=world.nodes[k]['metrics']['unmet_units']) for k in FIRMS])


class InvestmentTraceWorld(World):
    def __init__(self, quota=95):
        super().__init__()
        self.propensity = quota
        self.investment_gates = []

    def act(self, node_id):
        if self.phase == 3 and node_id == 'alltag':
            record = investment_gate(self)
            before = len(self.journal)
            super().act(node_id)
            record['executed_investment_cents'] = sum(t['amount_cents'] for t in self.journal[before:]
                if t['kind'] in ('investment', 'machine_purchase'))
            self.investment_gates.append(record)
        else:
            super().act(node_id)


def reconcile(world, tx):
    """Every sector cash change is explained by journal transfers, exactly."""
    sectors = {n['sector'] for n in world.nodes.values()}
    delta = {s: sum(n['cash_cents'] - world.month_open[n['id']]
        for n in world.nodes.values() if n['sector'] == s) for s in sectors}
    flows = defaultdict(int)
    for t in tx:
        source = world.nodes[t['source']]['sector']
        target = world.nodes[t['target']]['sector']
        flows[(source, target, t['kind'])] += t['amount_cents']
    explained = {s: sum(v * (int(b == s) - int(a == s))
        for (a, b, _), v in flows.items()) for s in sectors}
    # Credit creation/principal extinguish deposits, not the bank's equity cash.
    # The baseline has no firm principal payments; state credit is accounted here.
    for t in tx:
        if t['ledger_effect'] == 'loan_creation':
            explained['bank'] += t['amount_cents']
        elif t['ledger_effect'] == 'principal_repayment':
            explained['bank'] -= t['amount_cents']
    assert delta == explained, (world.month, delta, explained)
    return dict(cash_change_cents=delta,
        flows=[dict(source=a, target=b, kind=k, amount_cents=v)
            for (a, b, k), v in sorted(flows.items())])


def run(months, quota, reference):
    w = InvestmentTraceWorld(quota)
    rows = []
    for month in range(1, months + 1):
        start = len(w.journal)
        for _ in range(5):
            w.step(False)
        h, ref = w.history[-1], reference[month - 1]
        actual = dict(consumption_cents=h['consumption_cents'], employment=h['employment'],
            household_cash_cents=h['household_cash_cents'], firm_cash_cents=h['cash_by_sector']['firms'],
            government_cash_cents=h['government_cash_cents'], foreign_cash_cents=h['cash_by_sector']['external'],
            government_debt_cents=w.treasury.outstanding_cents, public_budget=w.budget.monthly(w),
            taxes_cents=w.treasury.monthly(w)['taxes_cents'], macro=w.macro.history[-1])
        for k, v in actual.items():
            assert v == ref[k], (quota, month, k)
        gate = w.investment_gates[-1]
        assert bool(gate['executed_investment_cents']) == gate['all_pass']
        tx = w.journal[start:]
        account = reconcile(w, tx)
        assert account['cash_change_cents']['households'] == ref['household_saving_cents']
        assert sum(t['amount_cents'] for t in tx if t['kind'] in ('investment', 'machine_purchase')) == ref['macro']['components']['investment_cents']
        rows.append(dict(month=month, investment_gate=gate, **account,
            planned_retention_cents=ref['planned_retention_cents'],
            household_saving_cents=ref['household_saving_cents'],
            inventory_change_cents=ref['macro']['components']['inventory_change_cents'],
            firms=[dict(id=k, cash_cents=w.nodes[k]['cash_cents'],
                staff_next=len(w.nodes[k]['employees']),
                result=deepcopy(w.nodes[k]['company']['result'])) for k in FIRMS]))
        if month % 120 == 0:
            print(quota, month, flush=True)
    return dict(consumption_percent=quota, reference_exact_monthly_match=True,
        gates_failed_counts=dict(Counter(k for r in rows for k, v in r['investment_gate']['checks'].items() if not v)),
        monthly=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--months', type=int, default=600)
    parser.add_argument('--output', default='.framework-review/saving-investment.json')
    args = parser.parse_args()
    if not 1 <= args.months <= 600:
        parser.error('Choose 1..600 months.')
    ref = json.loads(REFERENCE.read_text())
    paths = sorted(Path('poc').glob('*.py')) + [Path(__file__).relative_to(Path.cwd())]
    data = dict(model='illustrative_circular_flow_v16', months=args.months,
        rules_changed=False, reference=str(REFERENCE),
        reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        source_sha256={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        purpose='Observation only: investment gates, sector cash flows and existing company responses',
        runs=[])
    for quota, original in zip((95, 100), ref['runs']):
        assert quota == original['consumption_percent']
        data['runs'].append(run(args.months, quota, original['monthly']))
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
