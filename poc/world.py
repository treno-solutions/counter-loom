"""Illustrative, cent-exact circular-flow world. Rules: WORLD_MODEL.md.
BPTK schedules system agents; this ledger owns the authoritative monetary state.
"""
from copy import deepcopy
from threading import RLock
from uuid import uuid4
from BPTK_Py import Model, Agent, SimultaneousScheduler
from systems import HouseholdInput, HouseholdSystem, FirmInput, FirmSystem, GovernmentSystem, FinanceSystem

PHASES = ['Produktion & Löhne', 'Steuern & Transfers', 'Konsum & Aufträge', 'Investitionen', 'Monatsabschluss']
RULES = {
 'households': 'Tatsächlich erhaltenes Einkommen minus 30 % Lohnsteuer bildet das Kaufbudget. Davon werden 95 % konsumiert; nach dem Konsumeingriff 65 %. Nicht ausgegebenes Geld bleibt auf dem Konto. Fehlende Ware oder fehlendes Geld begrenzen den Kauf.',
 'firms': 'Beschäftigte produzieren und erhalten bis zu 2.400 € Bruttolohn. Firmen zahlen Energie und Kreditzinsen, verkaufen vorhandene Ware und versteuern positive operative Überschüsse mit 20 %. Zwei schwache Monate können eine Stelle kosten; nicht bediente Nachfrage kann bei ausreichender Liquidität eine Einstellung auslösen.',
 'government': 'Zwei öffentliche Stellen zu je 2.400 € brutto, bis zu 1.000 € Transfer je unbeschäftigtem Haushalt und bis zu 1.200 € Beschaffung je Betrieb. Alle Zahlungen werden aus dem endlichen Staatskonto geleistet; Einnahmen sind tatsächlich gezahlte Steuern.',
 'bank': 'Je Betrieb besteht anfangs eine Forderung über 12.000 €. Auf tatsächlich vereinnahmte Kreditzinsen folgt am Monatsende eine gleiche Ausschüttung an die sechs Haushalte. Keine Neukredite, Tilgung oder Geldschöpfung in diesem Ausschnitt.',
 'external': 'Vereinfachte Gegenpartei der Energieimporte. Erhaltene Zahlungen verbleiben im Auslandskonto. Keine Rückimporte oder weitere Auslandswirtschaft modelliert.'
}

class SystemAgent(Agent):
    def act(self, time, round_no, step_no):
        self.model.world.act(self.properties['node_id']['value'])

