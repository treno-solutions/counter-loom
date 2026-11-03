"""Illustrative, cent-exact circular-flow world. Rules: WORLD_MODEL.md.
BPTK schedules system agents; this ledger owns the authoritative monetary state.
"""
from copy import deepcopy
from threading import RLock
from uuid import uuid4
from BPTK_Py import Model, Agent, SimultaneousScheduler
from banking import Banking
from treasury import Treasury
from crisis import Closure, STANDBY_COST, compare
from rates import MonetaryPolicy
from pricing import Pricing, BASE_PRICES
from foreign import ForeignTrade
from firms import initial_company, plan as company_plan, staffing, forecast, outlook, work_target, MIN_WORK_BPS, WORK_STEP_BPS, MAX_BRIDGE_MONTHS, RESTART_CLOSES
from systems import HouseholdInput, HouseholdSystem, GovernmentSystem, FinanceSystem

PHASES = ['Produktion & Löhne', 'Steuern & Transfers', 'Konsum & Aufträge', 'Investitionen', 'Monatsabschluss']
RULES = {
 'households': 'Kaufplan: mindestens 1.000 € monatlicher Grundbedarf als illustrative Annahme, darüber 95 % des Nettoeinkommens (nach Konsumeingriff 65 %). Der Grundbedarfsplan kann aus vorhandenem Kontoguthaben finanziert werden. Käufe sind durch Geld, Lager und ganze Gütereinheiten begrenzt; unerfüllte Kaufpläne sind keine gebuchten Ausgaben oder Schulden.',
 'firms': 'Betriebe planen Absatz, Lager und Arbeitszeit. Der Vollzeitlohnsatz bleibt fest; tatsächliche Löhne und Kapazität folgen der Arbeitszeit. Eine begrenzte Verlustbrücke nutzt vorhandene Liquidität. Stilllegung beendet die Arbeit, erhält aber Lager, Anlagen und Schuld. Wiederanlauf benötigt zwei tragfähige Prüfungen und einen finanzierten Betriebspuffer. Lager bleibt zu Herstellungskosten bewertet. Ausschüttungen sind bei Rückständen oder ohne tragfähigen Weiterbetrieb gesperrt. Illustrative Regeln.',
 'government': 'Zwei öffentliche Stellen zu je 2.400 € brutto, bis zu 1.000 € Transfer je unbeschäftigtem Haushalt und bis zu 1.200 € Beschaffung je Betrieb. Vorhandene Kasse finanziert Ausgaben. Beim Abschluss schützt ein begrenzter Staatskredit bis 50.000 € bei Bedarf eine Reserve für einen Monat geplanter Ausgaben einschließlich neuer Monatszinsen. Neue Kreditbeträge erhalten den Leitzins plus einen Modellaufschlag; der vereinbarte Zins bleibt je Betrag fest und fällt ab Folgemonat an. Guthaben oberhalb des Reserveziels kann Schuld tilgen. Die Reserve ist nicht gesperrt; bei Kreditgrenze oder fehlendem Bankkapital darf die Kasse auch unter das Ziel fallen. Kredit ist Finanzierung, keine Steuereinnahme.',
 'bank': 'Eine Bank führt die Guthaben aller Nichtbanken. Eigenkapital und Kundeneinlagen sind getrennt. Ein begrenzter Maschinenkredit für acht Werkstatteinheiten schafft eine Einlage und eine Kreditforderung; Tilgung baut beide ab. Zinsen sind Bankertrag. Ein begrenzter Staatskredit sichert bei Bedarf eine Reserve für einen Monat geplanter Staatsausgaben; darüber wird vorhandene Kasse genutzt. Tatsächlich vereinnahmte Firmen- und Staatszinsen werden am Monatsende an Haushalte ausgeschüttet.',
 'external': 'Ein vereinfachtes Auslandskonto erhält Energiezahlungen und kauft inländische Waren: monatlich bis zu sechs Alltags- und zwei Werkstatteinheiten. Nur Guthaben vom Monatsbeginn finanziert Bestellungen. Bezahlung und Lagerabgang erfolgen gemeinsam; fehlendes Geld oder Ware begrenzt den Rückfluss. Keine Wechselkurse oder vollständige Auslandswirtschaft.'
}

