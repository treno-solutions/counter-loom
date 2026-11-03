"""Reproduce both archived income profiles; compare economic fields exactly."""
import hashlib,json,sys
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World


def run(quota,reference):
    w=World();w.propensity=quota
    for month in range(1,601):
        for _ in range(5):w.step(False)
        h=w.history[-1];g=w.treasury.monthly(w)
        actual=dict(month=month,household_cash_cents=h['household_cash_cents'],firm_cash_cents=h['cash_by_sector']['firms'],government_cash_cents=h['government_cash_cents'],foreign_cash_cents=h['cash_by_sector']['external'],government_debt_cents=w.treasury.outstanding_cents,consumption_cents=h['consumption_cents'],employment=h['employment'],public_budget=w.budget.monthly(w),taxes_cents=g['taxes_cents'],cash_balance_cents=g['budget_balance_cents'],macro=w.macro.history[-1],purchase_totals={k:sum(p[k] for p in h['households']) for k in ('desired_cents','paid_cents','stock_gap_cents','unit_remainder_cents','funding_gap_cents')},planned_retention_cents=sum(p['income_cents']-p['tax_cents']+p['prior_dividend_cents']-p['desired_cents'] for p in h['households']),household_saving_cents=sum(n['cash_cents']-w.month_open[n['id']] for n in w.households()))
        expected=deepcopy(reference[month-1])
        # The public rule explanation was shortened; all economic fields,
        # classifications, quantities, rates, decisions and dates must match.
        del actual['public_budget']['decision_reason'];del expected['public_budget']['decision_reason']
        assert actual==expected,(quota,month)
        if month%120==0:print(quota,month,flush=True)


if __name__=='__main__':
    source=Path('qa/consumption-v16-comparison-2026-11-03.json');ref=json.loads(source.read_text())
    result=dict(model='illustrative_circular_flow_v18',behavior='Historical v16 policies, new v18 serializer',months_each=600,
        reference=str(source),reference_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        excluded_fields=['public_budget.decision_reason (descriptive wording only)'],runs=[])
    for quota,old in zip((95,100),ref['runs']):
        run(quota,old['monthly'])
        result['runs'].append(dict(consumption_percent=quota,all_600_months_exact=True,scope='All archived economic fields; descriptive rule wording excluded',fields=list(old['monthly'][0])))
    files=sorted(p for p in Path('poc').glob('*.py') if not p.name.startswith('test_'))+[Path(__file__).resolve().relative_to(Path.cwd())]
    result['source_sha256']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    Path('qa/stability-v18-historical-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Both archived economic profiles reproduced exactly.',flush=True)
