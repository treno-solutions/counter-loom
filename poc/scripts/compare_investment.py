"""V20 project valuation: same-state rate shocks and a declared marginal opportunity."""
import argparse,gc,hashlib,json,sys
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World
from investment import present_value
from scripts.isolated_shocks import record,signature,MODEL_FILES

REFERENCE=Path('qa/bank-profit-v19-comparison.json')
SOURCES=(*MODEL_FILES,'poc/bank_profit.py','poc/investment.py','poc/scripts/compare_investment.py')


def metadata():
    return dict(date='2026-11-03',model='illustrative_circular_flow_v20',
        source_sha256={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in SOURCES},
        reference=str(REFERENCE),reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        assumptions=dict(rate_from_bps=200,rate_to_bps=500,duration_months=12,followup_months=60,
            appraisal_months=24,profit_tax_bps=2000,search_first_marginal_project_months=600),experiments=[])


def month(w):
    for _ in range(5):w.step(False)


def branch(base,policy,shock,old=None):
    w=deepcopy(base);w.investment_policy=policy;anchor=w.month
    initial=signature(base);cursor=len(w.journal);start=cursor
    accounts={k:n['cash_cents'] for k,n in w.nodes.items()};rows=[];assessments=[]
    for relative in range(1,61):
        if shock and relative in (1,13):w.monetary.queue(w,500 if relative==1 else 200)
        mstart=len(w.journal)
        for _ in range(5):
            w.step(False)
            for t in w.journal[cursor:]:
                assert accounts[t['source']]==t['source_before'] and accounts[t['target']]==t['target_before']
                if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                assert accounts[t['source']]==t['source_after'] and accounts[t['target']]==t['target_after']
            cursor=len(w.journal)
            assert accounts=={k:n['cash_cents'] for k,n in w.nodes.items()}
        row=record(w,w.journal[mstart:])
        if old:assert row==old['monthly'][relative-1],(relative,'v19 replay')
        row['relative_month']=relative
        row['investment_paid_cents']=sum(t['amount_cents'] for t in w.journal[mstart:] if t['kind'] in ('investment','machine_purchase'))
        rows.append(row);assessments.append(deepcopy(w.capital_orders.assessment))
    assert signature(base)==initial
    fields=('id','month','phase','source','target','amount_cents','kind','source_before','source_after','target_before','target_after','ledger_effect','deposit_delta_cents','loan_delta_cents','equity_delta_cents')
    return dict(case='rate' if shock else 'control',policy=policy,initial=initial,monthly=rows,assessments=assessments,
        transactions=[{k:t[k] for k in fields} for t in w.journal[start:]],
        checks=dict(phases_checked=300,ledger_reconstructed=True,parent_unchanged=True,archive_exact=bool(old)))


def late(output):
    data=metadata();old=json.loads(REFERENCE.read_text())['experiments'][1]
    base=World.stable(investment_policy='orders')
    for n in range(1,1441):
        month(base)
        if n%240==0:print('old warmup',n,flush=True)
    assert signature(base)==old['anchor']
    oldruns={r['case']:r for r in old['runs']};runs=[]
    for policy in ('orders','valuation'):
        for shock in (False,True):
            runs.append(branch(base,policy,shock,oldruns['rate' if shock else 'control'] if policy=='orders' else None))
            print('same-state',policy,shock,'complete',flush=True)
    data['experiments'].append(dict(name='same_late_state',anchor=signature(base),runs=runs))
    data['checks']=dict(warmup_phases_checked=7200,branch_phases_checked=1200,v19_anchor_and_both_branches_exact=True)
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def new_reference(output):
    data=metadata();base=World.stable();selection=None;late_history=[]
    for n in range(1,1441):
        previous=deepcopy(base) if selection is None and n<=600 else None
        month(base)
        if previous is not None:
            a=base.capital_orders.assessment
            high=present_value([(0,-a['machine_cost_cents'])]+[(m,0 if m<=a['lead_months'] else a['monthly_after_tax_cents']) for m in range(1,25+a['lead_months'])],500)
            if a['decision']=='invest' and a['cash_npv_cents']>0 and high<=0:
                selection=dict(month=n,control_assessment=deepcopy(a),same_cashflows_cash_npv_at_5_percent_cents=high,
                    criterion='First actually financeable positive cash NPV at 2%, non-positive at 5%, within first 600 control months')
                runs=[branch(previous,'valuation',shock) for shock in (False,True)]
                data['experiments'].append(dict(name='active_marginal_project',anchor=signature(previous),selection=selection,runs=runs))
                output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
                print('first marginal opportunity',n,a['cash_npv_cents'],high,flush=True)
        if n>1320:late_history.append(dict(signature(base),assessment=deepcopy(base.capital_orders.assessment)))
        if n%240==0:print('new warmup',n,flush=True)
    data['marginal_opportunity_found']=selection is not None
    data['late_reference_history']=late_history
    runs=[branch(base,'valuation',shock) for shock in (False,True)]
    data['experiments'].append(dict(name='mature_valuation',anchor=signature(base),runs=runs))
    data['checks']=dict(warmup_phases_checked=7200,branch_phases_checked=300*sum(len(e['runs']) for e in data['experiments']),
        first_marginal_opportunity_selected_before_shock_branches=True)
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('new reference complete',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--part',choices=('late','new'),required=True);p.add_argument('--output',required=True);a=p.parse_args()
    (late if a.part=='late' else new_reference)(Path(a.output))
