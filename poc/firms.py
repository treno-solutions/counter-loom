"""Illustrative firm rules: hours, liquidity bridge, mothballing and restart.
Whole goods, integer cents and work shares in basis points. COMPANY_MODEL.md.
"""
from math import ceil
from profit_distribution import initial_allocation

WAGE = 240000
MIN_WORK_BPS = 2500
WORK_STEP_BPS = 2500
MAX_BRIDGE_MONTHS = 3
RESTART_CLOSES = 2

def initial_company(forecast):
    return dict(order_units=0,order_reserved_units=0,order_price_cents=0,workforce_decision=None,forecast_milli=forecast*1000, inventory_value_cents=0,
                staff_signal=0, short_months=0, last_investment_month=0,
                status='operating',next_status='operating',work_bps=10000,next_work_bps=10000,
                bridge_months=0,loss_used_cents=0,loss_budget_cents=480000,profitable_months=0,restart_signal=0,
                retained_earnings_cents=0,cumulative_after_tax_cents=0,cumulative_regular_cents=0,cumulative_extra_cents=0,
                profit_allocation=initial_allocation(),plan={}, result={})

def demand_units(company):
    return (company['forecast_milli']+500)//1000

def full_capacity(firm,staff):
    return staff*firm['productivity']+firm['capital']*4*firm.get('unit_scale',1) if staff else 0

def outlook(firm,energy_multiplier,staff,work_bps,debt_service=0):
    demand=demand_units(firm['company']);target=ceil(demand/4)
    free=max(0,firm['inventory']-firm.get('reserved_units',0))
    capacity=full_capacity(firm,staff)*work_bps//10000
    order=firm['company'].get('order_units',0)
    units=min(max(0,demand+target-free)+order,capacity)
    energy=(500 if firm['id']=='alltag' else 900)//firm.get('unit_scale',1)*energy_multiplier
    wages=staff*(WAGE*work_bps//10000)
    interest=firm['loan']*firm['loan_next_rate_bps']//120000
    reserved=min(order,units)
    order_receipts=(order+firm['company'].get('order_reserved_units',0))*firm['company'].get('order_price_cents',firm['price']) if order and units>=order else 0
    receipts=min(demand,free+units-reserved)*firm['price']+order_receipts
    outflows=wages+units*energy+interest+debt_service
    return dict(production_units=units,capacity_units=capacity,wages_cents=wages,
                expected_receipts_cents=receipts,required_cash_cents=outflows,
                projected_gap_cents=max(0,outflows-receipts),
                reserve_cents=2*wages+units*energy+interest+debt_service)

def work_target(firm,staff):
    demand=demand_units(firm['company']);free=max(0,firm['inventory']-firm.get('reserved_units',0))
    needed=max(0,demand+ceil(demand/4)-free)+firm['company'].get('order_units',0)
    return max(MIN_WORK_BPS,min(10000,ceil(needed*10000/max(1,full_capacity(firm,staff)))))

def staffing(firm,energy_multiplier,debt_service=0):
    demand=demand_units(firm['company'])
    # Technical need is separate from the ability to finance a whole wage.
    needed=max(1,ceil(max(0,demand-firm['capital']*4*firm.get('unit_scale',1))/firm['productivity'])) if demand else 0
    desired=min(4,needed)
    staff=max(1,desired,len(firm['employees']))
    work=max(work_target(firm,staff),firm['company']['next_work_bps'])
    return desired,outlook(firm,energy_multiplier,staff,work,debt_service)['reserve_cents']

def plan(firm,energy_multiplier,debt_service=0):
    demand=demand_units(firm['company']);target=ceil(demand/4)
    opening=firm['inventory']-firm.get('reserved_units',0)
    work=firm['company']['work_bps'];staff=len(firm['employees'])
    capacity=full_capacity(firm,staff)*work//10000
    needed=max(0,demand+target-opening)+firm['company'].get('order_units',0)
    energy=(500 if firm['id']=='alltag' else 900)//firm.get('unit_scale',1)*energy_multiplier
    per_worker=WAGE*work//10000;wages=staff*per_worker
    interest=firm['loan']*firm['loan_rate_bps']//120000
    funded=max(0,firm['cash_cents']-wages-interest-debt_service)//energy
    return dict(demand_units=demand,target_units=target,opening_units=firm['inventory'],
                opening_value_cents=firm['company']['inventory_value_cents'],capacity_units=capacity,
                needed_units=needed,production_units=min(needed,capacity),funded_units=min(needed,capacity,funded),
                energy_unit_cents=energy,wages_due_cents=wages,interest_due_cents=interest,
                debt_service_cents=debt_service,staff=staff,work_bps=work,wage_per_worker_cents=per_worker,
                status=firm['company']['status'])

def forecast(company,funded_orders):
    company['forecast_milli']=(3*company['forecast_milli']+funded_orders*1000)//4
