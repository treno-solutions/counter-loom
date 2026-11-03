"""Bounded mandated closure and illustrative net-income replacement, not law."""
from copy import deepcopy

FIRMS = ('alltag', 'werkstatt')
STANDBY_COST = 30000  # Energy/maintenance service paid to the existing foreign account.

class Closure:
    def __init__(self):
        self.pending = None
        self.episodes = []

    def queue(self, world, firm, duration, replacement_bps):
        if firm not in (*FIRMS, 'both') or type(duration) is not int or not 1 <= duration <= 12 or type(replacement_bps) is not int or not 0 <= replacement_bps <= 10000:
            raise ValueError('Betrieb, Dauer (1–12 Monate) oder Ersatzquote (0–100 %) ungültig.')
        if self.pending or any(self.closed(world, f) for f in FIRMS):
            raise ValueError('Eine Schliessung ist bereits vorgemerkt oder aktiv.')
        if world.horizon_months is not None and world.month >= world.horizon_months:
            raise ValueError('Der Beobachtungszeitraum ist abgeschlossen.')
        self.pending = dict(firm=firm, duration=duration, replacement_bps=replacement_bps)
        world.revision += 1
        return world.snapshot()

    def closed(self, world, firm):
        return any(firm in e['firms'] and e['start_month'] <= world.month <= e['end_month'] for e in self.episodes)

    def begin_month(self, world):
        for e in self.episodes:
            if world.month == e['end_month'] + 1:
                world.notice('Befristete Schliessung beendet. Die erhaltenen Verträge und der vorherige Arbeitszeitplan werden wieder freigegeben; Absatz und Liquidität begrenzen den weiteren Betrieb.')
        if not self.pending:
            return
        p = self.pending
        firms = list(FIRMS) if p['firm'] == 'both' else [p['firm']]
        workers = []
        for f in firms:
            n = world.nodes[f]
            gross = 240000 * n['company']['work_bps'] // 10000
            for worker in n['employees']:
                workers.append(dict(id=worker, employer=f, reference_net_cents=gross-gross*30//100))
        e = dict(firms=firms, start_month=world.month, end_month=world.month+p['duration']-1,
                 replacement_bps=p['replacement_bps'], workers=workers)
        self.episodes.append(e)
        self.pending = None
        world.notice(f'Befristete Schliessung: {", ".join(world.nodes[f]["name"] for f in firms)}, Monat {e["start_month"]}–{e["end_month"]}. Produktion und Verkäufe ruhen; Verträge bleiben erhalten. Ersatzquote {e["replacement_bps"]/100:g} % des Referenz-Nettoeinkommens.')

    def benefits(self, world):
        return [dict(**h, due_cents=h['reference_net_cents']*e['replacement_bps']//10000)
                for e in self.episodes if e['start_month'] <= world.month <= e['end_month'] for h in e['workers']]

    def planned_benefits(self, world):
        return sum(h['due_cents'] for h in self.benefits(world))

    def pay_benefits(self, world):
        for row in self.benefits(world):
            h = world.nodes[row['id']]
            paid = world.pay('staat', h['id'], row['due_cents'], 'short_time', 'Kurzarbeitsleistung', True)
            h['metrics']['income'] += paid
            h['metrics']['transfers'] += paid
            h['metrics']['short_time'] += paid

    def snapshot(self, world):
        return dict(pending=deepcopy(self.pending), episodes=deepcopy(self.episodes),
                    closed_firms=[f for f in FIRMS if self.closed(world, f)], standby_cost_cents=STANDBY_COST,
                    monthly_due_cents=self.planned_benefits(world),
                    monthly_paid_cents=sum(h['metrics']['short_time'] for h in world.households()),
                    unpaid_cents=sum(o['amount_cents'] for o in world.obligations if o['kind']=='short_time'))


def compare(world, firm, duration, replacement_bps):
    """Two isolated continuations of exactly the same confirmed world state."""
    results = []
    for rate in (0, replacement_bps):
        clone = deepcopy(world)
        clone.horizon_months = None
        clone.crisis.queue(clone, firm, duration, rate)
        start = clone.month + 1
        end = start + duration + 5
        rows = []
        journal_start = len(clone.journal)
        while clone.month < end or clone.phase != 4:
            clone.step()
            if clone.phase == 4 and clone.month >= start:
                h = clone.history[-1]
                rows.append(dict(month=clone.month, closed=bool(clone.crisis.snapshot(clone)['closed_firms']),
                    household_net_cents=sum(x['income_cents']-x['tax_cents'] for x in h['households']),
                    household_cash_cents=h['household_cash_cents'], consumption_cents=h['consumption_cents'],
                    firm_cash_cents=sum(clone.nodes[f]['cash_cents'] for f in FIRMS),
                    production_units=sum(clone.nodes[f]['metrics']['produced_units'] for f in FIRMS),
                    employment=h['employment'], government_cash_cents=h['government_cash_cents'],
                    government_debt_cents=clone.treasury.outstanding_cents,
                    short_time_cents=clone.crisis.snapshot(clone)['monthly_paid_cents']))
        results.append(dict(replacement_bps=rate, rows=rows,
            total_short_time_cents=sum(t['amount_cents'] for t in clone.journal[journal_start:] if t['kind']=='short_time')))
    return dict(source_world_id=world.id, source_revision=world.revision, start_month=start,
                end_month=end, duration=duration, firm=firm, replacement_bps=replacement_bps, branches=results)
