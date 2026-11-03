"""Predeclared stability screens and isolated controls; retain unsuccessful runs."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

CASES={
    'stable':dict(months=1800,parameters={}),
    'joint_only':dict(months=600,parameters=dict(workforce_policy='joint'),historical=True),
    'quarter_only':dict(months=600,parameters=dict(workforce_policy='joint',fiscal_policy='quarterly'),historical=True),
    'orders_income95':dict(months=600,parameters=dict(workforce_policy='joint',fiscal_policy='quarterly',investment_policy='orders'),historical=True),
    'income95':dict(months=600,parameters=dict(consumption_policy='income')),
    'funding_only':dict(months=600,parameters=dict(fiscal_policy='funding_only')),
    'reserve1':dict(months=600,parameters=dict(liquidity_reserve_months=1)),
    'reserve6':dict(months=600,parameters=dict(liquidity_reserve_months=6)),
    'adjust6':dict(months=600,parameters=dict(liquidity_adjustment_months=6)),
    'adjust24':dict(months=600,parameters=dict(liquidity_adjustment_months=24)),
    'fiscal6':dict(months=600,parameters=dict(fiscal_horizon_months=6)),
    'fiscal24':dict(months=600,parameters=dict(fiscal_horizon_months=24)),
    'initial_distribution':dict(months=1800,parameters={},perturbation=True),
    'shocks':dict(months=600,parameters={},shocks=True),
}


def summary(rows):
    end=rows[-1]['month']
    windows=[]
    for stop in (end-240,end):
        if stop<240:continue
        first=rows[stop-241] if stop>240 else None
        last=rows[stop-1]
        if first is None:continue
        drift={k:(last['stocks_cents'][k]-first['stocks_cents'][k])/240 for k in last['stocks_cents']}
        period=rows[stop-240:stop]
        windows.append(dict(first_month=stop-239,last_month=stop,drift_cents_per_month=drift,
            mean_consumption_cents=sum(r['consumption_cents'] for r in period)/240,
            mean_private_fte_bps=sum(r['private_fte_bps'] for r in period)/240,
            production_positive=all(r['production_units']>0 for r in period),
            mean_funding_gap_cents=sum(r['funding_gap_cents'] for r in period)/240,
            mean_social_unfunded_cents=sum(r['social_unfunded_cents'] for r in period)/240,
            mean_basic_purchase_gap_cents=sum(r['basic_purchase_gap_cents'] for r in period)/240,
            real_inventory_drift_units_per_month={k:(last['inventory_units'][k]-first['inventory_units'][k])/240 for k in last['inventory_units']}))
    checks=[abs(v)<=100 for w in windows for v in w['drift_cents_per_month'].values()]
    active=all(w['production_positive'] and w['mean_consumption_cents']>0 for w in windows)
    supplied=all(w['mean_funding_gap_cents']==0 and w['mean_social_unfunded_cents']==0 and w['mean_basic_purchase_gap_cents']==0 for w in windows)
    real_ok=all(abs(v)<=1 for w in windows for v in w['real_inventory_drift_units_per_month'].values())
    return dict(windows=windows,nominal_drift_screen=bool(checks) and all(checks),activity_screen=active,supply_financing_screen=supplied,real_inventory_screen=real_ok,stationary_reference_screen=bool(checks) and all(checks) and active and supplied and real_ok,
        note='A 600-month screen alone does not establish long-horizon stationarity. Technical tolerance 100 cents/month, declared before evaluation; failed runs retained.')


def run(case,output):
    config=CASES[case]
    w=(World if config.get('historical') else World.stable)(**config['parameters'])
    if config.get('perturbation'):w.pay('h1','h2',30000,'initial_redistribution','Declared initial redistribution')
    parameters=w.snapshot()['parameters']
    files=[Path('poc')/n for n in ('world.py','firms.py','workforce.py','systems.py','public_budget.py','treasury.py','capital_orders.py','banking.py','foreign.py','rates.py','pricing.py','profit_distribution.py','distribution_tax.py','macro.py','crisis.py')]+[Path(__file__).resolve().relative_to(Path.cwd())]
    data=dict(model='illustrative_circular_flow_v18',case=case,months=config['months'],configuration=config,
        parameters=parameters,initial_balances=w.initial,initial_transactions=w.journal.copy(),
        criteria=dict(window_months=240,nominal_drift_tolerance_cents_per_month=100,activity_required=True,holdout_after_month=600,real_inventory_drift_tolerance_parts_per_month=1),
        source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},monthly=[])
    account={k:n['cash_cents'] for k,n in w.nodes.items()};last_tx=len(w.journal)
    for month in range(1,config['months']+1):
        if config.get('shocks'):
            if month==120:w.queue('energy')
            if month==144:w.queue('energy_recovery')
            if month==180:w.monetary.queue(w,500)
            if month==216:w.monetary.queue(w,200)
            if month==240:w.crisis.queue(w,'both',3,6000)
        for _ in range(5):
            w.step(False)
            for t in w.journal[last_tx:]:
                assert account[t['source']]==t['source_before'] and account[t['target']]==t['target_before']
                if t['ledger_effect']!='loan_creation':account[t['source']]-=t['amount_cents']
                if t['ledger_effect']!='principal_repayment':account[t['target']]+=t['amount_cents']
                assert account[t['source']]==t['source_after'] and account[t['target']]==t['target_after']
            assert account=={k:n['cash_cents'] for k,n in w.nodes.items()}
            last_tx=len(w.journal)
        h=w.history[-1];cash=h['cash_by_sector'];target=6*w.essential_budget_cents*w.liquidity_reserve_months
        stocks=dict(households=cash['households'],firms=cash['firms'],government=cash['government'],external=cash['external'],bank=cash['bank'],government_debt=w.treasury.outstanding_cents,
            government_net=cash['government']-w.treasury.outstanding_cents,household_target_gap=cash['households']-target)
        data['monthly'].append(dict(month=month,stocks_cents=stocks,household_target_cents=target,
            household_cash_cents={n['id']:n['cash_cents'] for n in w.households()},consumption_cents=h['consumption_cents'],
            funding_gap_cents=sum(p['funding_gap_cents'] for p in h['households']),basic_purchase_gap_cents=sum(max(0,w.essential_budget_cents-p['paid_cents']) for p in h['households']),stock_gap_cents=sum(p['stock_gap_cents'] for p in h['households']),
            social_unfunded_cents=w.budget.monthly(w)['social_unfunded_cents'],employment=h['employment'],public_staff=w.budget.plan['approved_staff'],
            private_fte_bps=w.macro.history[-1]['private_fte_bps'],production_units=sum(w.nodes[k]['metrics']['produced_units'] for k in ('alltag','werkstatt')),
            inventory_units={k:w.nodes[k]['inventory'] for k in ('alltag','werkstatt')},capital={k:w.nodes[k]['capital'] for k in ('alltag','werkstatt')},
            gdp_proxy_cents=w.macro.history[-1]['gdp_proxy_cents'],budget=w.budget.monthly(w),fiscal_review=w.budget.review_snapshot(w),
            investment_cents=w.macro.history[-1]['components']['investment_cents'],pending_order=w.capital_orders.snapshot()['pending'],
            staffing=[dict(firm_id=d['firm_id'],from_staff=d['current_staff'],to_staff=d['selected_staff'],fte_bps=d['selected_fte_bps']) for d in w.workforce_history[-2:]]))
        if month%120==0:print(case,month,stocks,flush=True)
    data['summary']=summary(data['monthly'])
    data['checks']=dict(all_phases_checked=True,independent_journal_reconstruction=True,phases=config['months']*5,transactions=len(w.journal))
    data['capital_orders']=w.capital_orders.snapshot()
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(case,'COMPLETE',data['summary'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=CASES,required=True);p.add_argument('--output')
    a=p.parse_args();run(a.case,a.output or f'qa/stability-v18/{a.case}.json')
