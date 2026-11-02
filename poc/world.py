"""Illustrative, cent-exact circular-flow world. Rules: WORLD_MODEL.md.
BPTK schedules system agents; this ledger owns the authoritative monetary state.
"""
from copy import deepcopy
from threading import RLock
from uuid import uuid4
from BPTK_Py import Model, Agent, SimultaneousScheduler
from banking import Banking
from treasury import Treasury
from rates import MonetaryPolicy
from foreign import ForeignTrade
from firms import initial_company, plan as company_plan, staffing, forecast
from systems import HouseholdInput, HouseholdSystem, GovernmentSystem, FinanceSystem

PHASES = ['Produktion & Löhne', 'Steuern & Transfers', 'Konsum & Aufträge', 'Investitionen', 'Monatsabschluss']
RULES = {
 'households': 'Kaufplan: mindestens 1.000 € monatlicher Grundbedarf als illustrative Annahme, darüber 95 % des Nettoeinkommens (nach Konsumeingriff 65 %). Der Grundbedarfsplan kann aus vorhandenem Kontoguthaben finanziert werden. Käufe sind durch Geld, Lager und ganze Gütereinheiten begrenzt; unerfüllte Kaufpläne sind keine gebuchten Ausgaben oder Schulden.',
 'firms': 'Betriebe planen Absatz und Lagerpuffer, begrenzen Produktion durch Personal, Geld und Energie und passen Stellen erst nach zwei Monaten an. Lager wird zu Herstellungskosten bewertet. Positive Gewinne werden versteuert und bei ausreichendem Betriebspuffer teilweise an die sechs Haushaltseigentümer ausgeschüttet. Feste Preise und Löhne; illustrative Regeln.',
 'government': 'Zwei öffentliche Stellen zu je 2.400 € brutto, bis zu 1.000 € Transfer je unbeschäftigtem Haushalt und bis zu 1.200 € Beschaffung je Betrieb. Tatsächliche Kassenfehlbeträge können durch einen Staatskredit der Bank bis 50.000 € finanziert werden. Neue Kreditbeträge erhalten den Leitzins plus einen Modellaufschlag; der vereinbarte Zins bleibt je Betrag fest und fällt ab Folgemonat an. Überschüsse tilgen Schuld; nach Ausschöpfen der Kreditgrenze bleibt die endliche Kassenreserve. Kredit ist Finanzierung, keine Steuereinnahme.',
 'bank': 'Eine Bank führt die Guthaben aller Nichtbanken. Eigenkapital und Kundeneinlagen sind getrennt. Ein begrenzter Maschinenkredit von 1.200 € schafft eine Einlage und eine Kreditforderung; Tilgung baut beide ab. Zinsen sind Bankertrag. Ein begrenzter Staatskredit finanziert Kassenfehlbeträge innerhalb seines Rahmens. Tatsächlich vereinnahmte Firmen- und Staatszinsen werden am Monatsende an Haushalte ausgeschüttet.',
 'external': 'Ein vereinfachtes Auslandskonto erhält Energiezahlungen und kauft inländische Waren: monatlich bis zu sechs Alltags- und zwei Werkstatteinheiten. Nur Guthaben vom Monatsbeginn finanziert Bestellungen. Bezahlung und Lagerabgang erfolgen gemeinsam; fehlendes Geld oder Ware begrenzt den Rückfluss. Keine Wechselkurse oder vollständige Auslandswirtschaft.'
}

class SystemAgent(Agent):
    def act(self, time, round_no, step_no):
        self.model.world.act(self.properties['node_id']['value'])

