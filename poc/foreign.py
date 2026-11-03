"""Bounded foreign buyer: real goods for existing deposits, FOREIGN_MODEL.md."""
from copy import deepcopy

FIRMS = ('alltag', 'werkstatt')

class ForeignTrade:
    def __init__(self, export_orders_units=None):
        self.orders = dict(export_orders_units if export_orders_units is not None else {'alltag':6,'werkstatt':2})
        if set(self.orders)!=set(FIRMS) or any(type(v) is not int or v<0 for v in self.orders.values()):
            raise ValueError('Foreign orders must be nonnegative whole units for both firms.')
        self.deliveries=[]
        self.plan=self.empty_plan()
        self.last_purchase_month=0

    def empty_plan(self):
        return dict(month=0,opening_cash_cents=0,desired_cents=0,budget_cents=0,
                    orders=[dict(seller=k,desired_units=v,desired_cents=0,allocated_cents=0,funded_units=0) for k,v in self.orders.items()])

    def begin_month(self,world):
        opening=world.nodes['ausland']['cash_cents']
        desired={key:self.orders[key]*world.nodes[key]['price'] for key in FIRMS}
        total=sum(desired.values());budget=min(opening,total)
        # Allocate the envelope before current-month energy receipts. Whole-unit
        # rounding leaves money on the foreign account; no forced spending.
        allocations={FIRMS[0]:budget*desired[FIRMS[0]]//total if total else 0}
        allocations[FIRMS[1]]=budget-allocations[FIRMS[0]]
        self.plan=dict(month=world.month,opening_cash_cents=opening,desired_cents=total,budget_cents=budget,
            orders=[dict(seller=k,desired_units=self.orders[k],desired_cents=desired[k],allocated_cents=allocations[k],
                         funded_units=min(self.orders[k],allocations[k]//world.nodes[k]['price'])) for k in FIRMS])

    def purchase(self,world):
        if self.plan['month']!=world.month or self.last_purchase_month==world.month:return
        self.last_purchase_month=world.month
        # Domestic purchases have already been settled; export orders see the
        # remaining free stock and cannot take a reserved machine.
        for order in self.plan['orders']:
            world.buy('ausland',order['seller'],order['desired_cents'],'export_sale',spending_limit=order['allocated_cents'])
        rows=[d for d in self.deliveries if d['month']==world.month]
        amount=sum(d['amount_cents'] for d in rows)
        units=sum(d['units'] for d in rows)
        if units:
            world.notice(f'Ausland kauft {units} Wareneinheiten für {amount/100:.2f} €: bezahlt und aus den Firmenlagern geliefert.','ausland')
        elif self.plan['desired_cents']:
            world.notice('Auslandsbestellung ohne Lieferung: Anfangsguthaben, verfügbare Ware oder eine betriebliche Verkaufssperre begrenzt den Kauf. Kein Geldrückfluss.','ausland')

    def delivery(self,world,seller,units,amount,cost,stock_before,transaction_id):
        self.deliveries.append(dict(transaction_id=transaction_id,month=world.month,phase=world.phase,
            seller=seller,buyer='ausland',units=units,unit_price_cents=world.nodes[seller]['price'],amount_cents=amount,
            cost_cents=cost,inventory_before=stock_before,inventory_after=world.nodes[seller]['inventory']))

    def snapshot(self,world):
        imports=sum(t['amount_cents'] for t in world.journal if t['kind'] in ('energy','closure_cost'))
        exports=sum(d['amount_cents'] for d in self.deliveries)
        current=[d for d in self.deliveries if d['month']==world.month]
        month_imports=sum(t['amount_cents'] for t in world.journal if t['kind'] in ('energy','closure_cost') and t['month']==world.month)
        month_exports=sum(d['amount_cents'] for d in current)
        return dict(plan=deepcopy(self.plan),deliveries=deepcopy(self.deliveries),
            month_imports_cents=month_imports,month_exports_cents=month_exports,
            cumulative_imports_cents=imports,cumulative_exports_cents=exports,
            net_inflow_cents=month_exports-month_imports,cumulative_net_inflow_cents=exports-imports,
            domestic_cash_cents=sum(n['cash_cents'] for n in world.nodes.values() if n['sector'] not in ('external','bank')),
            foreign_cash_cents=world.nodes['ausland']['cash_cents'])

    def check(self,world):
        imports=sum(t['amount_cents'] for t in world.journal if t['kind'] in ('energy','closure_cost'))
        exports=sum(d['amount_cents'] for d in self.deliveries)
        # Fixture/test-port transfers remain explicit so controlled unit tests
        # can wire this system without pretending those flows are trade.
        other=sum(t['amount_cents']*((1 if t['target']=='ausland' else 0)-(1 if t['source']=='ausland' else 0))
                  for t in world.journal if t['kind'] not in ('energy','closure_cost','export_sale'))
        assert world.nodes['ausland']['cash_cents']==world.initial['ausland']+imports-exports+other
        tx={t['id']:t for t in world.journal if t['kind']=='export_sale'}
        assert len(tx)==len(self.deliveries)
        for d in self.deliveries:
            t=tx[d['transaction_id']]
            assert t['source']=='ausland' and t['target']==d['seller']
            assert t['amount_cents']==d['amount_cents']==d['units']*d['unit_price_cents']
            assert t['deposit_delta_cents']==t['loan_delta_cents']==t['equity_delta_cents']==0
            assert d['inventory_before']-d['inventory_after']==d['units']
        if self.plan['month']==world.month:
            paid=sum(d['amount_cents'] for d in self.deliveries if d['month']==world.month)
            assert paid<=self.plan['budget_cents']<=self.plan['opening_cash_cents']
