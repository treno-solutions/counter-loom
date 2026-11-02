"""Illustrative state cash-deficit financing through one commercial bank.
Contract, policy and bounds: FISCAL_MODEL.md. All money in integer cents.
"""
from copy import deepcopy
from systems import GovernmentSystem

PRIMARY = ('wage','transfer','procurement')
TAXES = ('income_tax','profit_tax')
KINDS = ('government_credit','government_interest','government_principal')

class Treasury:
    def __init__(self,world,credit_limit_cents=5000000,annual_rate_bps=300,reserve_months=1):
        if any(type(v) is not int or v<0 for v in (credit_limit_cents,annual_rate_bps)):
            raise ValueError('Staatskreditparameter müssen nichtnegative ganze Zahlen sein.')
        if type(reserve_months) is not int or not 0<=reserve_months<=6:
            raise ValueError('Reserve muss zwischen null und sechs ganzen Ausgabenmonaten liegen.')
        self.reserve_months=reserve_months
        self.planned_primary_cents=0
        self.reserve_target_cents=0
        self.policy_cash_before_cents=None
        self.policy_credit_need_cents=0
        self.policy_repayment_capacity_cents=0
        self.decision='pending'
        self.decision_reason='Die Finanzierung wird nach den Unternehmenssteuern beim Monatsabschluss entschieden.'
        self.credit_limit_cents=credit_limit_cents
        self.annual_rate_bps=annual_rate_bps
        self.spread_bps=annual_rate_bps-world.monetary.initial_rate_bps
        self.tranches=[]
        self.month_interest_basis=[]
        self.outstanding_cents=0
        self.credit_created_cents=0
        self.principal_repaid_cents=0
        self.interest_charged_cents=0
        self.interest_paid_cents=0
        self.overdue_interest_cents=0
        self.last_service_month=0
        self.last_close_month=0
        self.history=[]
        self.opening_principal_cents=0
        self.opening_interest_arrears_cents=0
        self.month_interest_charge_cents=0
        self.unfunded_financing_cents=0
        self.message='Vorhandene Kasse finanziert Ausgaben. Kredit schützt bei Bedarf eine begrenzte Liquiditätsreserve.'
        self.plan_reserve(world)

    def plan_reserve(self,world):
        self.planned_primary_cents=(len(world.nodes['staat']['employees'])*GovernmentSystem.wage_per_job
            +sum(h['employer'] is None for h in world.households())*GovernmentSystem.transfer_per_unemployed
            +2*GovernmentSystem.procurement_per_firm)
        self.reserve_target_cents=self.reserve_months*(self.planned_primary_cents+self.month_interest_charge_cents)

    def begin_month(self,world):
        self.opening_principal_cents=self.outstanding_cents
        self.opening_interest_arrears_cents=self.overdue_interest_cents
        basis=[dict(tranche_id=t['tranche_id'],principal_cents=t['outstanding_cents'],annual_rate_bps=t['annual_rate_bps'],interest_cents=t['outstanding_cents']*t['annual_rate_bps']//120000) for t in self.tranches if t['outstanding_cents']]
        self.month_interest_charge_cents=sum(x['principal_cents']*x['annual_rate_bps'] for x in basis)//120000
        remainder=self.month_interest_charge_cents-sum(x['interest_cents'] for x in basis)
        ranking=sorted(basis,key=lambda x:(-(x['principal_cents']*x['annual_rate_bps']%120000),x['tranche_id']))
        for item in ranking[:remainder]:item['interest_cents']+=1
        self.month_interest_basis=basis
        self.unfunded_financing_cents=0
        self.policy_cash_before_cents=None
        self.policy_credit_need_cents=0
        self.policy_repayment_capacity_cents=0
        self.decision='pending'
        self.decision_reason='Die Finanzierung wird nach den Unternehmenssteuern beim Monatsabschluss entschieden.'
        self.plan_reserve(world)

    def issue(self,world,amount):
        if type(amount) is not int or amount<0:raise ValueError('Ungültiger Staatskreditbetrag.')
        paid=min(amount,max(0,self.credit_limit_cents-self.outstanding_cents)) if world.nodes['bank']['cash_cents']>0 else 0
        if not paid:return 0
        bank=world.nodes['bank'];state=world.nodes['staat'];before=world.banking.balance(world)
        source_before,target_before=bank['cash_cents'],state['cash_cents']
        state['cash_cents']+=paid
        state['government_loan_cents']+=paid
        bank['loan_assets']+=paid
        self.outstanding_cents+=paid
        self.tranches.append(dict(tranche_id=len(self.tranches)+1,transaction_id=len(world.journal)+1,issue_month=world.month,original_cents=paid,outstanding_cents=paid,annual_rate_bps=world.monetary.state_offer(world),policy_rate_at_issue_bps=world.monetary.rate_bps,spread_bps=self.spread_bps))
        self.credit_created_cents+=paid
        world.banking.created+=paid
        world.record('bank','staat',paid,'government_credit','Staatskredit gutgeschrieben',source_before,target_before,before,'loan_creation')
        world.notice(f'Staat nimmt {paid/100:.2f} € Kredit auf. Guthaben und Staatsschuld steigen gleich hoch; Zinsen ab Folgemonat.','staat')
        return paid

    def ensure_cash(self,world,amount):
        shortfall=max(0,amount-world.nodes['staat']['cash_cents'])
        if shortfall:
            self.issue(world,shortfall)

    def service(self,world):
        if self.last_service_month==world.month:return
        self.last_service_month=world.month
        self.interest_charged_cents+=self.month_interest_charge_cents
        self.overdue_interest_cents+=self.month_interest_charge_cents
        self.pay_interest(world)

    def pay_interest(self,world):
        paid=world.pay('staat','bank',self.overdue_interest_cents,'government_interest','Zinsen Staatskredit')
        self.overdue_interest_cents-=paid
        self.interest_paid_cents+=paid
        world.nodes['staat']['metrics']['interest']+=paid
        world.nodes['bank']['metrics']['interest']+=paid
        if self.overdue_interest_cents:
            world.notice(f'Staatszinsen: {self.overdue_interest_cents/100:.2f} € bleiben unbezahlt.','staat')

    def repay(self,world,amount):
        if type(amount) is not int or amount<0:raise ValueError('Ungültiger Tilgungsbetrag.')
        state=world.nodes['staat'];bank=world.nodes['bank']
        paid=min(amount,self.outstanding_cents,state['cash_cents'])
        if not paid:return 0
        before=world.banking.balance(world);source_before,target_before=state['cash_cents'],bank['cash_cents']
        state['cash_cents']-=paid
        state['government_loan_cents']-=paid
        bank['loan_assets']-=paid
        remaining=paid
        for tranche in self.tranches:
            take=min(remaining,tranche['outstanding_cents']);tranche['outstanding_cents']-=take;remaining-=take
        self.outstanding_cents-=paid
        self.principal_repaid_cents+=paid
        world.banking.repaid+=paid
        world.record('staat','bank',paid,'government_principal','Tilgung Staatskredit',source_before,target_before,before,'principal_repayment')
        world.notice(f'Staat tilgt {paid/100:.2f} € Kredit. Schuld und Bankforderung sinken.','staat')
        return paid

    def monthly(self,world):
        tx=[t for t in world.journal if t['month']==world.month]
        taxes=sum(t['amount_cents'] for t in tx if t['target']=='staat' and t['kind'] in TAXES)
        primary=sum(t['amount_cents'] for t in tx if t['source']=='staat' and t['kind'] in PRIMARY)
        interest=sum(t['amount_cents'] for t in tx if t['kind']=='government_interest')
        credit=sum(t['amount_cents'] for t in tx if t['kind']=='government_credit')
        repaid=sum(t['amount_cents'] for t in tx if t['kind']=='government_principal')
        return dict(month=world.month,taxes_cents=taxes,primary_spending_cents=primary,
            public_wage_arrears_cents=sum(o['amount_cents'] for o in world.obligations if o['source']=='staat' and o['kind']=='wage'),
            budget_balance_cents=taxes-primary-interest,planned_primary_cents=self.planned_primary_cents,
            reserve_target_cents=self.reserve_target_cents,
            reserve_draw_cents=max(0,world.month_open['staat']-world.nodes['staat']['cash_cents']),
            reserve_build_cents=max(0,world.nodes['staat']['cash_cents']-world.month_open['staat']),
            policy_cash_before_cents=world.nodes['staat']['cash_cents'] if self.policy_cash_before_cents is None else self.policy_cash_before_cents,
            policy_credit_need_cents=self.policy_credit_need_cents,policy_repayment_capacity_cents=self.policy_repayment_capacity_cents,
            decision=self.decision,decision_reason=self.decision_reason,
            interest_due_cents=self.opening_interest_arrears_cents+self.month_interest_charge_cents,
            interest_paid_cents=interest,cash_deficit_cents=primary+interest-taxes,
            credit_cents=credit,principal_repaid_cents=repaid,opening_cash_cents=world.month_open['staat'],
            closing_cash_cents=world.nodes['staat']['cash_cents'],opening_principal_cents=self.opening_principal_cents,
            closing_principal_cents=self.outstanding_cents,unfunded_financing_cents=self.unfunded_financing_cents,interest_basis=deepcopy(self.month_interest_basis),new_interest_charge_cents=self.month_interest_charge_cents)

    def close(self,world):
        if self.last_close_month==world.month:return
        self.last_close_month=world.month
        if self.overdue_interest_cents:self.pay_interest(world)
        cash=world.nodes['staat']['cash_cents']
        self.policy_cash_before_cents=cash
        self.policy_credit_need_cents=max(0,self.reserve_target_cents-cash)
        self.policy_repayment_capacity_cents=max(0,cash-self.reserve_target_cents)
        if self.policy_credit_need_cents:
            funded=self.issue(world,self.policy_credit_need_cents)
            self.unfunded_financing_cents=self.policy_credit_need_cents-funded
            if self.unfunded_financing_cents:
                self.decision='limited'
                self.decision_reason='Reserveziel nicht erreicht: Kreditrahmen oder Bankkapital begrenzt die Aufnahme. Verfügbares Guthaben bleibt für Zahlungen nutzbar.'
            else:
                self.decision='borrow'
                self.decision_reason='Kasse liegt unter dem Reserveziel. Ein Bankkredit füllt die fehlende Liquidität auf; Staatsschuld und Bankforderung steigen gleich hoch.'
        elif self.policy_repayment_capacity_cents and self.outstanding_cents:
            self.repay(world,self.policy_repayment_capacity_cents)
            self.decision='repay'
            self.decision_reason='Kasse liegt über dem Reserveziel. Der darüber verfügbare Betrag tilgt bestehende Schuld, höchstens bis zur vollständigen Rückzahlung.'
        else:
            self.decision='hold'
            self.decision_reason='Keine zusätzliche Kreditaufnahme oder Tilgung beim Abschluss: Reserveziel gedeckt oder keine Schuld vorhanden. Vorhandenes Guthaben bleibt in der Kasse.'
        self.message=self.decision_reason
        if self.unfunded_financing_cents:
            world.notice(f'Staat: {self.unfunded_financing_cents/100:.2f} € fehlen zum Liquiditätsreserveziel.','staat')
        self.history.append(self.monthly(world))

    def check(self,world):
        assert sum(t['outstanding_cents'] for t in self.tranches)==self.outstanding_cents
        assert all(0<=t['outstanding_cents']<=t['original_cents'] for t in self.tranches)
        assert sum(x['interest_cents'] for x in self.month_interest_basis)==self.month_interest_charge_cents
        assert 0<=self.outstanding_cents<=self.credit_limit_cents
        assert world.nodes['staat']['government_loan_cents']==self.outstanding_cents
        assert self.outstanding_cents==self.credit_created_cents-self.principal_repaid_cents
        assert self.overdue_interest_cents==self.interest_charged_cents-self.interest_paid_cents>=0

    def snapshot(self,world):
        return dict(financing_policy='liquidity_buffer',reserve_months=self.reserve_months,credit_limit_cents=self.credit_limit_cents,annual_rate_bps=world.monetary.state_offer(world),spread_bps=self.spread_bps,tranches=deepcopy(self.tranches),weighted_rate_bps=sum(t['outstanding_cents']*t['annual_rate_bps'] for t in self.tranches)//self.outstanding_cents if self.outstanding_cents else None,
            outstanding_cents=self.outstanding_cents,remaining_credit_cents=self.credit_limit_cents-self.outstanding_cents,
            credit_created_cents=self.credit_created_cents,principal_repaid_cents=self.principal_repaid_cents,
            interest_charged_cents=self.interest_charged_cents,interest_paid_cents=self.interest_paid_cents,
            overdue_interest_cents=self.overdue_interest_cents,message=self.message,
            monthly=self.monthly(world),history=deepcopy(self.history),events=deepcopy([t for t in world.journal if t['kind'] in KINDS]))
