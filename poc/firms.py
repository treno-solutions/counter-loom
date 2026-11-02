"""Illustrative firm planning, independent of the scheduler and cash ledger.
Units are indivisible goods, monetary values integer cents. COMPANY_MODEL.md.
"""
from math import ceil

WAGE = 240000

def initial_company(forecast):
    return dict(forecast_milli=forecast*1000, inventory_value_cents=0,
                staff_signal=0, short_months=0, last_investment_month=0,
                plan={}, result={})

def demand_units(company):
    return (company['forecast_milli']+500)//1000

def plan(firm, energy_multiplier, debt_service=0):
    demand=demand_units(firm['company'])
    target=ceil(demand/4)
    opening=firm['inventory']-firm.get('reserved_units',0)
    capacity=len(firm['employees'])*firm['productivity']+(firm['capital']*4 if firm['employees'] else 0)
    needed=max(0,demand+target-opening)
    energy_unit=(500 if firm['id']=='alltag' else 900)*energy_multiplier
    wages=len(firm['employees'])*WAGE
    interest=firm['loan']*firm['loan_rate_bps']//120000
    funded=max(0,firm['cash_cents']-wages-interest-debt_service)//energy_unit
    return dict(demand_units=demand,target_units=target,opening_units=firm['inventory'],
                opening_value_cents=firm['company']['inventory_value_cents'],capacity_units=capacity,
                needed_units=needed,production_units=min(needed,capacity),funded_units=min(needed,capacity,funded),
                energy_unit_cents=energy_unit,wages_due_cents=wages,interest_due_cents=interest,
                debt_service_cents=debt_service,staff=len(firm['employees']))

def staffing(firm, energy_multiplier, debt_service=0):
    demand=demand_units(firm['company'])
    energy=(500 if firm['id']=='alltag' else 900)*energy_multiplier
    needed=ceil(max(0,demand-firm['capital']*4)/firm['productivity'])
    affordable=max(0,demand*(firm['price']-energy)-firm['loan']*firm['loan_next_rate_bps']//120000-debt_service)//WAGE
    desired=min(4,needed,affordable)
    # Two future wage rounds, expected energy and debt service retained as working cash.
    reserve=2*max(desired,len(firm['employees']))*WAGE+demand*energy+firm['loan']*firm['loan_next_rate_bps']//120000+debt_service
    return desired,reserve

def forecast(company, funded_orders):
    company['forecast_milli']=(3*company['forecast_milli']+funded_orders*1000)//4
