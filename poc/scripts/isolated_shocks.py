"""Unchanged v18 economy: isolated shocks from one verified, mature state."""
import argparse
from collections import defaultdict
from copy import deepcopy
import gc
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World

ANCHOR_MONTH=1440
FOLLOWUP_MONTHS=60
CASES=('control','rate','energy','closure_no_support','closure_support60')
REFERENCE=Path('qa/stability-v18/stable.json')
MODEL_FILES=tuple('poc/'+name for name in (
    'world.py','firms.py','workforce.py','systems.py','public_budget.py','treasury.py',
    'capital_orders.py','banking.py','foreign.py','rates.py','pricing.py',
    'profit_distribution.py','distribution_tax.py','macro.py','crisis.py'))


def signature(w):
    h=w.history[-1];cash=h['cash_by_sector']
    return dict(month=w.month,stocks_cents=dict(households=cash['households'],firms=cash['firms'],
        government=cash['government'],external=cash['external'],bank=cash['bank'],
        government_debt=w.treasury.outstanding_cents,government_net=cash['government']-w.treasury.outstanding_cents,
        household_target_gap=cash['households']-6*w.essential_budget_cents*w.liquidity_reserve_months),
        household_cash_cents={n['id']:n['cash_cents'] for n in w.households()},
        consumption_cents=h['consumption_cents'],employment=h['employment'],public_staff=w.budget.plan['approved_staff'],
        private_fte_bps=w.macro.history[-1]['private_fte_bps'],
        production_units=sum(w.nodes[k]['metrics']['produced_units'] for k in ('alltag','werkstatt')),
        inventory_units={k:w.nodes[k]['inventory'] for k in ('alltag','werkstatt')},
        capital={k:w.nodes[k]['capital'] for k in ('alltag','werkstatt')},
        gdp_proxy_cents=w.macro.history[-1]['gdp_proxy_cents'],budget=w.budget.monthly(w))


def record(w,transactions):
    h=w.history[-1];flow=defaultdict(int)
    for t in transactions:
        flow[(w.nodes[t['source']]['sector'],w.nodes[t['target']]['sector'],t['kind'])]+=t['amount_cents']
    amount=lambda kind,source=None:sum(t['amount_cents'] for t in transactions if t['kind']==kind and (source is None or t['source']==source))
    households=[]
    for n in w.households():
        m=n['metrics'];p=next(p for p in h['households'] if p['id']==n['id'])
        households.append(dict(id=n['id'],cash_cents=n['cash_cents'],employer_at_purchase=p['employer'],employer_next=n['employer'],
            income_before_owner_payout_cents=m['income']-m['tax'],owner_payout_net_cents=m['distribution_net'],
            disposable_received_cents=m['income']-m['tax']+m['distribution_net'],
            wages_cents=sum(t['amount_cents'] for t in transactions if t['kind']=='wage' and t['target']==n['id']),
            transfers_cents=m['transfers'],short_time_cents=m['short_time'],
            consumption_cents=p['paid_cents'],consumption_base_price_cents=p['paid_real_cents'],
            desired_cents=p['desired_cents'],funding_gap_cents=p['funding_gap_cents'],stock_gap_cents=p['stock_gap_cents'],
            basic_purchase_gap_cents=max(0,w.essential_budget_cents-p['paid_cents']),goods=deepcopy(p['goods'])))
    firms=[]
    for key in ('alltag','werkstatt'):
        n=w.nodes[key];m=n['metrics'];c=n['company'];p=c['plan']
        assert n['inventory']==p['opening_units']+m['produced_units']-m['sold_units']
        firms.append(dict(id=key,cash_cents=n['cash_cents'],sales_cents=m['sales'],
            profit_before_tax_cents=c['result']['profit_before_tax_cents'],wages_cents=m['wages'],
            interest_paid_cents=sum(t['amount_cents'] for t in transactions if t['source']==key and t['kind'] in ('interest','machine_interest')),
            energy_paid_cents=sum(t['amount_cents'] for t in transactions if t['source']==key and t['kind'] in ('energy','closure_cost')),
            tax_cents=c['result']['tax_paid_cents'],distribution_gross_cents=c['result']['distribution_cents'],
            opening_inventory_units=p['opening_units'],produced_units=m['produced_units'],sold_units=m['sold_units'],
            inventory_units=n['inventory'],unmet_units=m['unmet_units'],unit_price_cents=n['price'],
            staff_at_production=p['staff'],staff_next=len(n['employees']),planned_fte_bps=p['staff']*p['work_bps'],
            paid_fte_bps=m['wages']*10000//240000,status=c['status'],next_status=c['next_status'],
            closed=w.crisis.closed(w,key),capital=n['capital']))
    fiscal=w.treasury.monthly(w)
    return dict(**signature(w),relative_month=w.month-ANCHOR_MONTH,households=households,firms=firms,
        consumption_base_price_cents=sum(p['paid_real_cents'] for p in h['households']),
        disposable_received_cents=sum(p['disposable_received_cents'] for p in households),
        paid_private_fte_bps=sum(p['paid_fte_bps'] for p in firms),
        policy_rate_bps=w.monetary.rate_bps,variable_rate_bps=w.nodes['alltag']['loan_rate_bps'],fixed_rate_bps=w.nodes['werkstatt']['loan_rate_bps'],
        price_index_bps=w.pricing.market(w)['price_index_bps'],energy_multiplier=w.energy_multiplier,
        government=dict(taxes_cents=fiscal['taxes_cents'],cash_balance_cents=fiscal['budget_balance_cents'],
            interest_paid_cents=fiscal['interest_paid_cents'],wages_paid_cents=amount('wage','staat'),
            transfers_paid_cents=amount('transfer','staat'),short_time_paid_cents=amount('short_time','staat'),
            procurement_paid_cents=amount('procurement','staat'),social_unfunded_cents=w.budget.monthly(w)['social_unfunded_cents'],
            interest_arrears_cents=w.treasury.overdue_interest_cents),
        flows=[dict(source=a,target=b,kind=k,amount_cents=v) for (a,b,k),v in sorted(flow.items())])


