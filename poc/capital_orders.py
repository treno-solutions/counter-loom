"""Funded machine orders, produced and reserved before simultaneous settlement."""
from copy import deepcopy


class CapitalOrders:
    def __init__(self):
        self.orders=[]

    @property
    def pending(self):
        return next((o for o in self.orders if o['delivery_month'] is None),None)

    def locked(self,node_id):
        p=self.pending
        return p['amount_cents'] if p and p['buyer']==node_id else 0

    def place_if_needed(self,world):
        if self.pending:return
        buyer=world.nodes['alltag'];seller=world.nodes['werkstatt'];c=buyer['company']
        if c['short_months']<2 or world.month-c['last_investment_month']<3:return
        _,reserve=world.company_staffing(buyer,world.machine_due('alltag',True))
        units=8*world.goods_unit_scale;price=seller['price'];cost=units*price
        if buyer['cash_cents']<reserve+cost or not buyer['employees']:return
        p=dict(id=len(self.orders)+1,buyer='alltag',seller='werkstatt',units=units,
            unit_price_cents=price,amount_cents=cost,placed_month=world.month,
            reserved_units=0,delivery_month=None,transaction_id=None)
        self.orders.append(p);seller['company']['order_units']=units;seller['company']['order_price_cents']=price
        self.reserve(world)
        world.notice('Maschinenauftrag finanziert: Werkstatt plant fehlende Teile; Ware und Kaufbetrag sind für die Lieferung gebunden.','alltag')

    def reserve(self,world):
        p=self.pending
        if not p:return
        seller=world.nodes[p['seller']]
        take=min(p['units']-p['reserved_units'],seller['inventory']-seller['reserved_units'])
        p['reserved_units']+=take;seller['reserved_units']+=take
        seller['company']['order_reserved_units']+=take
        seller['company']['order_units']=p['units']-p['reserved_units']

    def deliver(self,world):
        p=self.pending
        if not p or p['reserved_units']!=p['units']:return
        if any(world.crisis.closed(world,k) for k in ('alltag','werkstatt')):return
        buyer=world.nodes[p['buyer']];seller=world.nodes[p['seller']]
        if buyer['cash_cents']<p['amount_cents']:return
        seller['reserved_units']-=p['units'];seller['company']['order_reserved_units']-=p['units']
        units=world.buy(p['buyer'],p['seller'],p['amount_cents'],'investment',unit_price_cents=p['unit_price_cents'])
        assert units==p['units']
        buyer['capital']+=1;buyer['metrics']['investment']+=p['amount_cents']
        buyer['company']['last_investment_month']=world.month
        p['delivery_month']=world.month;p['transaction_id']=world.journal[-1]['id']
        seller['company']['order_price_cents']=0
        world.notice('Maschinenauftrag bezahlt und geliefert. Zusätzliche Kapazität erst ab dem Folgemonat.','alltag')

    def check(self,world):
        assert sum(o['delivery_month'] is None for o in self.orders)<=1
        for o in self.orders:
            assert 0<=o['reserved_units']<=o['units']
            assert o['amount_cents']==o['units']*o['unit_price_cents']
        p=self.pending;c=world.nodes['werkstatt']['company']
        assert c['order_units']==(p['units']-p['reserved_units'] if p else 0)
        assert c['order_reserved_units']==(p['reserved_units'] if p else 0)
        assert world.nodes['werkstatt']['reserved_units']>=c['order_reserved_units']
        if p:assert world.nodes[p['buyer']]['cash_cents']>=p['amount_cents']

    def snapshot(self):
        return dict(pending=deepcopy(self.pending),history=deepcopy(self.orders),locked_cash_cents=self.locked('alltag'))