class World:
    def __init__(self, essential_budget_cents=100000, export_orders_units=None, government_credit_limit_cents=5000000, government_annual_rate_bps=300, initial_policy_rate_bps=200):
        self.id = uuid4().hex[:16]
        self.revision = 0
        self.month = 0
        self.phase = -1
        self.nodes = {}
        self.journal = []
        self.obligations = []
        self.notices = []
        self.history = []
        self.pending = []
        self.active = []
        self.essential_budget_cents = essential_budget_cents
        self.energy_multiplier = 1
        self.propensity = 95
        self._node('alltag', 'Alltag & Versorgung', 'firms', 2400000, employees=['h1','h2'], price=10000, productivity=36, inventory=0, capital=0, loan=1200000, weak_months=0, reserved_units=0, machine_loan_cents=0)
        self._node('werkstatt', 'Werkstatt & Technik', 'firms', 2400000, employees=['h3','h4'], price=15000, productivity=20, inventory=0, capital=0, loan=1200000, weak_months=0, reserved_units=0, machine_loan_cents=0)
        self._node('staat', 'Staat', 'government', 8000000, employees=['h5','h6'], government_loan_cents=0)
        self._node('bank', 'Finanzsektor', 'bank', 1000000, loan_assets=2400000)
        self._node('ausland', 'Ausland', 'external', 0)
        for i in range(1,7):
            employer = 'alltag' if i<3 else 'werkstatt' if i<5 else 'staat'
            self._node(f'h{i}', f'Haushalt {i}', 'households', 300000, employer=employer, dividend_carry=0)
        for key, demand in [('alltag',60),('werkstatt',32)]:
            self.nodes[key]['company']=initial_company(demand)
        self.initial = {k:n['cash_cents'] for k,n in self.nodes.items()}
        self.initial_money = sum(self.initial.values())
        self.month_open = deepcopy(self.initial)
        self._reset_metrics()
        self.monetary = MonetaryPolicy(self,initial_policy_rate_bps)
        self.banking = Banking(self)
        self.treasury = Treasury(self,government_credit_limit_cents,government_annual_rate_bps)
        self.foreign = ForeignTrade(export_orders_units)
        self.foreign.begin_month(self)
        self.model = Model(starttime=0, stoptime=1200, dt=1, name='Counterloom circular-flow fixture', scheduler=SimultaneousScheduler())
        self.model.world = self
        self.model.register_agent_factory('system', lambda aid,model,props:SystemAgent(aid,model,props))
        # Ordering is part of the fixture, not a simultaneous market-clearing claim.
        for node_id in [k for k in self.nodes if k!='staat']+['staat']:
            self.model.create_agent('system', {'node_id':{'type':'String','value':node_id}})

    def _node(self, key, name, sector, cash, **extra):
        self.nodes[key] = dict(id=key, name=name, sector=sector, cash_cents=cash, **extra)

    def _reset_metrics(self):
        for n in self.nodes.values():
            n['metrics'] = dict(income=0, tax=0, sales=0, operating_costs=0, wages=0, interest=0, sold_units=0, unmet_units=0, produced_units=0, investment=0, transfers=0, consumption_plan=0, consumption_budget=0, consumption_paid=0, reserve_used=0, unfunded_units=0, production_plan=0, cost_of_sales=0, production_cost=0, idle_cost=0, interest_expense=0, unpaid_wages=0)

    def notice(self, text, node='world'):
        self.notices.append(dict(month=self.month, phase=self.phase, node=node, text=text))

    def pay(self, source, target, amount, kind, label, mandatory=False):
        if not isinstance(amount, int) or amount < 0 or source == target:
            raise ValueError('Invalid ledger transfer')
        if source=='staat' and kind in ('wage','transfer','procurement','government_interest'):
            self.treasury.ensure_cash(self,amount)
        sender, receiver = self.nodes[source], self.nodes[target]
        paid = min(amount, sender['cash_cents'])
        bank_before = self.banking.balance(self)
        if paid:
            before = [sender['cash_cents'], receiver['cash_cents']]
            sender['cash_cents'] -= paid
            receiver['cash_cents'] += paid
            effect = 'bank_income' if target=='bank' else 'bank_distribution' if source=='bank' else 'transfer'
            if target=='bank': self.banking.interest_received += paid
            if source=='bank': self.banking.distributed += paid
            self.record(source,target,paid,kind,label,before[0],before[1],bank_before,effect)
        if paid < amount:
            if mandatory:
                self.obligations.append(dict(month=self.month, source=source, target=target, amount_cents=amount-paid, kind=kind))
            self.notice(f'{sender["name"]}: {((amount-paid)/100):.2f} € für {label} nicht finanziert.', source)
        return paid

    def record(self,source,target,amount,kind,label,source_before,target_before,bank_before,effect):
        bank_after=self.banking.balance(self)
        self.journal.append(dict(id=len(self.journal)+1,month=self.month,phase=self.phase,source=source,target=target,amount_cents=amount,
            kind=kind,label=label,source_before=source_before,source_after=self.nodes[source]['cash_cents'],target_before=target_before,target_after=self.nodes[target]['cash_cents'],
            ledger_effect=effect,deposit_delta_cents=bank_after['customer_deposits_cents']-bank_before['customer_deposits_cents'],
            loan_delta_cents=bank_after['loan_assets_cents']-bank_before['loan_assets_cents'],equity_delta_cents=bank_after['equity_cents']-bank_before['equity_cents'],bank_before=bank_before,bank_after=bank_after))
        self.banking.check(self)

    def buy(self, buyer, seller, budget, kind='consumption', spending_limit=None):
        firm = self.nodes[seller]
        # A sale, inventory departure and both cash entries form one operation.
        desired = budget // firm['price']
        if buyer=='staat' and kind=='procurement':
            self.treasury.ensure_cash(self,min(desired,firm['inventory']-firm.get('reserved_units',0))*firm['price'])
        funded_desired = min(desired,self.nodes[buyer]['cash_cents']//firm['price'])
        if spending_limit is not None:
            funded_desired=min(funded_desired,spending_limit//firm['price'])
        units = min(funded_desired, firm['inventory']-firm.get('reserved_units',0))
        if units:
            stock_before=firm['inventory']
            paid = self.pay(buyer, seller, units*firm['price'], kind, 'Konsum' if kind=='consumption' else 'Öffentlicher Auftrag' if kind=='procurement' else 'Warenexport bezahlt' if kind=='export_sale' else 'Anlage geliefert')
            cost=firm['company']['inventory_value_cents']*units//firm['inventory']
            firm['company']['inventory_value_cents']-=cost
            firm['metrics']['cost_of_sales']+=cost
            firm['inventory'] -= units
            firm['metrics']['sales'] += paid
            firm['metrics']['sold_units'] += units
            if kind=='export_sale':
                self.foreign.delivery(self,seller,units,paid,cost,stock_before,self.journal[-1]['id'])
        firm['metrics']['unmet_units'] += max(0, funded_desired-units)
        firm['metrics']['unfunded_units'] += max(0, desired-funded_desired)
        return units

    def act(self, node_id):
        n = self.nodes[node_id]
        if self.phase == 0 and n['sector'] in ('firms', 'government'):
            if node_id=='staat':self.treasury.service(self)
            if n['sector']=='firms':
                n['company']['result']={}
                p=company_plan(n,self.energy_multiplier,self.machine_due(node_id))
                n['company']['plan']=p
                n['metrics']['production_plan']=p['production_units']
            for worker in n['employees']:
                paid=self.pay(node_id,worker,GovernmentSystem.wage_per_job,'wage','Lohn',True)
                self.nodes[worker]['metrics']['income']+=paid
                n['metrics']['wages']+=paid
                n['metrics']['operating_costs']+=paid
            if n['sector']=='firms':
                m=n['metrics'];p=n['company']['plan']
                m['unpaid_wages']=p['wages_due_cents']-m['wages']
                interest=self.pay(node_id,'bank',p['interest_due_cents'],'interest','Kreditzins',True)
                m['interest_expense']=p['interest_due_cents']
                m['operating_costs']+=interest
                self.nodes['bank']['metrics']['interest']+=interest
                if node_id=='alltag':
                    charged=self.banking.loan.interest_charged_cents
                    self.banking.service(self)
                    m['interest_expense']+=self.banking.loan.interest_charged_cents-charged
                labor_capacity=m['wages']*n['productivity']//240000
                if labor_capacity: labor_capacity+=n['capital']*4
                units=min(p['production_units'],labor_capacity,n['cash_cents']//p['energy_unit_cents'])
                energy=self.pay(node_id,'ausland',units*p['energy_unit_cents'],'energy','Energie für Produktion')
                m['operating_costs']+=energy
                m['produced_units']=units
                # Paid idle labour is an expense; productive labour is carried in stock.
                productive_wages=m['wages']*units//max(1,labor_capacity)
                m['production_cost']=productive_wages+energy
                m['idle_cost']=m['wages']-productive_wages
                n['inventory']+=units
                n['company']['inventory_value_cents']+=m['production_cost']
        elif self.phase == 1 and n['sector']=='households':
            n['metrics']['tax'] = self.pay(node_id,'staat',self.household_outputs(n)['tax_due'],'income_tax','Einkommensteuer',True)
        elif self.phase == 1 and node_id=='staat':
            for h in self.households():
                if h['employer'] is None:
                    transfer = self.pay('staat',h['id'],GovernmentSystem.transfer_per_unemployed,'transfer','Transfer')
                    h['metrics']['income'] += transfer
                    h['metrics']['transfers'] += transfer
        elif self.phase == 2 and node_id=='staat':
            for firm in ('alltag','werkstatt'):
                self.buy('staat',firm,GovernmentSystem.procurement_per_firm,'procurement')
        elif self.phase == 3 and node_id=='alltag':
            if self.banking.originate(self) or self.banking.loan.status=='credited': return
            _,reserve=staffing(n,self.energy_multiplier,self.machine_due(node_id,True))
            if n['company']['short_months']>=2 and self.month-n['company']['last_investment_month']>=3 and n['cash_cents']>=reserve+120000 and self.nodes['werkstatt']['inventory']-self.nodes['werkstatt'].get('reserved_units',0)>=8:
                self.buy('alltag','werkstatt',120000,'investment')
                n['capital']+=1
                n['metrics']['investment']+=120000
                n['company']['last_investment_month']=self.month
                self.notice('Alltag & Versorgung kauft nach anhaltendem Engpass eine Anlage: ab nächstem Monat +4 Einheiten Kapazität.',node_id)
        elif self.phase == 4 and n['sector']=='firms':
            self.close_company(n)
        elif self.phase == 4 and node_id=='bank':
            self.treasury.close(self)
            interest=n['metrics']['interest']
            for h,share in zip(self.households(),FinanceSystem.dividends(interest,6)):
                paid=self.pay('bank',h['id'],share,'dividend','Zinsausschüttung')
                h['dividend_carry'] += paid

    def household_outputs(self,n):
        return HouseholdSystem.outputs(HouseholdInput(n['metrics']['income']-n['metrics']['transfers'],n['metrics']['transfers'],n['metrics']['tax'],n['dividend_carry'],n['cash_cents'],self.propensity,self.essential_budget_cents))

    def machine_due(self,node_id,next_month=False):
        return self.banking.due(self,self.month+1 if next_month else self.month)['total_cents'] if node_id=='alltag' else 0

    def close_company(self,n):
        m=n['metrics'];c=n['company'];p=c['plan']
        orders=m['sold_units']+m['unmet_units']
        forecast(c,orders)
        c['short_months']=c['short_months']+1 if m['unmet_units']>0 else 0
        profit=m['sales']-m['cost_of_sales']-m['idle_cost']-m['unpaid_wages']-m['interest_expense']
        tax_due=max(0,profit)*20//100
        tax=self.pay(n['id'],'staat',tax_due,'profit_tax','Gewinnsteuer',True)
        desired,reserve=staffing(n,self.energy_multiplier,self.machine_due(n['id'],True))
        staff=len(n['employees']);direction=1 if desired>staff else -1 if desired<staff else 0
        old=c['staff_signal']
        c['staff_signal']=old+direction if direction and old*direction>0 else direction
        reason='Personal unverändert; Bedarf und finanzierbare Stellen werden monatlich geprüft.'
        if abs(c['staff_signal'])>=2:
            if direction<0 and staff:
                worker=n['employees'].pop();self.nodes[worker]['employer']=None
                reason='Eine Stelle entfällt nach zwei Monaten mit geringerem tragfähigem Personalbedarf.'
                c['staff_signal']=0
            elif direction>0:
                candidates=[h for h in self.households() if h['employer'] is None]
                if candidates and n['cash_cents']>=reserve:
                    worker=candidates[0];n['employees'].append(worker['id']);worker['employer']=n['id']
                    reason='Eine Stelle entsteht nach zwei Monaten Mehrbedarf und mit finanziertem Betriebspuffer.'
                    c['staff_signal']=0
                else:reason='Mehrbedarf besteht; freie Arbeitskraft oder Betriebspuffer fehlt.'
        if len(n['employees'])!=staff:self.notice(n['name']+': '+reason+' Gilt ab nächstem Monat.',n['id'])
        arrears=any(o['source']==n['id'] for o in self.obligations)
        if n['id']=='alltag':arrears=arrears or bool(self.banking.loan.overdue_interest_cents or self.banking.loan.overdue_principal_cents)
        after_tax=profit-tax_due
        payout=0 if arrears else min(max(0,after_tax)//2,max(0,n['cash_cents']-reserve))
        for h,share in zip(self.households(),FinanceSystem.dividends(payout,6)):
            paid=self.pay(n['id'],h['id'],share,'company_dividend','Gewinnausschüttung')
            h['dividend_carry']+=paid
        c['result']=dict(funded_orders_units=orders,profit_before_tax_cents=profit,tax_due_cents=tax_due,tax_paid_cents=tax,
                         after_tax_cents=after_tax,distribution_cents=payout,retained_result_cents=after_tax-payout,
                         reserve_cents=reserve,desired_staff=desired,next_staff=len(n['employees']),staff_reason=reason,
                         distribution_reason='Keine Ausschüttung bei Rückständen.' if arrears else 'Bis zu 50 % des positiven Ergebnisses; Betriebspuffer bleibt auf dem Konto.')

    def households(self):
        return [self.nodes[f'h{i}'] for i in range(1,7)]

    def step(self):
        if self.month>=24 and self.phase==4:
            raise ValueError('Lernlauf mit 24 Monaten abgeschlossen. Bitte neu starten.')
        self.phase=(self.phase+1)%5
        if self.phase==0:
            self.month+=1
            self.month_open={k:n['cash_cents'] for k,n in self.nodes.items()}
            self._reset_metrics()
            self.foreign.begin_month(self)
            self.monetary.begin_month(self)
            self.treasury.begin_month(self)
            for event in self.pending:
                self.active.append(dict(event=event, month=self.month))
                if event=='energy': self.energy_multiplier=2
                if event=='demand': self.propensity=65
                if event=='demand_recovery': self.propensity=95
                self.notice('Energieimporte kosten ab jetzt das Doppelte.' if event=='energy' else 'Haushalte planen ab jetzt 95 % ihres Nettoeinkommens für Konsum ein.' if event=='demand_recovery' else 'Haushalte planen ab jetzt 65 % statt 95 % ihres Nettoeinkommens für Konsum ein.')
            self.pending=[]
        if self.phase==4: self.banking.deliver(self)
        self.model.scheduler.run_step(self.model,self.revision,0,collect_data=False)
        if self.phase==2:
            # Rotate first buyer monthly; budgets depend on money earned by this actual household.
            hs=self.households();offset=(self.month-1)%6
            for h in hs[offset:]+hs[:offset]:
                plan=self.household_outputs(h)
                h['metrics']['consumption_plan']=plan['desired_budget']
                h['metrics']['consumption_budget']=plan['funded_budget']
                before_cash=h['cash_cents']
                h['dividend_carry']=0
                self.buy(h['id'],'alltag',plan['alltag_budget'])
                self.buy(h['id'],'werkstatt',plan['werkstatt_budget'])
                paid=before_cash-h['cash_cents']
                h['metrics']['consumption_paid']=paid
                h['metrics']['reserve_used']=max(0,paid-max(0,h['metrics']['income']-h['metrics']['tax']))
                if plan['funded_budget']<self.essential_budget_cents:
                    self.notice(f"{h['name']}: Das Grundbedarfsbudget ist wegen fehlender Zahlungsmittel nicht vollständig finanzierbar.",h['id'])
        if self.phase==2:self.foreign.purchase(self)
        self.revision+=1
        self.check()
        if self.phase==4:
            self.monetary.close(self)
            self.history.append(dict(month=self.month, consumption_cents=sum(t['amount_cents'] for t in self.journal if t['month']==self.month and t['kind']=='consumption'), employment=sum(h['employer'] is not None for h in self.households()), household_cash_cents=sum(h['cash_cents'] for h in self.households()), government_cash_cents=self.nodes['staat']['cash_cents'],cash_by_sector={s:sum(n['cash_cents'] for n in self.nodes.values() if n['sector']==s) for s in RULES}))
        return self.snapshot()

    def queue(self,event):
        if self.month>=24 or event=='demand_recovery' and self.propensity!=65:
            raise ValueError('Der Eingriff ist jetzt nicht verfügbar.')
        if event not in ('energy','demand','demand_recovery') or event in self.pending or any(x['event']==event for x in self.active):
            raise ValueError('Dieses Ereignis ist ungültig oder bereits ausgelöst.')
        self.pending.append(event)
        self.revision+=1
        return self.snapshot()

    def check(self):
        assert all(n['cash_cents']>=0 for n in self.nodes.values())
        assert sum(n['cash_cents'] for n in self.nodes.values())==self.initial_money+self.banking.created-self.banking.repaid
        self.banking.check(self)
        self.foreign.check(self)
        self.treasury.check(self)
        self.monetary.check(self)
        assert self.nodes['bank']['loan_assets']==sum(self.nodes[f]['loan'] for f in ('alltag','werkstatt'))+self.banking.loan.outstanding_cents+self.treasury.outstanding_cents
        assert all(self.nodes[f]['inventory']>=self.nodes[f].get('reserved_units',0)>=0 for f in ('alltag','werkstatt'))
        for key in ('alltag','werkstatt'):
            n=self.nodes[key];c=n['company'];m=n['metrics']
            assert c['inventory_value_cents']>=0
            if c['plan']:
                assert n['inventory']==c['plan']['opening_units']+m['produced_units']-m['sold_units']
                assert c['inventory_value_cents']==c['plan']['opening_value_cents']+m['production_cost']-m['cost_of_sales']
        employed=[h['id'] for h in self.households() if h['employer']]
        positions=[h for n in self.nodes.values() for h in n.get('employees',[])]
        assert sorted(employed)==sorted(positions) and len(positions)==len(set(positions))

    def snapshot(self,export=False):
        self.check()
        tx=[t for t in self.journal if t['month']==self.month]
        result=dict(world_id=self.id, revision=self.revision, month=self.month, phase=self.phase, phase_label=PHASES[self.phase] if self.phase>=0 else 'Bereit zum Start', nodes=deepcopy(list(self.nodes.values())), transactions=deepcopy(tx), notices=deepcopy(self.notices[-35:]), history=deepcopy(self.history[-36:]), pending=list(self.pending), active=deepcopy(self.active), rules=RULES, audit=dict(total_money_cents=self.banking.initial_deposits, current_money_cents=self.banking.balance(self)['customer_deposits_cents'], transaction_count=len(self.journal), open_obligations_cents=sum(x['amount_cents'] for x in self.obligations)+self.treasury.overdue_interest_cents+self.banking.loan.overdue_interest_cents+self.banking.loan.overdue_principal_cents, loan_principal_cents=self.nodes['bank']['loan_assets'], llm_calls=0), month_open=dict(self.month_open), initial_balances=dict(self.initial), parameters=dict(energy_multiplier=self.energy_multiplier,consumption_percent=self.propensity,essential_budget_cents=self.essential_budget_cents), classification='illustrative_circular_flow_v7',horizon_months=24,completed=self.month==24 and self.phase==4,banking=self.banking.snapshot(self),foreign_trade=self.foreign.snapshot(self),public_finance=self.treasury.snapshot(self),monetary_policy=self.monetary.snapshot(self))
        if export:
            result.update(full_journal=deepcopy(self.journal),initial_balances=dict(self.initial),open_obligations=deepcopy(self.obligations),all_history=deepcopy(self.history),all_notices=deepcopy(self.notices),model_document='poc/WORLD_MODEL.md')
        return result


LOCK=RLock()
WORLDS={}
def world_request(action,payload):
    if not isinstance(payload,dict):raise ValueError('JSON-Objekt erwartet.')
    with LOCK:
        if action=='create':
            if payload:raise ValueError('Neustart erwartet ein leeres Objekt.')
            if len(WORLDS)>=64:del WORLDS[next(iter(WORLDS))]
            w=World();WORLDS[w.id]=w
            return w.snapshot()
        required={'world_id'} if action=='export' else {'world_id','revision'} if action in ('step','credit') else {'world_id','revision','annual_rate_bps'} if action=='rate' else {'world_id','revision','event'}
        if set(payload)!=required:raise ValueError('Ungültige Anfragefelder.')
        key=payload['world_id']
        if not isinstance(key,str) or key not in WORLDS:raise ValueError('Lauf nicht mehr verfügbar. Bitte die Welt neu starten.')
        w=WORLDS[key]
        if action=='export':return w.snapshot(export=True)
        if type(payload['revision']) is not int or payload['revision']!=w.revision:raise ValueError('Veralteter Weltzustand. Bitte neu starten; es wurde kein Schritt doppelt ausgeführt.')
        if action=='step':return w.step()
        if action=='credit':return w.banking.request(w)
        if action=='event':return w.queue(payload['event'])
        if action=='rate':return w.monetary.queue(w,payload['annual_rate_bps'])
        raise ValueError('Unbekannte Aktion.')