class World:
    def __init__(self):
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
        self.energy_multiplier = 1
        self.propensity = 95
        self._node('alltag', 'Alltag & Versorgung', 'firms', 2400000, employees=['h1','h2'], price=10000, productivity=36, inventory=0, capital=0, loan=1200000, weak_months=0)
        self._node('werkstatt', 'Werkstatt & Technik', 'firms', 2400000, employees=['h3','h4'], price=15000, productivity=20, inventory=0, capital=0, loan=1200000, weak_months=0)
        self._node('staat', 'Staat', 'government', 8000000, employees=['h5','h6'])
        self._node('bank', 'Finanzsektor', 'bank', 1000000, loan_assets=2400000)
        self._node('ausland', 'Ausland · Energie', 'external', 0)
        for i in range(1,7):
            employer = 'alltag' if i<3 else 'werkstatt' if i<5 else 'staat'
            self._node(f'h{i}', f'Haushalt {i}', 'households', 300000, employer=employer, dividend_carry=0)
        self.initial = {k:n['cash_cents'] for k,n in self.nodes.items()}
        self.initial_money = sum(self.initial.values())
        self.month_open = deepcopy(self.initial)
        self._reset_metrics()
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
            n['metrics'] = dict(income=0, tax=0, sales=0, operating_costs=0, wages=0, interest=0, sold_units=0, unmet_units=0, produced_units=0, investment=0, transfers=0)

    def notice(self, text, node='world'):
        self.notices.append(dict(month=self.month, phase=self.phase, node=node, text=text))

    def pay(self, source, target, amount, kind, label, mandatory=False):
        if not isinstance(amount, int) or amount < 0 or source == target:
            raise ValueError('Invalid ledger transfer')
        sender, receiver = self.nodes[source], self.nodes[target]
        paid = min(amount, sender['cash_cents'])
        if paid:
            before = [sender['cash_cents'], receiver['cash_cents']]
            sender['cash_cents'] -= paid
            receiver['cash_cents'] += paid
            self.journal.append(dict(id=len(self.journal)+1, month=self.month, phase=self.phase, source=source, target=target, amount_cents=paid, kind=kind, label=label, source_before=before[0], source_after=sender['cash_cents'], target_before=before[1], target_after=receiver['cash_cents']))
        if paid < amount:
            if mandatory:
                self.obligations.append(dict(month=self.month, source=source, target=target, amount_cents=amount-paid, kind=kind))
            self.notice(f'{sender["name"]}: {((amount-paid)/100):.2f} € für {label} nicht finanziert.', source)
        return paid

    def buy(self, buyer, seller, budget, kind='consumption'):
        firm = self.nodes[seller]
        # A sale, inventory departure and both cash entries form one operation.
        desired = budget // firm['price']
        units = min(desired, firm['inventory'], self.nodes[buyer]['cash_cents']//firm['price'])
        if units:
            paid = self.pay(buyer, seller, units*firm['price'], kind, 'Konsum' if kind=='consumption' else 'Öffentlicher Auftrag' if kind=='procurement' else 'Anlage geliefert')
            firm['inventory'] -= units
            firm['metrics']['sales'] += paid
            firm['metrics']['sold_units'] += units
        firm['metrics']['unmet_units'] += max(0, desired-units)
        return units

    def act(self, node_id):
        n = self.nodes[node_id]
        if self.phase == 0 and n['sector'] in ('firms', 'government'):
            if n['sector']=='firms':
                n['metrics']['produced_units'] = self.firm_outputs(n)['production']
                n['inventory'] += n['metrics']['produced_units']
            for worker in n['employees']:
                paid = self.pay(node_id,worker,GovernmentSystem.wage_per_job,'wage','Lohn',True)
                self.nodes[worker]['metrics']['income'] += paid
                n['metrics']['wages'] += paid
                n['metrics']['operating_costs'] += paid
            if n['sector']=='firms':
                energy = self.pay(node_id,'ausland',len(n['employees'])*18000*self.energy_multiplier,'energy','Energieimport',True)
                interest = self.pay(node_id,'bank',n['loan']*2//1200,'interest','Kreditzins',True)
                n['metrics']['operating_costs'] += energy+interest
                self.nodes['bank']['metrics']['interest'] += interest
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
            reserve = max(1,len(n['employees']))*240000*2
            if (n['metrics']['unmet_units']>0 or n['metrics']['produced_units']>0 and n['metrics']['sold_units']*100>=n['metrics']['produced_units']*80) and n['cash_cents']>=reserve+120000 and self.nodes['werkstatt']['inventory']>=8:
                self.buy('alltag','werkstatt',120000,'investment')
                n['capital'] += 1
                n['metrics']['investment'] += 120000
                self.notice('Alltag & Versorgung kauft eine Anlage: ab nächstem Monat +4 Einheiten Kapazität.',node_id)
        elif self.phase == 4 and n['sector']=='firms':
            profit = max(0,n['metrics']['sales']-n['metrics']['operating_costs'])
            self.pay(node_id,'staat',profit*20//100,'profit_tax','Überschusssteuer',True)
            # Use due costs as well as actual payments; lack of liquidity is not cheap production.
            decision = self.firm_outputs(n)
            n['weak_months'] = decision['weak_months']
            if decision['employment_action']=='release':
                worker = n['employees'].pop()
                self.nodes[worker]['employer'] = None
                n['weak_months']=0
                self.notice(f'{n["name"]}: Stelle von {self.nodes[worker]["name"]} entfällt ab nächstem Monat nach zwei schwachen Umsatzmonaten.', node_id)
            elif decision['employment_action']=='hire':
                candidates=[h for h in self.households() if h['employer'] is None]
                if candidates:
                    worker=candidates[0];n['employees'].append(worker['id']);worker['employer']=node_id
                    self.notice(f'{n["name"]}: {worker["name"]} erhält ab nächstem Monat eine Stelle.',node_id)
        elif self.phase == 4 and node_id=='bank':
            interest=n['metrics']['interest']
            for h,share in zip(self.households(),FinanceSystem.dividends(interest,6)):
                paid=self.pay('bank',h['id'],share,'dividend','Zinsausschüttung')
                h['dividend_carry'] += paid

    def household_outputs(self,n):
        return HouseholdSystem.outputs(HouseholdInput(n['metrics']['income']-n['metrics']['transfers'],n['metrics']['transfers'],n['metrics']['tax'],n['dividend_carry'],n['cash_cents'],self.propensity))

    def firm_outputs(self,n):
        due=len(n['employees'])*(240000+18000*self.energy_multiplier)+n['loan']*2//1200
        return FirmSystem.outputs(FirmInput(len(n['employees']),n['productivity'],n['capital'],n['metrics']['sales'],due,n['weak_months'],n['metrics']['unmet_units'],n['cash_cents']))

    def households(self):
        return [self.nodes[f'h{i}'] for i in range(1,7)]

    def step(self):
        if self.month>=240 and self.phase==4:
            raise ValueError('Technische Laufgrenze von 240 Monaten erreicht. Bitte neu starten.')
        self.phase=(self.phase+1)%5
        if self.phase==0:
            self.month+=1
            self.month_open={k:n['cash_cents'] for k,n in self.nodes.items()}
            self._reset_metrics()
            for event in self.pending:
                self.active.append(dict(event=event, month=self.month))
                if event=='energy': self.energy_multiplier=2
                if event=='demand': self.propensity=65
                self.notice('Energieimporte kosten ab jetzt das Doppelte.' if event=='energy' else 'Haushalte planen ab jetzt 65 % statt 95 % ihres Nettoeinkommens für Konsum ein.')
            self.pending=[]
        self.model.scheduler.run_step(self.model,self.revision,0,collect_data=False)
        if self.phase==2:
            # Rotate first buyer monthly; budgets depend on money earned by this actual household.
            hs=self.households();offset=(self.month-1)%6
            for h in hs[offset:]+hs[:offset]:
                plan=self.household_outputs(h)
                h['dividend_carry']=0
                self.buy(h['id'],'alltag',plan['alltag_budget'])
                self.buy(h['id'],'werkstatt',plan['werkstatt_budget'])
        self.revision+=1
        self.check()
        if self.phase==4:
            self.history.append(dict(month=self.month, consumption_cents=sum(t['amount_cents'] for t in self.journal if t['month']==self.month and t['kind']=='consumption'), employment=sum(h['employer'] is not None for h in self.households()), household_cash_cents=sum(h['cash_cents'] for h in self.households()), government_cash_cents=self.nodes['staat']['cash_cents'],cash_by_sector={s:sum(n['cash_cents'] for n in self.nodes.values() if n['sector']==s) for s in RULES}))
        return self.snapshot()

    def queue(self,event):
        if event not in ('energy','demand') or event in self.pending or any(x['event']==event for x in self.active):
            raise ValueError('Dieses Ereignis ist ungültig oder bereits ausgelöst.')
        self.pending.append(event)
        self.revision+=1
        return self.snapshot()

    def check(self):
        assert all(n['cash_cents']>=0 for n in self.nodes.values())
        assert sum(n['cash_cents'] for n in self.nodes.values())==self.initial_money
        assert self.nodes['bank']['loan_assets']==sum(self.nodes[f]['loan'] for f in ('alltag','werkstatt'))
        assert all(self.nodes[f]['inventory']>=0 for f in ('alltag','werkstatt'))
        employed=[h['id'] for h in self.households() if h['employer']]
        positions=[h for n in self.nodes.values() for h in n.get('employees',[])]
        assert sorted(employed)==sorted(positions) and len(positions)==len(set(positions))

    def snapshot(self,export=False):
        self.check()
        tx=[t for t in self.journal if t['month']==self.month]
        result=dict(world_id=self.id, revision=self.revision, month=self.month, phase=self.phase, phase_label=PHASES[self.phase] if self.phase>=0 else 'Bereit zum Start', nodes=deepcopy(list(self.nodes.values())), transactions=deepcopy(tx), notices=deepcopy(self.notices[-35:]), history=deepcopy(self.history[-36:]), pending=list(self.pending), active=deepcopy(self.active), rules=RULES, audit=dict(total_money_cents=self.initial_money, current_money_cents=sum(n['cash_cents'] for n in self.nodes.values()), transaction_count=len(self.journal), open_obligations_cents=sum(x['amount_cents'] for x in self.obligations), loan_principal_cents=self.nodes['bank']['loan_assets'], llm_calls=0), month_open=dict(self.month_open), initial_balances=dict(self.initial), parameters=dict(energy_multiplier=self.energy_multiplier,consumption_percent=self.propensity), classification='illustrative_circular_flow_v1')
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
        required={'world_id'} if action=='export' else {'world_id','revision'} if action=='step' else {'world_id','revision','event'}
        if set(payload)!=required:raise ValueError('Ungültige Anfragefelder.')
        key=payload['world_id']
        if not isinstance(key,str) or key not in WORLDS:raise ValueError('Lauf nicht mehr verfügbar. Bitte die Welt neu starten.')
        w=WORLDS[key]
        if action=='export':return w.snapshot(export=True)
        if type(payload['revision']) is not int or payload['revision']!=w.revision:raise ValueError('Veralteter Weltzustand. Bitte neu starten; es wurde kein Schritt doppelt ausgeführt.')
        if action=='step':return w.step()
        if action=='event':return w.queue(payload['event'])
        raise ValueError('Unbekannte Aktion.')
