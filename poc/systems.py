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
    essential_budget: int = 100000
    consumption_policy: str = 'income'
    opening_cash: int = 0
    reserve_months: int = 3
    adjustment_months: int = 12

class HouseholdSystem:
    @staticmethod
    def outputs(data: HouseholdInput):
        income_budget=max(0,data.wage_income+data.transfer_income-data.paid_tax+data.prior_dividend)*data.consumption_percent//100
        if data.consumption_policy == 'liquidity_target':
            target=data.essential_budget*data.reserve_months
            disposable=max(0,data.wage_income+data.transfer_income-data.paid_tax+data.prior_dividend)
            income_budget=disposable*data.consumption_percent//100+(data.opening_cash-target)//data.adjustment_months
        elif data.consumption_policy != 'income':
            raise ValueError('Unknown household consumption policy.')
        desired=max(data.essential_budget,income_budget)
        budget=min(data.cash,desired)
        return {'tax_due': data.wage_income*30//100, 'alltag_budget':budget*55//100, 'werkstatt_budget':budget-budget*55//100, 'desired_budget':desired, 'funded_budget':budget}

class GovernmentSystem:
    wage_per_job=240000
    transfer_per_unemployed=100000
    procurement_per_firm=120000

class FinanceSystem:
    @staticmethod
    def dividends(received_interest, households):
        return [received_interest//households+(1 if i<received_interest%households else 0) for i in range(households)]