class SystemAgent(Agent):
    def act(self, time, round_no, step_no):
        self.model.world.act(self.properties['node_id']['value'])

class World:
    def __init__(self, essential_budget_cents=100000, export_orders_units=None, government_credit_limit_cents=5000000, government_annual_rate_bps=300, initial_policy_rate_bps=200, energy_pass_through_bps=5000, government_reserve_months=1, government_initial_cash_cents=8000000, horizon_months=None):
        if type(government_initial_cash_cents) is not int or government_initial_cash_cents<0:
            raise ValueError('Initial state cash must be nonnegative whole cents.')
        if horizon_months is not None and (type(horizon_months) is not int or horizon_months<1):
            raise ValueError('Optional observation horizon must be a positive whole month.')
        self.horizon_months=horizon_months
        self.id = uuid4().hex[:16]
        self.revision = 0
        self.month = 0
        self.phase = -1
        self.nodes = {}
        self.journal = []
        self.obligations = []
        self.notices = []
        self.history = []
        self.household_month = []
        self.crisis = Closure()
        self.pending = []
        self.active = []
        self.essential_budget_cents = essential_budget_cents
        self.energy_multiplier = 1
        self.propensity = 95
        self._node('alltag', 'Alltag & Versorgung', 'firms', 2400000, employees=['h1','h2'], price=10000, productivity=36, inventory=0, capital=0, loan=1200000, weak_months=0, reserved_units=0, machine_loan_cents=0)
        self._node('werkstatt', 'Werkstatt & Technik', 'firms', 2400000, employees=['h3','h4'], price=15000, productivity=20, inventory=0, capital=0, loan=1200000, weak_months=0, reserved_units=0, machine_loan_cents=0)
        self._node('staat', 'Staat', 'government', government_initial_cash_cents, employees=['h5','h6'], government_loan_cents=0)
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
        self.treasury = Treasury(self,government_credit_limit_cents,government_annual_rate_bps,government_reserve_months)
        self.pricing = Pricing(self,energy_pass_through_bps)
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
            n['metrics'] = dict(income=0, tax=0, sales=0, operating_costs=0, wages=0, interest=0, sold_units=0, unmet_units=0, produced_units=0, investment=0, transfers=0, consumption_plan=0, consumption_budget=0, consumption_paid=0, reserve_used=0, unfunded_units=0, production_plan=0, cost_of_sales=0, production_cost=0, idle_cost=0, interest_expense=0, unpaid_wages=0, short_time=0, closure_cost=0, closure_blocked_units=0)

    def notice(self, text, node='world'):
        self.notices.append(dict(month=self.month, phase=self.phase, node=node, text=text))

    def pay(self, source, target, amount, kind, label, mandatory=False):
        if not isinstance(amount, int) or amount < 0 or source == target:
            raise ValueError('Invalid ledger transfer')
        if source=='staat' and kind in ('wage','transfer','short_time','procurement','government_interest'):
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

    def buy(self, buyer, seller, budget, kind='consumption', spending_limit=None, unit_price_cents=None):
        firm = self.nodes[seller]
        price=firm['price'] if unit_price_cents is None else unit_price_cents
        if type(price) is not int or price<=0:raise ValueError('Unit price must be a positive number of cents.')
        # A sale, inventory departure and both cash entries form one operation.
        desired = budget // price
        if buyer=='staat' and kind=='procurement' and not self.crisis.closed(self,seller):
            self.treasury.ensure_cash(self,min(desired,firm['inventory']-firm.get('reserved_units',0))*price)
        funded_desired = min(desired,self.nodes[buyer]['cash_cents']//price)
        if spending_limit is not None:
            funded_desired=min(funded_desired,spending_limit//price)
        units = 0 if self.crisis.closed(self,seller) else min(funded_desired, firm['inventory']-firm.get('reserved_units',0))
        if self.crisis.closed(self,seller):firm['metrics']['closure_blocked_units']+=funded_desired
        if units:
            stock_before=firm['inventory']
            paid = self.pay(buyer, seller, units*price, kind, 'Konsum' if kind=='consumption' else 'Öffentlicher Auftrag' if kind=='procurement' else 'Warenexport bezahlt' if kind=='export_sale' else 'Anlage geliefert')
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
                plan_node=deepcopy(n) if self.crisis.closed(self,node_id) else n
                if self.crisis.closed(self,node_id):plan_node['company']['work_bps']=0
                p=company_plan(plan_node,self.energy_multiplier,self.machine_due(node_id))
                n['company']['plan']=p
                n['metrics']['production_plan']=p['production_units']
            for worker in n['employees']:
                paid=self.pay(node_id,worker,GovernmentSystem.wage_per_job if node_id=='staat' else n['company']['plan']['wage_per_worker_cents'],'wage','Lohn',True)
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
                # One common floor for combined labour/machine capacity, matching the plan.
                labor_capacity=(len(n['employees'])*n['productivity']+n['capital']*4)*m['wages']//max(1,len(n['employees'])*240000)
                units=min(p['production_units'],labor_capacity,n['cash_cents']//p['energy_unit_cents'])
                energy=self.pay(node_id,'ausland',units*p['energy_unit_cents'],'energy','Energie für Produktion')
                m['operating_costs']+=energy
                m['produced_units']=units
                # Paid idle labour is an expense; productive labour is carried in stock.
                productive_wages=m['wages']*units//max(1,labor_capacity)
                m['production_cost']=productive_wages+energy
                m['idle_cost']=m['wages']-productive_wages
                if self.crisis.closed(self,node_id):
                    upkeep=self.pay(node_id,'ausland',STANDBY_COST,'closure_cost','Erhaltungsenergie bei Schliessung',True)
                    m['closure_cost']=STANDBY_COST
                    m['operating_costs']+=upkeep
                n['inventory']+=units
                n['company']['inventory_value_cents']+=m['production_cost']
        elif self.phase == 1 and n['sector']=='households':
            n['metrics']['tax'] = self.pay(node_id,'staat',self.household_outputs(n)['tax_due'],'income_tax','Einkommensteuer',True)
        elif self.phase == 1 and node_id=='staat':
            self.crisis.pay_benefits(self)
            for h in self.households():
                if h['employer'] is None:
                    transfer = self.pay('staat',h['id'],GovernmentSystem.transfer_per_unemployed,'transfer','Transfer')
                    h['metrics']['income'] += transfer
                    h['metrics']['transfers'] += transfer
        elif self.phase == 2 and node_id=='staat':
            for firm in ('alltag','werkstatt'):
                self.buy('staat',firm,GovernmentSystem.procurement_per_firm,'procurement')
        elif self.phase == 3 and node_id=='alltag':
            if self.crisis.closed(self,'alltag') or self.crisis.closed(self,'werkstatt'):return
            if self.banking.originate(self) or self.banking.loan.status=='credited': return
            _,reserve=staffing(n,self.energy_multiplier,self.machine_due(node_id,True))
            machine_cost=8*self.nodes['werkstatt']['price']
            if n['company']['short_months']>=2 and self.month-n['company']['last_investment_month']>=3 and n['cash_cents']>=reserve+machine_cost and self.nodes['werkstatt']['inventory']-self.nodes['werkstatt'].get('reserved_units',0)>=8:
                self.buy('alltag','werkstatt',machine_cost,'investment')
                n['capital']+=1
                n['metrics']['investment']+=machine_cost
                n['company']['last_investment_month']=self.month
                self.notice('Alltag & Versorgung kauft nach anhaltendem Engpass eine Anlage: ab nächstem Monat +4 Einheiten Vollzeitkapazität, bei Teilzeit anteilig.',node_id)
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
        if not self.crisis.closed(self,n['id']):
            forecast(c,orders)
            c['short_months']=c['short_months']+1 if m['unmet_units']>0 else 0
        profit=m['sales']-m['cost_of_sales']-m['idle_cost']-m['unpaid_wages']-m['interest_expense']-m['closure_cost']
        tax_due=max(0,profit)*20//100
        tax=self.pay(n['id'],'staat',tax_due,'profit_tax','Gewinnsteuer',True)
        desired,_=staffing(n,self.energy_multiplier,self.machine_due(n['id'],True))
        staff=len(n['employees']);c['profitable_months']=c['profitable_months']+1 if profit>0 else 0
        c['loss_used_cents']+=max(0,-profit)
        debt=self.machine_due(n['id'],True)
        candidate=next((h for h in self.households() if h['employer'] is None),None)
        if self.crisis.closed(self,n['id']):
            option=outlook(n,self.energy_multiplier,staff,c['work_bps'],debt)
            demand_ok=c['forecast_milli']>=1000; margin_ok=option['projected_gap_cents']==0
            cash_ok=n['cash_cents']>=option['required_cash_cents']
            c['next_status']=c['status'];c['next_work_bps']=c['work_bps']
            reason='Angeordnete befristete Schliessung: Verträge und Vor-Krisen-Arbeitszeitplan bleiben erhalten. Keine automatische Entlassung oder Ausschüttung; Schuldendienst und Erhaltungskosten laufen weiter.'
        elif c['status']=='mothballed':
            work=work_target(n,1);option=outlook(n,self.energy_multiplier,1,work,debt)
            if c['profitable_months']>=2 and n['cash_cents']>=option['reserve_cents']:c['loss_used_cents']=0
            demand_ok=c['forecast_milli']>=1000
            margin_ok=option['projected_gap_cents']==0 and demand_ok
            cash_ok=n['cash_cents']>=option['reserve_cents']
            c['restart_signal']=c['restart_signal']+1 if margin_ok and cash_ok else 0
            ready=c['restart_signal']>=RESTART_CLOSES and candidate is not None
            if ready:
                n['employees'].append(candidate['id']);candidate['employer']=n['id']
                c['next_status']='restarting';c['next_work_bps']=work;c['staff_signal']=0;c['bridge_months']=0
                reason='Wiederanlauf nach zwei tragfähigen Prüfungen: eine Arbeitskraft und vorfinanzierter Betriebspuffer; Produktion ab Folgemonat.'
            else:
                c['next_status']='mothballed';c['next_work_bps']=0
                reason='Stillgelegt: Wiederanlauf benötigt Nachfrage, einen Plan ohne neue Finanzierungslücke, zwei finanzierte Lohnrunden und zwei bestätigte Abschlüsse sowie freie Arbeitskraft.'
        else:
            c['restart_signal']=0
            direction=1 if desired>staff else -1 if desired<staff else 0
            old=c['staff_signal'];c['staff_signal']=old+direction if direction and old*direction>0 else direction
            if abs(c['staff_signal'])>=2:
                if direction<0 and staff>1:
                    worker=n['employees'].pop();self.nodes[worker]['employer']=None;c['staff_signal']=0
                elif direction>0 and candidate is not None:
                    trial_target=work_target(n,staff+1)
                    trial_work=max(MIN_WORK_BPS,min(c['work_bps']+WORK_STEP_BPS,max(c['work_bps']-WORK_STEP_BPS,trial_target)))
                    trial=outlook(n,self.energy_multiplier,staff+1,trial_work,debt)
                    if c['profitable_months']>=2 and n['cash_cents']>=trial['reserve_cents']:c['loss_used_cents']=0
                    trial_bridge=c['bridge_months']<MAX_BRIDGE_MONTHS and trial['projected_gap_cents']<=max(0,c['loss_budget_cents']-c['loss_used_cents'])
                    if n['cash_cents']>=trial['reserve_cents'] and (trial['projected_gap_cents']==0 or trial_bridge):
                        n['employees'].append(candidate['id']);candidate['employer']=n['id'];c['staff_signal']=0
            target=work_target(n,len(n['employees']))
            work=max(MIN_WORK_BPS,min(c['work_bps']+WORK_STEP_BPS,max(c['work_bps']-WORK_STEP_BPS,target)))
            option=outlook(n,self.energy_multiplier,len(n['employees']),work,debt)
            demand_ok=c['forecast_milli']>=1000;margin_ok=option['projected_gap_cents']==0 and demand_ok
            cash_ok=n['cash_cents']>=option['required_cash_cents']
            if c['profitable_months']>=2 and n['cash_cents']>=option['reserve_cents']:c['loss_used_cents']=0
            room=max(0,c['loss_budget_cents']-c['loss_used_cents'])
            bridge_ok=cash_ok and c['bridge_months']<MAX_BRIDGE_MONTHS and option['projected_gap_cents']<=room
            if not cash_ok or not margin_ok and not bridge_ok:
                for worker in n['employees']:self.nodes[worker]['employer']=None
                n['employees']=[];c['next_status']='mothballed';c['next_work_bps']=0;c['restart_signal']=0;c['staff_signal']=0
                reason='Stilllegung ab Folgemonat: Vorfinanzierung fehlt oder die begrenzte Verlustbrücke reicht nicht. Lager, Anlagen und Schuld bleiben bestehen.'
            elif not margin_ok:
                c['next_status']='buffered';c['next_work_bps']=work;c['bridge_months']+=1
                reason='Befristeter Weiterbetrieb aus vorhandener Liquidität: erwartete Finanzierungslücke innerhalb von Verlustbudget und höchstens drei Brückenmonaten.'
            else:
                c['next_status']='operating';c['next_work_bps']=work;c['bridge_months']=0
                reason='Tragfähiger Betriebsplan; Arbeitszeit folgt Produktionsbedarf mit höchstens 25 Prozentpunkten Änderung pro Monat.'
        reserve=option['reserve_cents']
        if len(n['employees'])!=staff or c['next_status']!=c['status'] or c['next_work_bps']!=c['work_bps']:
            self.notice(n['name']+': '+reason+' Gilt ab nächstem Monat.',n['id'])
        arrears=any(o['source']==n['id'] for o in self.obligations)
        if n['id']=='alltag':arrears=arrears or bool(self.banking.loan.overdue_interest_cents or self.banking.loan.overdue_principal_cents)
        after_tax=profit-tax_due
        payout=0 if self.crisis.closed(self,n['id']) or arrears or c['next_status']!='operating' else min(max(0,after_tax)//2,max(0,n['cash_cents']-reserve))
        for h,share in zip(self.households(),FinanceSystem.dividends(payout,6)):
            paid=self.pay(n['id'],h['id'],share,'company_dividend','Gewinnausschüttung')
            h['dividend_carry']+=paid
        c['result']=dict(funded_orders_units=orders,profit_before_tax_cents=profit,tax_due_cents=tax_due,tax_paid_cents=tax,
                         after_tax_cents=after_tax,distribution_cents=payout,retained_result_cents=after_tax-payout,
                         reserve_cents=reserve,desired_staff=desired,next_staff=len(n['employees']),staff_reason=reason,
                         next_status=c['next_status'],next_work_bps=c['next_work_bps'],projected_gap_cents=option['projected_gap_cents'],
                         expected_receipts_cents=option['expected_receipts_cents'],required_cash_cents=option['required_cash_cents'],
                         demand_ok=demand_ok,margin_ok=margin_ok,cash_ok=cash_ok,restart_ready=c['restart_signal']>=RESTART_CLOSES,
                         loss_this_month_cents=max(0,-profit),
                         distribution_reason='Keine Ausschüttung bei Rückständen oder ohne regulär tragfähigen Weiterbetrieb.' if arrears or c['next_status']!='operating' else 'Bis zu 50 % des positiven Ergebnisses; Betriebspuffer bleibt auf dem Konto.')

    def households(self):
        return [self.nodes[f'h{i}'] for i in range(1,7)]

    def step(self):
        if self.horizon_months is not None and self.month>=self.horizon_months and self.phase==4:
            raise ValueError('Gewählter Beobachtungszeitraum abgeschlossen. Bitte neu starten.')
        self.phase=(self.phase+1)%5
        if self.phase==0:
            self.month+=1
            self.month_open={k:n['cash_cents'] for k,n in self.nodes.items()}
            self._reset_metrics()
            for firm_id in ('alltag','werkstatt'):
                company=self.nodes[firm_id]['company']
                company['status']=company['next_status']
                company['work_bps']=company['next_work_bps']
            self.household_month = []
            self.monetary.begin_month(self)
            self.crisis.begin_month(self)
            self.treasury.begin_month(self)
            for event in self.pending:
                self.active.append(dict(event=event, month=self.month))
                if event=='energy': self.energy_multiplier=2
                if event=='energy_recovery': self.energy_multiplier=1
                if event=='demand': self.propensity=65
                if event=='demand_recovery': self.propensity=95
                self.notice('Energieimporte kosten ab jetzt wieder den Ausgangspreis.' if event=='energy_recovery' else 'Energieimporte kosten ab jetzt das Doppelte.' if event=='energy' else 'Haushalte planen ab jetzt 95 % ihres Nettoeinkommens für Konsum ein.' if event=='demand_recovery' else 'Haushalte planen ab jetzt 65 % statt 95 % ihres Nettoeinkommens für Konsum ein.')
            self.pending=[]
            self.pricing.begin_month(self)
            self.foreign.begin_month(self)
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
                prior_dividend=h['dividend_carry']
                h['dividend_carry']=0
                purchased={key:self.buy(h['id'],key,plan[f'{key}_budget']) for key in ('alltag','werkstatt')}
                desired_split={'alltag':plan['desired_budget']*55//100}
                desired_split['werkstatt']=plan['desired_budget']-desired_split['alltag']
                goods=[dict(seller=key,unit_price_cents=self.nodes[key]['price'],base_price_cents=BASE_PRICES[key],
                    desired_units=desired_split[key]//self.nodes[key]['price'],paid_units=purchased[key]) for key in ('alltag','werkstatt')]
                paid=before_cash-h['cash_cents']
                purchasable=sum(plan[f'{key}_budget']//self.nodes[key]['price']*self.nodes[key]['price'] for key in ('alltag','werkstatt'))
                self.household_month.append(dict(id=h['id'],employer=h['employer'],goods=goods,
                    desired_real_cents=sum(g['desired_units']*g['base_price_cents'] for g in goods),
                    paid_real_cents=sum(g['paid_units']*g['base_price_cents'] for g in goods),
                    desired_cents=plan['desired_budget'],funded_cents=plan['funded_budget'],paid_cents=paid,
                    funding_gap_cents=plan['desired_budget']-plan['funded_budget'],
                    stock_gap_cents=purchasable-paid,unit_remainder_cents=plan['funded_budget']-purchasable,
                    income_cents=h['metrics']['income'],tax_cents=h['metrics']['tax'],
                    transfers_cents=h['metrics']['transfers'],short_time_cents=h['metrics']['short_time'],closure_gap_cents=sum(plan[f'{key}_budget']//self.nodes[key]['price']*self.nodes[key]['price'] for key in ('alltag','werkstatt') if self.crisis.closed(self,key)),prior_dividend_cents=prior_dividend,cash_before_cents=before_cash))
                h['metrics']['consumption_paid']=paid
                h['metrics']['reserve_used']=max(0,paid-max(0,h['metrics']['income']-h['metrics']['tax']))
                if plan['funded_budget']<self.essential_budget_cents:
                    self.notice(f"{h['name']}: Das Grundbedarfsbudget ist wegen fehlender Zahlungsmittel nicht vollständig finanzierbar.",h['id'])
        if self.phase==2:self.foreign.purchase(self)
        self.revision+=1
        self.check()
        if self.phase==4:
            self.monetary.close(self)
            self.history.append(dict(month=self.month,crisis=self.crisis.snapshot(self),market=self.pricing.market(self), consumption_percent=self.propensity,essential_budget_cents=self.essential_budget_cents, households=sorted(deepcopy(self.household_month),key=lambda h:h['id']), consumption_cents=sum(t['amount_cents'] for t in self.journal if t['month']==self.month and t['kind']=='consumption'), employment=sum(h['employer'] is not None for h in self.households()), household_cash_cents=sum(h['cash_cents'] for h in self.households()), government_cash_cents=self.nodes['staat']['cash_cents'],cash_by_sector={s:sum(n['cash_cents'] for n in self.nodes.values() if n['sector']==s) for s in RULES}))
        return self.snapshot()

    def queue(self,event):
        if self.horizon_months is not None and self.month>=self.horizon_months:
            raise ValueError('Der Eingriff ist im letzten Beobachtungsmonat nicht verfügbar.')
        targets={'energy':('energy_multiplier',2),'energy_recovery':('energy_multiplier',1),
                 'demand':('propensity',65),'demand_recovery':('propensity',95)}
        if event not in targets or event in self.pending:
            raise ValueError('Dieses Ereignis ist ungültig oder bereits vorgemerkt.')
        attribute,target=targets[event]
        if getattr(self,attribute)==target or any(targets[e][0]==attribute for e in self.pending):
            raise ValueError('Dieser Zielwert gilt bereits oder für diesen Bereich ist schon ein Eingriff vorgemerkt.')
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
        result=dict(world_id=self.id, revision=self.revision, month=self.month, phase=self.phase, phase_label=PHASES[self.phase] if self.phase>=0 else 'Bereit zum Start', nodes=deepcopy(list(self.nodes.values())), transactions=deepcopy(tx), notices=deepcopy(self.notices[-35:]), history=deepcopy(self.history[-36:]), pending=list(self.pending), active=deepcopy(self.active), rules=RULES, audit=dict(total_money_cents=self.banking.initial_deposits, current_money_cents=self.banking.balance(self)['customer_deposits_cents'], transaction_count=len(self.journal), open_obligations_cents=sum(x['amount_cents'] for x in self.obligations)+self.treasury.overdue_interest_cents+self.banking.loan.overdue_interest_cents+self.banking.loan.overdue_principal_cents, loan_principal_cents=self.nodes['bank']['loan_assets'], llm_calls=0), month_open=dict(self.month_open), initial_balances=dict(self.initial), parameters=dict(energy_multiplier=self.energy_multiplier,consumption_percent=self.propensity,essential_budget_cents=self.essential_budget_cents), classification='illustrative_circular_flow_v11',crisis=self.crisis.snapshot(self),horizon_months=self.horizon_months,completed=self.horizon_months is not None and self.month>=self.horizon_months and self.phase==4,banking=self.banking.snapshot(self),foreign_trade=self.foreign.snapshot(self),public_finance=self.treasury.snapshot(self),monetary_policy=self.monetary.snapshot(self),pricing=self.pricing.snapshot(self))
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
        required={'world_id'} if action=='export' else {'world_id','revision'} if action in ('step','credit') else {'world_id','revision','firm','duration','replacement_bps'} if action in ('closure','compare') else {'world_id','revision','annual_rate_bps'} if action=='rate' else {'world_id','revision','event'}
        if set(payload)!=required:raise ValueError('Ungültige Anfragefelder.')
        key=payload['world_id']
        if not isinstance(key,str) or key not in WORLDS:raise ValueError('Lauf nicht mehr verfügbar. Bitte die Welt neu starten.')
        w=WORLDS[key]
        if action=='export':return w.snapshot(export=True)
        if type(payload['revision']) is not int or payload['revision']!=w.revision:raise ValueError('Veralteter Weltzustand. Bitte neu starten; es wurde kein Schritt doppelt ausgeführt.')
        if action=='step':return w.step()
        if action=='credit':return w.banking.request(w)
        if action=='event':return w.queue(payload['event'])
        if action=='closure':return w.crisis.queue(w,payload['firm'],payload['duration'],payload['replacement_bps'])
        if action=='compare':return compare(w,payload['firm'],payload['duration'],payload['replacement_bps'])
        if action=='rate':return w.monetary.queue(w,payload['annual_rate_bps'])
        raise ValueError('Unbekannte Aktion.')
