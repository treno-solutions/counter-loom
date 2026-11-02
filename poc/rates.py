"""Illustrative policy input and distinct credit-pricing rules; RATES_MODEL.md."""
from copy import deepcopy

class MonetaryPolicy:
    def __init__(self,world,initial_rate_bps=200):
        self.validate(initial_rate_bps)
        self.initial_rate_bps=initial_rate_bps
        self.rate_bps=initial_rate_bps
        self.pending_rate_bps=None
        self.changes=[]
        self.history=[]
        self.last_begin_month=0
        self.last_close_month=0
        self.machine_spread_bps=400
        self.fixed_corporate_rate_bps=200
        self.variable_spread_bps=0
        world.nodes['alltag']['loan_rate_bps']=initial_rate_bps
        world.nodes['alltag']['loan_next_rate_bps']=initial_rate_bps
        world.nodes['werkstatt']['loan_rate_bps']=self.fixed_corporate_rate_bps
        world.nodes['werkstatt']['loan_next_rate_bps']=self.fixed_corporate_rate_bps

    @staticmethod
    def validate(rate):
        if type(rate) is not int or not 0<=rate<=1000:
            raise ValueError('Leitzins muss zwischen 0 und 10 % in ganzen Basispunkten liegen.')

    def queue(self,world,rate):
        self.validate(rate)
        if world.month>=24:raise ValueError('Im letzten Monat kann keine weitere Leitzinsänderung vorgemerkt werden.')
        if rate==self.rate_bps:
            if self.pending_rate_bps is None:raise ValueError('Dieser Leitzins gilt bereits.')
            self.pending_rate_bps=None
            world.notice('Vorgemerkte Leitzinsänderung zurückgenommen.','bank')
        else:
            self.pending_rate_bps=rate
            world.notice(f'Leitzins {rate/100:.2f} % ab nächstem Monatsbeginn vorgemerkt.','bank')
        world.revision+=1
        return world.snapshot()

    def rate_for_month(self,month):
        value=self.initial_rate_bps
        for change in self.changes:
            if change['month']<=month:value=change['new_rate_bps']
        return value

    def machine_offer(self):return self.rate_bps+self.machine_spread_bps

    def state_offer(self,world):return max(0,self.rate_bps+world.treasury.spread_bps)

    def begin_month(self,world):
        if self.last_begin_month==world.month:return
        self.last_begin_month=world.month
        if self.pending_rate_bps is not None:
            previous=self.rate_bps;self.rate_bps=self.pending_rate_bps;self.pending_rate_bps=None
            self.changes.append(dict(month=world.month,old_rate_bps=previous,new_rate_bps=self.rate_bps))
            world.notice(f'Modell-Leitzins ab Monat {world.month}: {self.rate_bps/100:.2f} %. Neue Kredite erhalten die neuen Konditionen.','bank')
        firm=world.nodes['alltag'];before=firm['loan_rate_bps']
        firm['loan_rate_bps']=max(0,self.rate_for_month(world.month-1)+self.variable_spread_bps)
        firm['loan_next_rate_bps']=max(0,self.rate_for_month(world.month)+self.variable_spread_bps)
        if before!=firm['loan_rate_bps']:
            world.notice(f'Variabler Betriebskredit Alltag & Versorgung: Vertragszins ab Monat {world.month} {firm["loan_rate_bps"]/100:.2f} %.','alltag')

    def contracts(self,world):
        result=[]
        for key,binding,spread in [('alltag','variable',self.variable_spread_bps),('werkstatt','fixed',0)]:
            n=world.nodes[key]
            rate=n['loan_rate_bps']
            result.append(dict(borrower=key,binding=binding,principal_cents=n['loan'],annual_rate_bps=rate,
                spread_bps=spread,reference_lag_months=1 if binding=='variable' else 0,
                monthly_interest_due_cents=n['loan']*rate//120000,
                next_reset_month=world.month+1 if binding=='variable' else None,
                next_rate_bps=max(0,self.rate_for_month(world.month)+spread) if binding=='variable' else rate))
        return result

    def close(self,world):
        if self.last_close_month==world.month:return
        self.last_close_month=world.month
        self.history.append(dict(month=world.month,policy_rate_bps=self.rate_bps,
            variable_rate_bps=world.nodes['alltag']['loan_rate_bps'],fixed_rate_bps=world.nodes['werkstatt']['loan_rate_bps'],
            machine_offer_bps=self.machine_offer(),state_offer_bps=self.state_offer(world)))

    def check(self,world):
        assert 0<=self.rate_bps<=1000
        assert world.nodes['werkstatt']['loan_rate_bps']==self.fixed_corporate_rate_bps
        if world.month:assert world.nodes['alltag']['loan_rate_bps']==max(0,self.rate_for_month(world.month-1)+self.variable_spread_bps)

    def snapshot(self,world):
        return dict(initial_rate_bps=self.initial_rate_bps,rate_bps=self.rate_bps,pending_rate_bps=self.pending_rate_bps,
            pending_effective_month=world.month+1 if self.pending_rate_bps is not None else None,
            machine_spread_bps=self.machine_spread_bps,state_spread_bps=world.treasury.spread_bps,
            machine_offer_bps=self.machine_offer(),state_offer_bps=self.state_offer(world),
            contracts=self.contracts(world),changes=deepcopy(self.changes),history=deepcopy(self.history))
