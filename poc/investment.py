"""Bounded investment appraisal: frozen demand, labour savings, cash and loan NPV."""
from decimal import Decimal, localcontext, ROUND_HALF_UP
from math import ceil
from firms import WAGE, MIN_WORK_BPS, demand_units, full_capacity

HORIZON_MONTHS = 24


def operating_projection(firm, energy_multiplier, extra_capital=0):
    staff=len(firm['employees']);demand=demand_units(firm['company'])
    capacity=full_capacity(firm,staff)+extra_capital*4*firm['unit_scale'] if staff else 0
    work=max(MIN_WORK_BPS,min(10000,ceil(demand*10000/max(1,capacity))))
    units=min(demand,capacity*work//10000)
    wages=staff*(WAGE*work//10000)
    energy=units*((500 if firm['id']=='alltag' else 900)//firm['unit_scale'])*energy_multiplier
    return dict(units=units,work_bps=work,wages_cents=wages,energy_cents=energy,sales_cents=units*firm['price'])


def present_value(cashflows, annual_rate_bps):
    with localcontext() as ctx:
        ctx.prec=40
        factor=Decimal(1)+Decimal(annual_rate_bps)/Decimal(120000)
        value=sum(Decimal(cents)/(factor**month) for month,cents in cashflows)
        return int(value.quantize(Decimal(1),rounding=ROUND_HALF_UP))


def value_path(cashflows,annual_rate_bps):
    with localcontext() as ctx:
        ctx.prec=40
        factor=Decimal(1)+Decimal(annual_rate_bps)/Decimal(120000)
        value=Decimal(0);path=[]
        for month,cents in cashflows:
            value+=Decimal(cents)/(factor**month)
            path.append(dict(month=month,value_cents=int(value.quantize(Decimal(1),rounding=ROUND_HALF_UP))))
        return path


def appraise(firm, machine_cost_cents, energy_multiplier, discount_rate_bps, loan_rate_bps, lead_months=0):
    before=operating_projection(firm,energy_multiplier)
    after=operating_projection(firm,energy_multiplier,1)
    sales=after['sales_cents']-before['sales_cents']
    wages=before['wages_cents']-after['wages_cents']
    energy=after['energy_cents']-before['energy_cents']
    pretax=sales+wages-energy
    # Same 20% marginal profit tax as the model firms; no depreciation deduction.
    benefit=pretax-max(0,pretax)*20//100
    cost=machine_cost_cents
    cashflows=[(0,-cost)]+[(m,0 if m<=lead_months else benefit) for m in range(1,HORIZON_MONTHS+lead_months+1)]
    cash_path=value_path(cashflows,discount_rate_bps)
    cash_npv=cash_path[-1]['value_cents']
    principal=(cost+11)//12;outstanding=cost;debt=[];loanflows=[(m,0) for m in range(lead_months+1)]
    for m in range(1,HORIZON_MONTHS+1):
        repayment=min(outstanding,principal) if m<=12 else 0
        interest=outstanding*loan_rate_bps//120000 if repayment else 0
        # Interest expense reduces taxable profit only if a positive marginal gain exists.
        tax_without=max(0,pretax)*20//100
        tax_with=max(0,pretax-interest)*20//100
        interest_after_tax=interest-(tax_without-tax_with)
        loanflows.append((m+lead_months,benefit-repayment-interest_after_tax))
        if repayment:debt.append(dict(month=m,opening_principal_cents=outstanding,interest_cents=interest,principal_cents=repayment))
        outstanding-=repayment
    return dict(horizon_months=HORIZON_MONTHS,lead_months=lead_months,discount_rate_bps=discount_rate_bps,
        loan_rate_bps=loan_rate_bps,machine_cost_cents=cost,demand_units=demand_units(firm['company']),
        before=before,after=after,additional_sales_cents=sales,wage_saving_cents=wages,
        additional_energy_cents=energy,monthly_before_tax_cents=pretax,monthly_after_tax_cents=benefit,
        cash_npv_cents=cash_npv,loan_npv_cents=present_value(loanflows,discount_rate_bps),cash_value_path=cash_path,loan_value_path=value_path(loanflows,discount_rate_bps),
        loan_interest_cents=sum(r['interest_cents'] for r in debt),loan_schedule=debt,
        first_debt_service_cents=debt[0]['principal_cents']+debt[0]['interest_cents'])
