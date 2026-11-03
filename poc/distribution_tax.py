"""Illustrative withholding on actual owner distributions; all amounts in cents."""
from copy import deepcopy
from systems import FinanceSystem

KINDS=('company_dividend','company_extra_dividend','dividend')
class DistributionTax:
    def __init__(self,rate_bps=2500):
        if type(rate_bps) is not int or not 0<=rate_bps<=5000:
            raise ValueError('Ausschüttungssteuer muss zwischen 0 und 5000 ganzen Basispunkten liegen.')
        self.rate_bps=rate_bps
        self.receipts=[]
        self.history=[]

    def pay(self,world,source,h,amount,kind,label):
        assert kind in KINDS
        gross=world.pay(source,h['id'],amount,kind,label)
        if not gross:return 0
        gross_id=world.journal[-1]['id']
        m=h['metrics']
        tax=(m['distribution_gross']+gross)*self.rate_bps//10000-m['distribution_tax']
        paid=world.pay(h['id'],'staat',tax,'distribution_tax','Einbehaltene Ausschüttungssteuer')
        assert paid==tax
        net=gross-tax
        m['distribution_gross']+=gross;m['distribution_tax']+=tax;m['distribution_net']+=net
        h['dividend_carry']+=net
        self.receipts.append(dict(month=world.month,source=source,recipient=h['id'],kind=kind,
            gross_cents=gross,tax_cents=tax,net_cents=net,gross_transaction_id=gross_id,
            tax_transaction_id=world.journal[-1]['id'] if tax else None))
        return gross

    def settle_bank(self,world):
        # Tax from bank payouts can fund overdue state interest. Settle the real
        # cash feedback before reviewing the budget and recording fiscal history.
        while True:
            if world.treasury.overdue_interest_cents:world.treasury.pay_interest(world)
            tx=[t for t in world.journal if t['month']==world.month]
            earned=sum(t['amount_cents'] for t in tx if t['target']=='bank' and t['kind'] in ('interest','machine_interest','government_interest'))
            distributed=sum(t['amount_cents'] for t in tx if t['source']=='bank' and t['kind']=='dividend')
            gross=min(max(0,earned-distributed),world.nodes['bank']['cash_cents'])
            if not gross:break
            tax_before=sum(h['metrics']['distribution_tax'] for h in world.households())
            for h,share in zip(world.households(),FinanceSystem.dividends(gross,6)):
                self.pay(world,'bank',h,share,'dividend','Zinsausschüttung')
            tax_after=sum(h['metrics']['distribution_tax'] for h in world.households())
            if tax_after==tax_before or not world.treasury.overdue_interest_cents:break

    def monthly(self,world):
        rows=[r for r in self.receipts if r['month']==world.month]
        def totals(items):return {f'{k}_cents':sum(r[f'{k}_cents'] for r in items) for k in ('gross','tax','net')}
        return dict(month=world.month,state_taxes={kind:sum(t['amount_cents'] for t in world.journal if t['month']==world.month and t['target']=='staat' and t['kind']==kind) for kind in ('income_tax','arrears_income_tax','profit_tax','distribution_tax')},**totals(rows),households=[dict(id=h['id'],**totals([r for r in rows if r['recipient']==h['id']])) for h in world.households()],sources=[dict(id=source,**totals([r for r in rows if r['source']==source])) for source in ('alltag','werkstatt','bank')])

    def snapshot(self,world):
        return dict(rate_bps=self.rate_bps,monthly=self.monthly(world),history=deepcopy(self.history[-36:]))
