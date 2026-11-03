"""One-bank balance sheet and one explicit machine-credit contract.
Customer deposits and bank equity are distinct; see BANKING_MODEL.md.
"""
from dataclasses import asdict, dataclass


@dataclass
class MachineLoan:
    status: str = 'available'
    amount_cents: int = 120000
    outstanding_cents: int = 0
    annual_rate_bps: int = 600
    policy_rate_at_issue_bps: int | None = None
    spread_bps: int = 400
    monthly_principal_cents: int = 10000
    term_months: int = 12
    borrower: str = 'alltag'
    supplier: str = 'werkstatt'
    units: int = 8
    issue_month: int | None = None
    delivery_month: int | None = None
    last_service_month: int | None = None
    principal_paid_cents: int = 0
    interest_paid_cents: int = 0
    interest_charged_cents: int = 0
    overdue_interest_cents: int = 0
    overdue_principal_cents: int = 0
    message: str = 'Ein begrenzter Maschinenkredit kann angefragt werden.'


class Banking:
    def __init__(self, world):
        self.initial_deposits = sum(n['cash_cents'] for n in world.nodes.values() if n['sector'] != 'bank')
        self.reserves = self.initial_deposits + world.nodes['bank']['cash_cents'] - world.nodes['bank']['loan_assets']
        self.created = 0
        self.repaid = 0
        self.interest_received = 0
        self.distributed = 0
        self.loan = MachineLoan(units=8*world.goods_unit_scale)

    def balance(self, world):
        deposits = sum(n['cash_cents'] for n in world.nodes.values() if n['sector'] != 'bank')
        loans = world.nodes['bank']['loan_assets']
        equity = world.nodes['bank']['cash_cents']
        return dict(reserves_cents=self.reserves, loan_assets_cents=loans, customer_deposits_cents=deposits, equity_cents=equity,
                    assets_cents=self.reserves + loans, liabilities_and_equity_cents=deposits + equity)

    def request(self, world):
        if world.horizon_months is not None and world.month>=world.horizon_months and world.phase>=3:
            raise ValueError('Die letzte Investitionsphase dieses Lernlaufs ist vorbei. Bitte neu starten.')
        if self.loan.status != 'available':
            raise ValueError('Für diesen Lauf wurde bereits ein Maschinenkredit angefragt.')
        self.loan.status = 'requested'
        self.loan.message = 'Anfrage vorgemerkt. Die nächste Investitionsphase prüft Betrieb und verfügbare Maschine.'
        world.revision += 1
        world.notice('Maschinenkredit angefragt: Prüfung und mögliche Gutschrift in der nächsten Investitionsphase.', 'bank')
        return world.snapshot()

    def originate(self, world):
        loan = self.loan
        if loan.status != 'requested':
            return False
        borrower, supplier = world.nodes[loan.borrower], world.nodes[loan.supplier]
        if world.crisis.closed(world,loan.borrower) or world.crisis.closed(world,loan.supplier):
            loan.message='Maschinenvertrag wartet bis zur Wiederöffnung; reservierte Ware bleibt erhalten.'
            return True
        if world.nodes['bank']['cash_cents'] <= 0 or not borrower['employees']:
            loan.message = 'Anfrage wartet: positives Bankkapital und ein Betrieb mit Beschäftigten sind Voraussetzung.'
            return True
        if supplier['inventory'] - supplier.get('reserved_units', 0) < loan.units:
            loan.message = f'Anfrage wartet auf {loan.units} verfügbare Werkstatteinheiten für die Maschine.'
            return True
        loan.amount_cents=loan.units*supplier['price']
        loan.monthly_principal_cents=(loan.amount_cents+loan.term_months-1)//loan.term_months
        loan.annual_rate_bps=world.monetary.machine_offer()
        loan.policy_rate_at_issue_bps=world.monetary.rate_bps
        before = self.balance(world)
        source_before = world.nodes['bank']['cash_cents']
        target_before = borrower['cash_cents']
        borrower['cash_cents'] += loan.amount_cents
        borrower['machine_loan_cents'] = loan.amount_cents
        world.nodes['bank']['loan_assets'] += loan.amount_cents
        self.created += loan.amount_cents
        loan.outstanding_cents = loan.amount_cents
        loan.issue_month = world.month
        loan.status = 'credited'
        loan.message = 'Kreditguthaben und Kreditforderung sind gebucht. Die reservierte Maschine wird in der Abschlussphase geliefert.'
        supplier['reserved_units'] = supplier.get('reserved_units', 0) + loan.units
        world.record('bank', loan.borrower, loan.amount_cents, 'machine_credit', 'Maschinenkredit gutgeschrieben', source_before, target_before, before, 'loan_creation')
        world.notice(f'Die Bank schafft {loan.amount_cents/100:.2f} € Kreditguthaben und eine gleich hohe Forderung. Ihr Eigenkapital wird nicht ausgezahlt.', 'bank')
        return True

    def deliver(self, world):
        loan = self.loan
        if loan.status != 'credited':
            return
        borrower, supplier = world.nodes[loan.borrower], world.nodes[loan.supplier]
        if world.crisis.closed(world,loan.borrower) or world.crisis.closed(world,loan.supplier):
            loan.message='Maschinenlieferung wartet bis zur Wiederöffnung; Kredit und Reservierung bleiben bestehen.'
            return
        if borrower['cash_cents'] < loan.amount_cents or supplier['inventory'] < loan.units:
            loan.message = 'Lieferung wartet auf Zahlungsmittel beziehungsweise reservierte Ware.'
            return
        supplier['reserved_units'] -= loan.units
        units = world.buy(loan.borrower, loan.supplier, loan.amount_cents, 'machine_purchase', unit_price_cents=loan.amount_cents//loan.units)
        if units != loan.units:
            raise RuntimeError('Reservierte Maschinenlieferung stimmt nicht mit dem Vertrag überein.')
        borrower['capital'] += 1
        borrower['metrics']['investment'] += loan.amount_cents
        loan.delivery_month = world.month
        loan.status = 'delivered'
        loan.message = 'Maschine bezahlt und geliefert. Ab nächstem Monat wirkt die Kapazität und beginnt der Schuldendienst.'
        world.notice(f'Kreditfinanzierte Maschine geliefert: {loan.amount_cents/100:.2f} € gehen an die Werkstatt, ab Folgemonat +{4*world.goods_unit_scale} Wareneinheiten Vollzeitkapazität, bei Teilzeit anteilig.', loan.borrower)

    def due(self,world,month=None):
        loan=self.loan
        month=world.month if month is None else month
        if loan.delivery_month is None or month<=loan.delivery_month or loan.status=='repaid' or loan.last_service_month==month:
            return dict(total_cents=0,interest_cents=0,principal_cents=0)
        interest=loan.overdue_interest_cents+loan.outstanding_cents*loan.annual_rate_bps//120000
        principal=max(0,min(loan.outstanding_cents,min(loan.term_months,month-loan.delivery_month)*loan.monthly_principal_cents-loan.principal_paid_cents))
        return dict(total_cents=interest+principal,interest_cents=interest,principal_cents=principal)

    def service(self, world):
        loan = self.loan
        if loan.delivery_month is None or world.month <= loan.delivery_month or loan.status == 'repaid' or loan.last_service_month == world.month:
            return
        loan.last_service_month = world.month
        loan.status = 'repaying'
        charge = loan.outstanding_cents * loan.annual_rate_bps // 120000
        loan.interest_charged_cents += charge
        loan.overdue_interest_cents += charge
        paid_interest = world.pay(loan.borrower, 'bank', loan.overdue_interest_cents, 'machine_interest', 'Zinsen Maschinenkredit')
        loan.overdue_interest_cents -= paid_interest
        loan.interest_paid_cents += paid_interest
        world.nodes[loan.borrower]['metrics']['operating_costs'] += paid_interest
        world.nodes['bank']['metrics']['interest'] += paid_interest
        # Cumulative schedule avoids re-creating old unpaid instalments every month.
        due_instalments = min(loan.term_months, world.month - loan.delivery_month)
        due_principal = max(0, min(loan.outstanding_cents, due_instalments * loan.monthly_principal_cents - loan.principal_paid_cents))
        paid = min(due_principal, world.nodes[loan.borrower]['cash_cents'])
        if paid:
            before = self.balance(world)
            source_before, target_before = world.nodes[loan.borrower]['cash_cents'], world.nodes['bank']['cash_cents']
            world.nodes[loan.borrower]['cash_cents'] -= paid
            world.nodes[loan.borrower]['machine_loan_cents'] -= paid
            world.nodes['bank']['loan_assets'] -= paid
            loan.outstanding_cents -= paid
            loan.principal_paid_cents += paid
            self.repaid += paid
            world.record(loan.borrower, 'bank', paid, 'machine_principal', 'Tilgung Maschinenkredit', source_before, target_before, before, 'principal_repayment')
        loan.overdue_principal_cents = max(0, min(loan.amount_cents,due_instalments * loan.monthly_principal_cents) - loan.principal_paid_cents)
        if loan.overdue_interest_cents or loan.overdue_principal_cents:
            loan.message = 'Eine fällige Zahlung ist nicht vollständig gedeckt. Restschuld und Rückstände bleiben bestehen.'
            world.notice('Maschinenkredit: fällige Zinsen oder Tilgung sind nicht vollständig bezahlt.', loan.borrower)
        elif loan.outstanding_cents == 0:
            loan.status = 'repaid'
            loan.message = 'Maschinenkredit vollständig getilgt; keine weiteren Raten werden abgebucht.'
            world.notice('Der Maschinenkredit ist vollständig getilgt.', 'bank')
        else:
            loan.message = 'Die fälligen Zinsen und Tilgung wurden bezahlt. Die Restschuld ist gesunken.'

    def check(self, world):
        balance = self.balance(world)
        assert balance['assets_cents'] == balance['liabilities_and_equity_cents']
        expected = self.initial_deposits + self.created - self.repaid - self.interest_received + self.distributed
        assert balance['customer_deposits_cents'] == expected
        assert world.nodes['alltag'].get('machine_loan_cents', 0) == self.loan.outstanding_cents
        assert world.nodes['bank']['loan_assets'] == sum(world.nodes[f]['loan'] for f in ('alltag', 'werkstatt')) + self.loan.outstanding_cents + world.nodes['staat'].get('government_loan_cents',0)
        assert self.loan.principal_paid_cents + self.loan.outstanding_cents == (self.loan.amount_cents if self.loan.issue_month is not None else 0)

    def snapshot(self, world):
        events = [t for t in world.journal if t['kind'] in ('machine_credit', 'machine_purchase', 'machine_interest', 'machine_principal')]
        loan_data=asdict(self.loan)
        if self.loan.issue_month is None:
            loan_data['annual_rate_bps']=world.monetary.machine_offer()
            loan_data['amount_cents']=self.loan.units*world.nodes[self.loan.supplier]['price']
            loan_data['monthly_principal_cents']=(loan_data['amount_cents']+self.loan.term_months-1)//self.loan.term_months
        return dict(balance=self.balance(world), loan=loan_data, events=events, initial_deposits_cents=self.initial_deposits,
                    credit_created_cents=self.created, principal_repaid_cents=self.repaid, interest_received_cents=self.interest_received,
                    distributed_cents=self.distributed, expected_deposits_cents=self.initial_deposits+self.created-self.repaid-self.interest_received+self.distributed)
