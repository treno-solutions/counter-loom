"""Cash-basis bank profit, equal profit tax and bounded owner distributions."""
from copy import deepcopy
from systems import FinanceSystem


class BankProfit:
    def __init__(self, world, policy='consistent'):
        if policy not in ('consistent', 'legacy'):
            raise ValueError('Ungültige Bankgewinnregel.')
        self.policy = policy
        self.capital_floor = world.initial['bank']
        self.retained = 0
        self.history = []
        self.monthly = self.empty(0)

    def empty(self, month):
        return dict(month=month, interest_income_cents=0, operating_costs_cents=0,
            profit_before_tax_cents=0, profit_tax_due_cents=0, profit_tax_paid_cents=0,
            after_tax_cents=0, opening_retained_cents=self.retained, distribution_cents=0,
            regular_distribution_cents=0, extra_distribution_cents=0,
            retained_earnings_cents=self.retained, capital_floor_cents=self.capital_floor,
            closing_equity_cents=self.capital_floor, closed=False)

    def close(self, world):
        if self.monthly['month'] == world.month and self.monthly['closed']:
            return
        opening = self.retained
        if self.policy == 'legacy':
            world.distribution_tax.settle_bank_legacy(world)
        else:
            # State interest can be paid out of bank profit/withholding taxes.
            # Recompute cumulative entitlements, never tax or pay an amount twice.
            while True:
                before = len(world.journal)
                if world.treasury.overdue_interest_cents:
                    world.treasury.pay_interest(world)
                tx = [t for t in world.journal if t['month'] == world.month]
                earned = sum(t['amount_cents'] for t in tx if t['target']=='bank' and t['kind'] in ('interest','machine_interest','government_interest'))
                tax_paid = sum(t['amount_cents'] for t in tx if t['source']=='bank' and t['kind']=='profit_tax')
                due = earned*20//100
                world.pay('bank','staat',max(0,due-tax_paid),'profit_tax','Gewinnsteuer Bank',True)
                distributed = sum(t['amount_cents'] for t in tx if t['source']=='bank' and t['kind']=='dividend')
                after_tax = earned-due
                pool = max(0,opening+after_tax)
                entitlement = pool if world.month%3==0 else min(pool,after_tax//2)
                available = max(0,world.nodes['bank']['cash_cents']-self.capital_floor)
                additional = min(max(0,entitlement-distributed),available)
                for h,share in zip(world.households(),FinanceSystem.dividends(additional,6)):
                    world.distribution_tax.pay(world,'bank',h,share,'dividend','Bankgewinn ausgeschüttet')
                if len(world.journal)==before:
                    break
        tx = [t for t in world.journal if t['month']==world.month]
        earned = sum(t['amount_cents'] for t in tx if t['target']=='bank' and t['kind'] in ('interest','machine_interest','government_interest'))
        paid = sum(t['amount_cents'] for t in tx if t['source']=='bank' and t['kind']=='profit_tax')
        payout = sum(t['amount_cents'] for t in tx if t['source']=='bank' and t['kind']=='dividend')
        due = earned*20//100 if self.policy=='consistent' else 0
        after = earned-due
        self.retained = opening+after-payout
        regular = min(payout,max(0,after)//2) if self.policy=='consistent' else payout
        self.monthly = dict(self.empty(world.month), interest_income_cents=earned,
            profit_before_tax_cents=earned,profit_tax_due_cents=due,profit_tax_paid_cents=paid,
            after_tax_cents=after,opening_retained_cents=opening,distribution_cents=payout,
            regular_distribution_cents=regular,extra_distribution_cents=payout-regular,
            retained_earnings_cents=self.retained,closing_equity_cents=world.nodes['bank']['cash_cents'],closed=True)
        self.history.append(deepcopy(self.monthly))
        assert self.retained>=0
        if self.policy=='consistent':
            assert paid==due
            assert world.nodes['bank']['cash_cents']>=self.capital_floor

    def snapshot(self):
        return dict(policy=self.policy,profit_tax_bps=2000 if self.policy=='consistent' else 0,
            monthly=deepcopy(self.monthly),history=deepcopy(self.history[-36:]))
