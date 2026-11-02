"""Bounded, illustrative energy-cost pass-through; no general price equilibrium."""
from copy import deepcopy

BASE_PRICES={'alltag':10000,'werkstatt':15000}
BASE_ENERGY={'alltag':500,'werkstatt':900}
BASKET={'alltag':33,'werkstatt':18}  # 55/45 expenditure weights at starting prices.

class Pricing:
    def __init__(self,world,pass_through_bps=5000):
        if type(pass_through_bps) is not int or not 0<=pass_through_bps<=10000:
            raise ValueError('Cost pass-through must be 0..10000 whole basis points.')
        self.last_begin_month=0
        self.pass_through_bps=pass_through_bps
        self.monthly_limit_bps=100
        self.previous_energy=dict(BASE_ENERGY)
        self.quotes={key:dict(previous_price_cents=price,target_price_cents=price,reference_energy_unit_cents=BASE_ENERGY[key]) for key,price in BASE_PRICES.items()}

    def begin_month(self,world):
        if self.last_begin_month==world.month:return
        self.last_begin_month=world.month
        for key,base in BASE_PRICES.items():
            firm=world.nodes[key];previous=firm['price'];reference=self.previous_energy[key]
            target=base+(reference-BASE_ENERGY[key])*self.pass_through_bps//10000
            limit=max(1,previous*self.monthly_limit_bps//10000)
            firm['price']=max(previous-limit,min(previous+limit,target))
            self.quotes[key]=dict(previous_price_cents=previous,target_price_cents=target,reference_energy_unit_cents=reference)
            if previous!=firm['price']:
                world.notice(f'{firm["name"]}: Stückpreis {previous/100:.2f} € → {firm["price"]/100:.2f} € nach der Energiekostenregel.',key)
            self.previous_energy[key]=BASE_ENERGY[key]*world.energy_multiplier

    def market(self,world):
        cost=sum(units*world.nodes[key]['price'] for key,units in BASKET.items())
        base=sum(units*BASE_PRICES[key] for key,units in BASKET.items())
        firms=[]
        for key,price in BASE_PRICES.items():
            n=world.nodes[key];m=n['metrics'];c=n['company'];r=c['result'];p=c['plan']
            firms.append(dict(id=key,unit_price_cents=n['price'],base_price_cents=price,
                base_energy_unit_cents=BASE_ENERGY[key],energy_unit_cents=BASE_ENERGY[key]*world.energy_multiplier,
                **deepcopy(self.quotes[key]),produced_units=m['produced_units'],sold_units=m['sold_units'],sales_cents=m['sales'],
                profit_before_tax_cents=r.get('profit_before_tax_cents',m['sales']-m['cost_of_sales']-m['idle_cost']-m['unpaid_wages']-m['interest_expense']),
                staff=p.get('staff',len(n['employees'])),next_staff=len(n['employees']),desired_staff=r.get('desired_staff',len(n['employees'])),
                staff_reason=r.get('staff_reason','Personalprüfung beim Monatsabschluss.')))
        return dict(basket_cost_cents=cost,base_basket_cost_cents=base,price_index_bps=cost*10000//base,
            purchasing_power_bps=base*10000//cost,firms=firms)

    def snapshot(self,world):
        return dict(pass_through_bps=self.pass_through_bps,monthly_limit_bps=self.monthly_limit_bps,lag_months=1,market=self.market(world))