def intervention(w,case,relative_month):
    if relative_month==1:
        if case=='rate':w.monetary.queue(w,500)
        elif case=='energy':w.queue('energy')
        elif case.startswith('closure_'):w.crisis.queue(w,'alltag',3,6000 if case=='closure_support60' else 0)
    if relative_month==13:
        if case=='rate':w.monetary.queue(w,200)
        elif case=='energy':w.queue('energy_recovery')


def simulate_branch(base,case,reference):
    w=deepcopy(base);initial=signature(w)
    assert initial==signature(base)
    accounts={k:n['cash_cents'] for k,n in w.nodes.items()};start=len(w.journal);cursor=start
    rows=[]
    for relative in range(1,FOLLOWUP_MONTHS+1):
        intervention(w,case,relative)
        month_start=len(w.journal)
        for _ in range(5):
            w.step(False)
            for t in w.journal[cursor:]:
                assert accounts[t['source']]==t['source_before'] and accounts[t['target']]==t['target_before']
                if t['ledger_effect']!='loan_creation':accounts[t['source']]-=t['amount_cents']
                if t['ledger_effect']!='principal_repayment':accounts[t['target']]+=t['amount_cents']
                assert accounts[t['source']]==t['source_after'] and accounts[t['target']]==t['target_after']
            assert accounts=={k:n['cash_cents'] for k,n in w.nodes.items()}
            cursor=len(w.journal)
        if case=='control':
            for k,v in signature(w).items():assert v==reference[w.month-1][k],(w.month,k)
        rows.append(record(w,w.journal[month_start:]))
        if relative%12==0:print(case,relative,flush=True)
    fields=('id','month','phase','source','target','amount_cents','kind','source_before','source_after','target_before','target_after','ledger_effect','deposit_delta_cents','loan_delta_cents','equity_delta_cents')
    ledger=[{k:t[k] for k in fields} for t in w.journal[start:]]
    assert signature(base)==initial,'Branch mutated its common starting state'
    return dict(case=case,initial=initial,monthly=rows,transactions=ledger,
        checks=dict(phases_checked=FOLLOWUP_MONTHS*5,journal_reconstruction=True,control_matches_archive=case=='control',
            base_state_unchanged=True,transactions_checked=len(ledger)))


def run(output):
    ref=json.loads(REFERENCE.read_text());reference=ref['monthly']
    for f in MODEL_FILES:assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==ref['source_sha256'][f],f
    w=World.stable();pre=[]
    for month in range(1,ANCHOR_MONTH+1):
        start=len(w.journal)
        for _ in range(5):w.step(False)
        for k,v in signature(w).items():assert v==reference[month-1][k],(month,k)
        if month>ANCHOR_MONTH-24:pre.append(record(w,w.journal[start:]))
        if month%120==0:print('warmup',month,flush=True)
    anchor=signature(w)
    data=dict(model='illustrative_circular_flow_v18',model_rules_changed=False,
        anchor_month=ANCHOR_MONTH,shock_first_month=ANCHOR_MONTH+1,followup_months=FOLLOWUP_MONTHS,
        reference=str(REFERENCE),reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        source_sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in (*MODEL_FILES,'poc/scripts/isolated_shocks.py')},
        assumptions=dict(rate=dict(from_bps=200,to_bps=500,duration_months=12),energy=dict(multiplier=2,duration_months=12),
            closure=dict(firm='alltag',duration_months=3,replacement_bps=[0,6000])),
        anchor=anchor,anchor_sha256=hashlib.sha256(json.dumps(anchor,sort_keys=True).encode()).hexdigest(),
        checks=dict(warmup_matches_all_reference_months=True,warmup_phases_checked=ANCHOR_MONTH*5),pre_shock_monthly=pre,runs=[])
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    for case in CASES:
        data['runs'].append(simulate_branch(w,case,reference))
        out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        print(case,'COMPLETE',flush=True);gc.collect()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='qa/isolated-shocks-v18-2026-11-03.json')
    a=p.parse_args();run(a.output)
