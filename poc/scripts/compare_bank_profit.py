"""Same rate shock and state: archived bank rule versus consistent taxed profit."""
from copy import deepcopy
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World
from bank_profit import BankProfit
from scripts.isolated_shocks import signature,record,intervention,MODEL_FILES

OUTPUT=Path('qa/bank-profit-v19-comparison.json')
REFERENCE=Path('qa/isolated-shocks-v18-2026-11-03.json')


def advance(w):
    for _ in range(5):w.step(False)


def warmup(policy,reference=None):
    w=World.stable(bank_profit_policy=policy)
    old=json.loads(Path('qa/stability-v18/stable.json').read_text())['monthly'] if reference else None
    for month in range(1,1441):
        advance(w)
        if old:
            for k,v in signature(w).items():assert old[month-1][k]==v,(month,k)
        if month%240==0:print('warmup',policy,month,flush=True)
    return w


def branch(base,policy,shock,old=None):
    w=deepcopy(base)
    if w.bank_profit.policy!=policy:w.bank_profit=BankProfit(w,policy)
    start=len(w.journal);rows=[];profits=[];accounts={k:n['cash_cents'] for k,n in w.nodes.items()};cursor=start
    for relative in range(1,61):
        intervention(w,'rate' if shock else 'control',relative)
        month_start=len(w.journal)
        for _ in range(5):
            w.step(False)
            for t in w.journal[cursor:]:
                assert accounts[t['source']]==t['source_before'] and accounts[t['target']]==t['target_before']
                if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                assert accounts[t['source']]==t['source_after'] and accounts[t['target']]==t['target_after']
            cursor=len(w.journal)
            assert accounts=={k:n['cash_cents'] for k,n in w.nodes.items()}
        row=record(w,w.journal[month_start:]);rows.append(row);profits.append(deepcopy(w.bank_profit.monthly))
        if old:assert row==old['monthly'][relative-1],relative
    fields=('id','month','phase','source','target','amount_cents','kind','source_before','source_after','target_before','target_after','ledger_effect','deposit_delta_cents','loan_delta_cents','equity_delta_cents')
    ledger=[{k:t[k] for k in fields} for t in w.journal[start:]]
    return dict(case='rate' if shock else 'control',policy=policy,initial=signature(base),monthly=rows,bank_profit=profits,transactions=ledger,
        checks=dict(phases_checked=300,ledger_reconstructed=True,archive_exact=bool(old)))


def run():
    old=json.loads(REFERENCE.read_text());oldruns={r['case']:r for r in old['runs']}
    source=(*MODEL_FILES,'poc/bank_profit.py','poc/scripts/compare_bank_profit.py')
    data=dict(date='2026-11-03',model='illustrative_circular_flow_v19',
        source_sha256={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in source},
        reference=str(REFERENCE),reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        assumptions=dict(anchor_month=1440,followup_months=60,rate_from_bps=200,rate_to_bps=500,duration_months=12,
            profit_tax_bps=2000,monthly_payout_bps=5000,quarterly_surplus=True,capital_floor_cents=1000000,
            bank_operating_costs_modelled=False,investment_rules_changed=False),experiments=[])
    base=warmup('legacy',True)
    assert signature(base)==old['anchor']
    common=signature(base);runs=[]
    for policy in ('legacy','consistent'):
        for shock in (False,True):
            runs.append(branch(base,policy,shock,oldruns['rate' if shock else 'control'] if policy=='legacy' else None))
            assert signature(base)==common
            print('same-state',policy,shock,'complete',flush=True)
    data['experiments'].append(dict(name='same_state_policy_change',anchor=common,runs=runs))
    OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    base=warmup('consistent');common=signature(base)
    runs=[branch(base,'consistent',shock) for shock in (False,True)]
    data['experiments'].append(dict(name='mature_consistent_rule',anchor=common,runs=runs))
    data['checks']=dict(legacy_warmup_matches_1440_archived_months=True,legacy_branches_match_archive=True,
        warmup_phases_checked=14400,branch_phases_checked=1800,common_parents_unchanged=True)
    OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('All six branches complete',flush=True)


if __name__=='__main__':run()
