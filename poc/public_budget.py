"""Bounded illustrative public budget: persistent deficits and funded public jobs."""
from copy import deepcopy
from systems import GovernmentSystem

WAGE = GovernmentSystem.wage_per_job
TRANSFER = GovernmentSystem.transfer_per_unemployed
PROCUREMENT = GovernmentSystem.procurement_per_firm

class PublicBudget:
    def __init__(self, world, policy):
        if policy not in ('legacy','adaptive'):raise ValueError('Ungültige staatliche Budgetregel.')
        self.policy=policy
        self.target_staff=2
        self.procurement_bps=10000
        self.next_target_staff=2
        self.next_procurement_bps=10000
        self.deficit_streak=0
        self.surplus_streak=0
        self.revenues=[]
        self.history=[]
        self.last_begin=0
        self.last_review=0
        self.plan=dict(month=0,requested_staff=len(world.nodes['staat']['employees']),approved_staff=len(world.nodes['staat']['employees']),
                       payroll_cents=len(world.nodes['staat']['employees'])*WAGE,social_need_cents=0,
                       procurement_cents=2*PROCUREMENT,procurement_bps=10000,funding_capacity_cents=world.nodes['staat']['cash_cents'],
                       hard_funding_cut=False,released=[],hired=[],opening_wage_arrears_cents=0)
        self.decision='hold'
        self.reason='Budgetprüfung nach dem Monatsabschluss; Änderungen gelten erst ab dem nächsten Monat.'
        self.effective_month=0

    def social_need(self,world,public_staff=None):
        unemployed=sum(h['employer'] is None for h in world.households())
        current=len(world.nodes['staat']['employees'])
        if public_staff is not None:unemployed+=current-public_staff
        return max(0,unemployed)*TRANSFER+world.crisis.planned_benefits(world)

    def begin_month(self,world):
        if self.last_begin==world.month:return
        self.last_begin=world.month
        self.target_staff=self.next_target_staff
        self.procurement_bps=self.next_procurement_bps
        self.decision='hold';self.reason='Reguläre Budgetprüfung beim Monatsabschluss.';self.effective_month=world.month+1
        state=world.nodes['staat'];old=list(state['employees']);released=[];hired=[]
        requested=self.target_staff if self.policy=='adaptive' else len(old)
        interest=world.treasury.overdue_interest_cents+world.treasury.month_interest_charge_cents
        credit=max(0,world.treasury.credit_limit_cents-world.treasury.outstanding_cents) if world.nodes['bank']['cash_cents']>0 else 0
        capacity=max(0,state['cash_cents']+credit-interest)
        approved=len(old)
        hard=False
        if self.policy=='adaptive':
            available=len(old)+sum(h['employer'] is None for h in world.households())
            candidates=range(min(requested,available),-1,-1)
            approved=next((staff for staff in candidates if staff*WAGE+self.social_need(world,staff)<=capacity),0)
            hard=approved<min(requested,available)
            if hard:
                self.target_staff=approved;self.next_target_staff=approved
                self.procurement_bps=0;self.next_procurement_bps=0
            while len(state['employees'])>approved:
                worker=state['employees'].pop();world.nodes[worker]['employer']=None;released.append(worker)
            for h in world.households():
                if len(state['employees'])>=approved:break
                if h['employer'] is None:
                    state['employees'].append(h['id']);h['employer']='staat';hired.append(h['id'])
            # Confirm financing before work, not merely a forecast of later taxes.
            need=approved*WAGE+self.social_need(world)+interest
            world.treasury.ensure_cash(world,need)
            assert state['cash_cents']>=approved*WAGE+min(interest,state['cash_cents'])
        self.plan=dict(month=world.month,requested_staff=requested,approved_staff=approved,payroll_cents=approved*WAGE,
                       social_need_cents=self.social_need(world),procurement_cents=2*(PROCUREMENT*self.procurement_bps//10000),
                       procurement_bps=self.procurement_bps,funding_capacity_cents=capacity,hard_funding_cut=hard,released=released,hired=hired,
                       opening_wage_arrears_cents=sum(o['amount_cents'] for o in world.obligations if o['source']=='staat' and o['kind']=='wage'))
        if hard or released or hired:
            world.notice(f'Staatsbudget ab Monat {world.month}: {approved} vollständig finanzierte öffentliche Stellen; {len(released)} Verträge beendet, {len(hired)} neu besetzt. Beschaffungsquote {self.procurement_bps/100:g} %. Keine Arbeit gegen ungeklärte Lohnfinanzierung.','staat')

    def procurement_per_firm(self):
        return PROCUREMENT*self.procurement_bps//10000 if self.policy=='adaptive' else PROCUREMENT

    def pay_social(self,world):
        if self.policy=='legacy':
            world.crisis.pay_benefits(world)
            for h in world.households():
                if h['employer'] is None:
                    paid=world.pay('staat',h['id'],TRANSFER,'transfer','Transfer')
                    h['metrics']['income']+=paid;h['metrics']['transfers']+=paid
            return
        rows=[dict(id=h['id'],due_cents=TRANSFER,kind='transfer') for h in world.households() if h['employer'] is None]
        rows += [dict(id=h['id'],due_cents=h['due_cents'],kind='short_time') for h in world.crisis.benefits(world) if h['due_cents']]
        total=sum(r['due_cents'] for r in rows)
        world.treasury.ensure_cash(world,total+world.treasury.overdue_interest_cents)
        budget=min(total,max(0,world.nodes['staat']['cash_cents']-world.treasury.overdue_interest_cents))
        paid=[budget*r['due_cents']//total for r in rows] if total else []
        ranking=sorted(range(len(rows)),key=lambda i:(-(budget*rows[i]['due_cents']%total),rows[i]['id'],rows[i]['kind'])) if total else []
        for i in ranking[:budget-sum(paid)]:paid[i]+=1
        for r,amount in zip(rows,paid):
            h=world.nodes[r['id']]
            actual=world.pay('staat',r['id'],amount,r['kind'],'Kurzarbeitsleistung' if r['kind']=='short_time' else 'Transfer')
            h['metrics']['income']+=actual;h['metrics']['transfers']+=actual
            if r['kind']=='short_time':
                h['metrics']['short_time']+=actual
                if actual<r['due_cents']:
                    world.obligations.append(dict(month=world.month,source='staat',target=r['id'],amount_cents=r['due_cents']-actual,kind='short_time'))
        if budget<total:world.notice(f'Sozialbudget: {((total-budget)/100):.2f} € des Referenzbedarfs nicht finanziert; Zahlungen anteilig statt nach Haushaltsreihenfolge. Kurzarbeitsansprüche bleiben als offene Verpflichtung erfasst.','staat')
        self.settle_wage_arrears(world)

    def settle_wage_arrears(self,world):
        # Existing claims remain claims. Repayment uses cash after current social payments.
        envelope=max(0,world.nodes['staat']['cash_cents']-world.treasury.overdue_interest_cents)
        for o in world.obligations:
            if not envelope:break
            if o['source']!='staat' or o['kind']!='wage':continue
            paid=world.pay('staat',o['target'],min(envelope,o['amount_cents']),'public_wage_arrears','Nachzahlung öffentlicher Löhne')
            o['amount_cents']-=paid;envelope-=paid
            h=world.nodes[o['target']];h['metrics']['income']+=paid
            tax=max(0,world.household_outputs(h)['tax_due']-h['metrics']['tax'])
            h['metrics']['tax']+=world.pay(h['id'],'staat',tax,'arrears_income_tax','Steuer auf Lohnnachzahlung')
        world.obligations=[o for o in world.obligations if o['amount_cents']]

    def amounts(self,world):
        tx=[t for t in world.journal if t['month']==world.month]
        total=lambda kinds,source=None,target=None:sum(t['amount_cents'] for t in tx if t['kind'] in kinds and (source is None or t['source']==source) and (target is None or t['target']==target))
        recurring=total(('income_tax','profit_tax','distribution_tax'),target='staat')
        social=total(('transfer','short_time'),source='staat')
        current_interest=world.treasury.month_interest_charge_cents
        committed=self.plan['payroll_cents']+self.plan['social_need_cents']+self.plan['procurement_cents']+current_interest
        return dict(recurring_taxes_cents=recurring,committed_spending_cents=committed,commitment_balance_cents=recurring-committed,
                    wages_paid_cents=total(('wage',),source='staat'),social_paid_cents=social,
                    social_unfunded_cents=max(0,self.plan['social_need_cents']-social),procurement_paid_cents=total(('procurement',),source='staat'),
                    wage_arrears_paid_cents=total(('public_wage_arrears',),source='staat'),
                    new_wage_arrears_cents=sum(o['amount_cents'] for o in world.obligations if o['source']=='staat' and o['kind']=='wage' and o['month']==world.month))

    def review(self,world):
        if self.last_review==world.month:return
        self.last_review=world.month
        a=self.amounts(world);balance=a['commitment_balance_cents']
        self.revenues.append(a['recurring_taxes_cents'])
        self.deficit_streak=self.deficit_streak+1 if balance<0 else 0
        self.surplus_streak=self.surplus_streak+1 if balance>0 else 0
        self.next_target_staff=self.target_staff;self.next_procurement_bps=self.procurement_bps
        self.decision='funding_cut' if self.plan['hard_funding_cut'] else 'hold'
        self.reason='Finanzierungsgrenze vor Arbeitsbeginn: Beschaffung ausgesetzt und nur vollständig finanzierte öffentliche Stellen genehmigt.' if self.plan['hard_funding_cut'] else 'Keine Änderung der Ausgabenregel für den Folgemonat.'
        self.effective_month=world.month if self.plan['hard_funding_cut'] else world.month+1
        if self.policy=='legacy':
            self.reason='Referenzregel: keine strukturelle Budgetanpassung; bisherige Ausgabenversprechen bleiben bestehen.'
            return
        if self.deficit_streak>=3:
            if self.procurement_bps:
                self.next_procurement_bps=max(0,self.procurement_bps-2500);self.decision='cut_procurement'
                self.reason='Drei Defizitabschlüsse gemessen am geplanten laufenden Bedarf: Beschaffungsquote sinkt ab Folgemonat um 25 Prozentpunkte.'
            elif self.target_staff:
                self.next_target_staff=self.target_staff-1;self.decision='cut_staff'
                self.reason='Drei weitere Defizitabschlüsse bei ausgesetzter Beschaffung: eine öffentliche Stelle entfällt ab Folgemonat.'
            else:
                self.reason='Keine weitere Kürzung von Beschaffung oder Stellen möglich. Ein verbleibender Sozial- oder Zinsbedarf bleibt als Finanzierungslücke sichtbar.'
            if self.decision in ('cut_staff','cut_procurement'):self.deficit_streak=0;self.effective_month=world.month+1
        elif self.surplus_streak>=3:
            candidates=[]
            if self.target_staff<2 and any(h['employer'] is None for h in world.households()):candidates.append((self.target_staff+1,self.procurement_bps,'restore_staff'))
            if self.procurement_bps<10000:candidates.append((self.target_staff,self.procurement_bps+2500,'restore_procurement'))
            mean=sum(self.revenues[-3:])//len(self.revenues[-3:])
            arrears=any(o['source']=='staat' and o['kind']=='wage' for o in world.obligations) or world.treasury.overdue_interest_cents>0
            for desired,proc,decision in candidates:
                payroll=desired*WAGE
                social=self.social_need(world,desired)
                cost=payroll+social+2*(PROCUREMENT*proc//10000)+world.treasury.month_interest_charge_cents
                if not arrears and mean>=cost and world.nodes['staat']['cash_cents']>=cost+payroll:
                    self.next_target_staff=desired;self.next_procurement_bps=proc;self.decision=decision;self.surplus_streak=0
                    self.reason='Drei positive Abschlüsse, wiederkehrende Steuern decken den erweiterten Plan und Kasse deckt Plan plus zusätzliche Lohnrunde: vorsichtiger Wiederaufbau ab Folgemonat.'
                    self.effective_month=world.month+1;break
        if self.decision not in ('hold','funding_cut'):world.notice(self.reason,'staat')

    def monthly(self,world):
        return dict(**deepcopy(self.plan),**self.amounts(world),policy=self.policy,next_target_staff=self.next_target_staff,
                    next_procurement_bps=self.next_procurement_bps,deficit_streak=self.deficit_streak,surplus_streak=self.surplus_streak,
                    mean_recurring_taxes_cents=sum(self.revenues[-3:])//len(self.revenues[-3:]) if self.revenues else 0,
                    decision=self.decision,decision_reason=self.reason,decision_effective_month=self.effective_month)

    def record(self,world):
        self.history.append(self.monthly(world))

    def check(self,world):
        if self.policy=='adaptive' and world.phase>=0 and self.plan['month']==world.month:
            assert world.nodes['staat']['metrics']['wages']==self.plan['payroll_cents']
            assert self.plan['payroll_cents']==self.plan['approved_staff']*WAGE
            assert not any(o['source']=='staat' and o['kind']=='wage' and o['month']==world.month for o in world.obligations)

    def snapshot(self,world):
        return dict(policy=self.policy,monthly=self.monthly(world),history=deepcopy(self.history[-36:]))
