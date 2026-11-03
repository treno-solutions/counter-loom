"""Read-only national-account proxies; measured flows never change agent decisions."""
from copy import deepcopy
from pricing import BASE_PRICES

def change_bps(value,base):
    return round((value/base-1)*10000) if base>0 else None

class MacroAccounts:
    def __init__(self):
        self.history=[]
        self.opening_inventory_cents=0

    def begin_month(self,world):
        self.opening_inventory_cents=sum(world.nodes[k]['company']['inventory_value_cents'] for k in ('alltag','werkstatt'))

    def close(self,world):
        assert not self.history or self.history[-1]['month']<world.month
        tx=[t for t in world.journal if t['month']==world.month]
        amount=lambda kinds:sum(t['amount_cents'] for t in tx if t['kind'] in kinds)
        # State procurement is a final goods purchase. Public work is separately
        # approximated by actual current payroll, not by transfers or financing.
        components=dict(consumption_cents=amount(('consumption',)),public_goods_cents=amount(('procurement',)),
            investment_cents=amount(('investment','machine_purchase')),exports_cents=amount(('export_sale',)),
            imports_cents=amount(('energy','closure_cost')),inventory_change_cents=sum(world.nodes[k]['company']['inventory_value_cents'] for k in ('alltag','werkstatt'))-self.opening_inventory_cents,
            public_services_cents=sum(t['amount_cents'] for t in tx if t['source']=='staat' and t['kind']=='wage'))
        gdp=components['consumption_cents']+components['public_goods_cents']+components['investment_cents']+components['exports_cents']-components['imports_cents']+components['inventory_change_cents']+components['public_services_cents']
        firms=[world.nodes[k] for k in ('alltag','werkstatt')]
        fte_bps=sum(n['company']['plan']['staff']*n['company']['plan']['work_bps'] for n in firms)
        output=sum(n['metrics']['produced_units']*(BASE_PRICES[n['id']]//world.goods_unit_scale) for n in firms)
        employed=sum(n['company']['plan']['staff'] for n in firms)+len(world.nodes['staat']['employees'])
        price_index=world.pricing.market(world)['price_index_bps']
        prev=self.history[-1] if self.history else None
        year=next((r for r in reversed(self.history) if r['month']==world.month-12),None)
        first_output=self.history[0]['goods_output_base_cents'] if self.history else output
        row=dict(month=world.month,gdp_proxy_cents=gdp,components=components,
            nominal_growth_mom_bps=change_bps(gdp,prev['gdp_proxy_cents']) if prev else None,
            nominal_growth_yoy_bps=change_bps(gdp,year['gdp_proxy_cents']) if year else None,
            policy_rate_bps=world.monetary.rate_bps,price_index_bps=price_index,
            inflation_yoy_bps=change_bps(price_index,year['price_index_bps']) if year else None,
            goods_output_base_cents=output,goods_output_index_bps=round(output/first_output*10000) if first_output else None,
            private_fte_bps=fte_bps,goods_productivity_cents=round(output*10000/fte_bps) if fte_bps else None,
            employment_at_production=employed,unemployment_bps=round((6-employed)*10000/6),
            customer_deposits_cents=world.banking.balance(world)['customer_deposits_cents'],government_debt_cents=world.treasury.outstanding_cents)
        self.history.append(row)

    def snapshot(self):
        return dict(monthly=deepcopy(self.history[-1]) if self.history else None,history=deepcopy(self.history[-120:]),household_count=6,demography_modeled=False,birth_rate_per_1000=None)
