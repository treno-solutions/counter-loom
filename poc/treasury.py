"""Illustrative state cash-deficit financing through one commercial bank.
Contract, policy and bounds: FISCAL_MODEL.md. All money in integer cents.
"""
from copy import deepcopy

PRIMARY = ('wage','transfer','procurement')
TAXES = ('income_tax','profit_tax')
KINDS = ('government_credit','government_interest','government_principal')

class Treasury:
    def __init__(self,world,credit_limit_cents=5000000,annual_rate_bps=300):
        if any(type(v) is not int or v<0 for v in (credit_limit_cents,annual_rate_bps)):
            raise ValueError('Staatskreditparameter müssen nichtnegative ganze Zahlen sein.')
        self.credit_limit_cents=credit_limit_cents
        self.annual_rate_bps=annual_rate_bps
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
        self.message='Monatliche Kassenfehlbeträge können durch einen begrenzten Staatskredit finanziert werden.'

    def begin_month(self,world):
        self.opening_principal_cents=self.outstanding_cents
        self.opening_interest_arrears_cents=self.overdue_interest_cents
        self.month_interest_charge_cents=self.opening_principal_cents*self.annual_rate_bps//120000
        self.unfunded_financing_cents=0

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
            interest_due_cents=self.opening_interest_arrears_cents+self.month_interest_charge_cents,
            interest_paid_cents=interest,cash_deficit_cents=primary+interest-taxes,
            credit_cents=credit,principal_repaid_cents=repaid,opening_cash_cents=world.month_open['staat'],
            closing_cash_cents=world.nodes['staat']['cash_cents'],opening_principal_cents=self.opening_principal_cents,
            closing_principal_cents=self.outstanding_cents,unfunded_financing_cents=self.unfunded_financing_cents)

    def close(self,world):
        if self.last_close_month==world.month:return
        self.last_close_month=world.month
        if self.overdue_interest_cents:self.pay_interest(world)
        m=self.monthly(world)
        adjustment=m['cash_deficit_cents']-m['credit_cents']+m['principal_repaid_cents']
        if adjustment>0:
            funded=self.issue(world,adjustment)
            self.unfunded_financing_cents=adjustment-funded
        elif adjustment<0:self.repay(world,-adjustment)
        if self.unfunded_financing_cents:
            self.message='Kreditgrenze oder Bankkapital begrenzt die Finanzierung. Der Staat nutzt seine Kassenreserve.'
            world.notice(f'Staat: {self.unfunded_financing_cents/100:.2f} € Kassenfehlbetrag nicht kreditfinanziert.','staat')
        elif self.outstanding_cents:
            self.message='Fehlbeträge werden innerhalb der Kreditgrenze finanziert; Überschüsse führen Schuld zurück. Zinsen folgen der Anfangsschuld.'
        else:self.message='Zurzeit keine Staatsschuld. Ein Überschuss bleibt nach vollständiger Tilgung auf dem Konto.'
        self.history.append(self.monthly(world))

    def check(self,world):
        assert 0<=self.outstanding_cents<=self.credit_limit_cents
        assert world.nodes['staat']['government_loan_cents']==self.outstanding_cents
        assert self.outstanding_cents==self.credit_created_cents-self.principal_repaid_cents
        assert self.overdue_interest_cents==self.interest_charged_cents-self.interest_paid_cents>=0

    def snapshot(self,world):
        return dict(credit_limit_cents=self.credit_limit_cents,annual_rate_bps=self.annual_rate_bps,
            outstanding_cents=self.outstanding_cents,remaining_credit_cents=self.credit_limit_cents-self.outstanding_cents,
            credit_created_cents=self.credit_created_cents,principal_repaid_cents=self.principal_repaid_cents,
            interest_charged_cents=self.interest_charged_cents,interest_paid_cents=self.interest_paid_cents,
            overdue_interest_cents=self.overdue_interest_cents,message=self.message,
            monthly=self.monthly(world),history=deepcopy(self.history),events=deepcopy([t for t in world.journal if t['kind'] in KINDS]))
