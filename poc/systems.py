"""Pure system rules: explicit inputs -> planned outputs, without UI or global world.
Execution and counterpart settlement remain the ledger's responsibility.
All constants are illustrative assumptions documented in WORLD_MODEL.md.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class HouseholdInput:
    wage_income: int
    transfer_income: int
    paid_tax: int
    prior_dividend: int
    cash: int
    consumption_percent: int = 95

class HouseholdSystem:
    @staticmethod
    def outputs(data: HouseholdInput):
        budget=min(data.cash,max(0,data.wage_income+data.transfer_income-data.paid_tax+data.prior_dividend)*data.consumption_percent//100)
        return {'tax_due': data.wage_income*30//100, 'alltag_budget':budget*55//100, 'werkstatt_budget':budget-budget*55//100}

@dataclass(frozen=True)
class FirmInput:
    staff: int
    productivity: int
    capital: int
    sales: int
    due_costs: int
    prior_weak_months: int
    unmet_units: int
    cash: int

class FirmSystem:
    @staticmethod
    def outputs(data: FirmInput):
        weak=data.prior_weak_months+1 if data.sales*100<data.due_costs*80 else 0
        return {'production':data.staff*data.productivity+data.capital*4 if data.staff else 0,
                'weak_months':weak,
                'employment_action':'release' if weak>=2 and data.staff else 'hire' if data.unmet_units>0 and data.cash>=max(1,data.staff+1)*240000*3 else 'hold'}

class GovernmentSystem:
    wage_per_job=240000
    transfer_per_unemployed=100000
    procurement_per_firm=120000

class FinanceSystem:
    @staticmethod
    def dividends(received_interest, households):
        return [received_interest//households+(1 if i<received_interest%households else 0) for i in range(households)]
