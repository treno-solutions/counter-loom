"""Joint headcount/hours planning with incumbent retention and funded transitions."""
from firms import demand_units,full_capacity,outlook,MIN_WORK_BPS,WORK_STEP_BPS,MAX_BRIDGE_MONTHS

def ceildiv(a,b):return (a+b-1)//b

def requirements(firm):
    demand=demand_units(firm['company']);target=ceildiv(demand,4)
    free=max(0,firm['inventory']-firm.get('reserved_units',0))
    order=firm['company'].get('order_units',0)
    return dict(demand_units=demand,target_inventory_units=target,free_inventory_units=free,order_units=order,required_units=max(0,demand+target-free)+order)

def options(firm,energy_multiplier,debt_service=0,available_worker=False,policy='joint'):
    c=firm['company'];current=len(firm['employees']);old_fte=current*c['work_bps'];step=max(1,current)*WORK_STEP_BPS
    need=requirements(firm)['required_units'];rows=[]
    for staff in range(1,5):
        raw=ceildiv(need*10000,max(1,full_capacity(firm,staff)))
        target=max(MIN_WORK_BPS,min(10000,raw))
        if policy=='joint' and current:
            low=max(staff*MIN_WORK_BPS,max(0,old_fte-step));high=min(staff*10000,old_fte+step)
            transition_ok=low<=high
            work=ceildiv(max(low,min(high,staff*target)),staff) if transition_ok else target
            work=max(MIN_WORK_BPS,min(10000,work))
        elif policy=='legacy':
            transition_ok=True
            work=max(MIN_WORK_BPS,min(c['work_bps']+WORK_STEP_BPS,max(c['work_bps']-WORK_STEP_BPS,target)))
        else:transition_ok=True;work=target
        o=outlook(firm,energy_multiplier,staff,work,debt_service)
        reset=c['profitable_months']>=2 and firm['cash_cents']>=o['reserve_cents']
        room=c['loss_budget_cents'] if reset else max(0,c['loss_budget_cents']-c['loss_used_cents'])
        bridge=c['bridge_months']<MAX_BRIDGE_MONTHS and o['projected_gap_cents']<=room
        rows.append(dict(staff=staff,raw_work_bps=raw,target_work_bps=target,work_bps=work,fte_bps=staff*work,
            transition_ok=transition_ok,worker_available=staff<=current or available_worker,
            cash_ok=firm['cash_cents']>=o['required_cash_cents'],reserve_ok=firm['cash_cents']>=o['reserve_cents'],margin_or_bridge_ok=o['projected_gap_cents']==0 or bridge,**o))
    return rows

def choose(firm,energy_multiplier,debt_service=0,available_worker=False):
    c=firm['company'];staff=len(firm['employees']);assert staff>0
    rows=options(firm,energy_multiplier,debt_service,available_worker)
    current=next(o for o in rows if o['staff']==staff)
    direction=1 if current['raw_work_bps']>10000 and staff<4 else -1 if current['raw_work_bps']<MIN_WORK_BPS and staff>1 else 0
    desired=staff+direction;old=c['staff_signal']
    signal=old+direction if direction and old*direction>0 else direction
    selected=current;reason='Bestehende Verträge bleiben: Arbeitszeit deckt den gemeinsamen Absatz- und Lagerplan innerhalb der Bandbreite.'
    if direction:
        reason='Vertragsänderung wartet auf zwei gleichgerichtete Abschlüsse; zunächst wird der gesamte Arbeitsumfang angepasst.'
        if abs(signal)>=2:
            trial=next(o for o in rows if o['staff']==desired)
            funded=trial['reserve_ok'] if direction>0 else trial['cash_ok']
            if trial['transition_ok'] and trial['worker_available'] and funded and trial['margin_or_bridge_ok']:
                selected=trial;signal=0
                reason='Bestätigter Kapazitätsengpass: finanzierte zusätzliche Arbeitskraft; Arbeitsumfang wird auf die neue Kopfzahl verteilt.' if direction>0 else 'Bestätigter Bedarf unter Mindestarbeitszeit: eine Stelle entfällt; der gemeinsame Arbeitsumfang bleibt innerhalb der Anpassungsgrenze.'
            else:reason='Bestätigter Vertragsbedarf, aber Übergangsgrenze, freie Arbeitskraft oder Finanzierung erlaubt die Änderung noch nicht.'
    return dict(desired_staff=desired,signal=signal,selected=selected,options=rows,reason=reason,**requirements(firm))
