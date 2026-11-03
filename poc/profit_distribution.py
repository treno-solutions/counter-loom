"""Illustrative retained earnings and quarterly surplus distribution; integer cents."""

POLICIES = ('legacy', 'surplus')

def allocation(opening_retained, after_tax, cash, operating_buffer, investment_buffer, allowed, month, policy):
    if policy not in POLICIES:raise ValueError('Unknown profit distribution policy.')
    # The reference branch retains the exact former cash constraint.
    investment_buffer = investment_buffer if policy == 'surplus' else 0
    protected = operating_buffer + investment_buffer
    free = max(0, cash-protected)
    pool = opening_retained + after_tax
    regular = min(max(0, after_tax)//2, free) if allowed else 0
    if policy == 'surplus':regular = min(regular, max(0, pool))
    quarterly = month % 3 == 0
    extra = min(max(0, pool-regular), free-regular) if allowed and quarterly and policy == 'surplus' else 0
    reason = ('Ausschüttung gesperrt: Schliessung, Rückstände oder kein regulär tragfähiger Folgeplan.' if not allowed else
              'Bisherige Regel: höchstens 50 % des positiven Monatsergebnisses; keine zusätzliche Ausschüttung.' if policy == 'legacy' else
              'Zusätzliche Ausschüttung erst beim Quartalsabschluss.' if not quarterly else
              'Quartalsprüfung: Gewinnvortrag und frei verfügbare Liquidität begrenzen die zusätzliche Ausschüttung.')
    return dict(month=month,opening_retained_cents=opening_retained,after_tax_cents=after_tax,
                regular_paid_cents=regular,extra_paid_cents=extra,total_paid_cents=regular+extra,
                closing_retained_cents=pool-regular-extra,eligible_profit_cents=max(0,pool),
                cash_before_cents=cash,operating_buffer_cents=operating_buffer,
                investment_buffer_cents=investment_buffer,protected_cash_cents=protected,
                free_cash_cents=free,quarter_due=quarterly,allowed=allowed,reason=reason)


def initial_allocation():
    result=allocation(0,0,0,0,0,False,1,'surplus')
    result['month']=0
    result['reason']='Gewinnverwendung wird beim ersten Monatsabschluss geprüft.'
    return result
