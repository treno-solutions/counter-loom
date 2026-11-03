"""Funded machine orders, produced and reserved before simultaneous settlement."""
from copy import deepcopy
from investment import appraise


class CapitalOrders:
    def __init__(self):
        self.orders=[]
        self.assessment=None
        self.assessments=[]

    @property
    def pending(self):
        return next((o for o in self.orders if o['delivery_month'] is None),None)

    def locked(self,node_id):
        p=self.pending
        return p['amount_cents'] if p and p['buyer']==node_id else 0

    def review(self,world):
        buyer=world.nodes['alltag'];seller=world.nodes['werkstatt'];c=buyer['company']
        cost=8*world.goods_unit_scale*seller['price']
        lead=0 if seller['inventory']-seller['reserved_units']>=8*world.goods_unit_scale else 1
        a=appraise(buyer,cost,world.energy_multiplier,world.monetary.rate_bps,world.monetary.machine_offer(),lead)
        _,reserve=world.company_staffing(buyer,world.machine_due('alltag',True))
        if self.pending:reason='pending'
        elif any(world.crisis.closed(world,k) for k in ('alltag','werkstatt')):reason='closed'
        elif not buyer['employees']:reason='no_staff'
        elif c['status']!='operating':reason='inactive'
        elif not a['demand_units']:reason='no_demand'
        elif world.month-c['last_investment_month']<3:reason='cooldown'
        elif a['cash_npv_cents']<=0:reason='unprofitable'
        elif buyer['cash_cents']<reserve+cost:reason='no_cash'
        else:reason='invest'
        credit_ready=(reason not in ('pending','closed','no_staff','inactive','no_demand','cooldown') and world.banking.loan.status in ('available','requested') and world.nodes['bank']['cash_cents']>0
            and buyer['cash_cents']>=reserve+a['first_debt_service_cents'])
        if reason=='no_cash' and credit_ready and a['loan_npv_cents']>0:reason='seek_credit'
        a.update(month=world.month,buyer='alltag',supplier='werkstatt',decision=reason,
            operating_reserve_cents=reserve,available_cash_cents=buyer['cash_cents'],cash_required_cents=reserve+cost,
            credit_available=credit_ready,credit_profitable=a['loan_npv_cents']>0)
        self.assessment=a
        if self.assessments and self.assessments[-1]['month']==world.month:self.assessments[-1]=deepcopy(a)
        else:self.assessments.append(deepcopy(a))
        return a

    def place_if_needed(self,world):
        if self.pending:return
        buyer=world.nodes['alltag'];seller=world.nodes['werkstatt'];c=buyer['company']
        if world.investment_policy=='valuation':
            a=self.assessment if self.assessment and self.assessment['month']==world.month else self.review(world)
            if a['decision']=='seek_credit':
                world.banking.loan.status='requested'
                world.banking.loan.message='Wirtschaftliche Investition: Kreditprüfung für den Maschinenkauf vorgemerkt.'
                world.notice(world.banking.loan.message,'alltag')
                return
            if a['decision']!='invest':return
        elif c['short_months']<2 or world.month-c['last_investment_month']<3:return
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
        return dict(pending=deepcopy(self.pending),history=deepcopy(self.orders),locked_cash_cents=self.locked('alltag'),assessment=deepcopy(self.assessment),assessment_history=deepcopy(self.assessments[-36:]))
