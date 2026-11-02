import { z } from 'zod';
const cents = z.number().int().nonnegative();
const signedCents = z.number().int();
export const Sector = z.enum(['households', 'firms', 'government', 'bank', 'external']);
export type SectorId = z.infer<typeof Sector>;
const Metric = z.object({ income: cents, tax: cents, sales: cents, operating_costs: cents, wages: cents, interest: cents, sold_units: cents, unmet_units: cents, produced_units: cents, investment: cents, transfers: cents, consumption_plan: cents, consumption_budget: cents, consumption_paid: cents, reserve_used: cents, unfunded_units: cents, production_plan: cents, cost_of_sales: cents, production_cost: cents, idle_cost: cents, interest_expense: cents, unpaid_wages: cents });
const CompanyPlan = z.object({ demand_units: cents, target_units: cents, opening_units: cents, opening_value_cents: cents, capacity_units: cents, needed_units: cents, production_units: cents, funded_units: cents, energy_unit_cents: cents, wages_due_cents: cents, interest_due_cents: cents, debt_service_cents: cents, staff: cents }).strict();
const CompanyResult = z.object({ funded_orders_units: cents, profit_before_tax_cents: signedCents, tax_due_cents: cents, tax_paid_cents: cents, after_tax_cents: signedCents, distribution_cents: cents, retained_result_cents: signedCents, reserve_cents: cents, desired_staff: cents, next_staff: cents, staff_reason: z.string(), distribution_reason: z.string() }).strict();
const Company = z.object({ forecast_milli: cents, inventory_value_cents: cents, staff_signal: signedCents, short_months: cents, last_investment_month: cents, plan: z.union([CompanyPlan,z.object({}).strict()]), result: z.union([CompanyResult,z.object({}).strict()]) }).strict();
export const NodeSchema = z.object({ id: z.string(), name: z.string(), sector: Sector, cash_cents: cents, metrics: Metric, employees: z.array(z.string()).optional(), employer: z.string().nullable().optional(), inventory: cents.optional(), capital: cents.optional(), loan: cents.optional(), loan_assets: cents.optional(), price: cents.optional(), productivity: cents.optional(), weak_months: cents.optional(), dividend_carry: cents.optional(), reserved_units: cents.optional(), machine_loan_cents: cents.optional(), company: Company.optional(), government_loan_cents: cents.optional(), loan_rate_bps: cents.optional(), loan_next_rate_bps: cents.optional() }).strict();
export type WorldNode = z.infer<typeof NodeSchema>;
const BalanceSchema = z.object({ reserves_cents: cents, loan_assets_cents: cents, customer_deposits_cents: cents, equity_cents: cents, assets_cents: cents, liabilities_and_equity_cents: cents }).strict();
const TransactionSchema = z.object({ id: z.number().int(), month: z.number().int(), phase: z.number().int().min(0).max(4), source: z.string(), target: z.string(), amount_cents: cents, kind: z.string(), label: z.string(), source_before: cents, source_after: cents, target_before: cents, target_after: cents, ledger_effect: z.enum(['transfer', 'bank_income', 'bank_distribution', 'loan_creation', 'principal_repayment']), deposit_delta_cents: signedCents, loan_delta_cents: signedCents, equity_delta_cents: signedCents, bank_before: BalanceSchema, bank_after: BalanceSchema }).strict();
export type Transaction = z.infer<typeof TransactionSchema>;
const LoanSchema = z.object({ status: z.enum(['available', 'requested', 'credited', 'delivered', 'repaying', 'repaid']), amount_cents: cents, outstanding_cents: cents, annual_rate_bps: cents, policy_rate_at_issue_bps: cents.nullable(), spread_bps: signedCents, monthly_principal_cents: cents, term_months: cents, borrower: z.string(), supplier: z.string(), units: cents, issue_month: cents.nullable(), delivery_month: cents.nullable(), last_service_month: cents.nullable(), principal_paid_cents: cents, interest_paid_cents: cents, interest_charged_cents: cents, overdue_interest_cents: cents, overdue_principal_cents: cents, message: z.string() }).strict();
const ForeignPlan = z.object({ month: cents, opening_cash_cents: cents, desired_cents: cents, budget_cents: cents, orders: z.array(z.object({seller:z.enum(['alltag','werkstatt']),desired_units:cents,desired_cents:cents,allocated_cents:cents,funded_units:cents}).strict()).length(2) }).strict();
const ExportDelivery = z.object({transaction_id:cents,month:cents,phase:z.literal(2),seller:z.enum(['alltag','werkstatt']),buyer:z.literal('ausland'),units:cents,unit_price_cents:cents,amount_cents:cents,cost_cents:cents,inventory_before:cents,inventory_after:cents}).strict();
const ForeignTrade = z.object({plan:ForeignPlan,deliveries:z.array(ExportDelivery),month_imports_cents:cents,month_exports_cents:cents,cumulative_imports_cents:cents,cumulative_exports_cents:cents,net_inflow_cents:signedCents,cumulative_net_inflow_cents:signedCents,domestic_cash_cents:cents,foreign_cash_cents:cents}).strict();
const FiscalMonth = z.object({month:cents,taxes_cents:cents,primary_spending_cents:cents,interest_due_cents:cents,interest_paid_cents:cents,cash_deficit_cents:signedCents,credit_cents:cents,principal_repaid_cents:cents,opening_cash_cents:cents,closing_cash_cents:cents,opening_principal_cents:cents,closing_principal_cents:cents,unfunded_financing_cents:cents,new_interest_charge_cents:cents,interest_basis:z.array(z.object({tranche_id:cents,principal_cents:cents,annual_rate_bps:cents,interest_cents:cents}).strict())}).strict();
const StateTranche=z.object({tranche_id:cents,transaction_id:cents,issue_month:cents,original_cents:cents,outstanding_cents:cents,annual_rate_bps:cents,policy_rate_at_issue_bps:cents,spread_bps:signedCents}).strict();
const PublicFinance = z.object({spread_bps:signedCents,tranches:z.array(StateTranche),weighted_rate_bps:cents.nullable(),credit_limit_cents:cents,annual_rate_bps:cents,outstanding_cents:cents,remaining_credit_cents:cents,credit_created_cents:cents,principal_repaid_cents:cents,interest_charged_cents:cents,interest_paid_cents:cents,overdue_interest_cents:cents,message:z.string(),monthly:FiscalMonth,history:z.array(FiscalMonth),events:z.array(TransactionSchema)}).strict();
const MonetaryPolicy=z.object({initial_rate_bps:cents,rate_bps:cents,pending_rate_bps:cents.nullable(),pending_effective_month:cents.nullable(),machine_spread_bps:signedCents,state_spread_bps:signedCents,machine_offer_bps:cents,state_offer_bps:cents,contracts:z.array(z.object({borrower:z.enum(['alltag','werkstatt']),binding:z.enum(['variable','fixed']),principal_cents:cents,annual_rate_bps:cents,spread_bps:signedCents,reference_lag_months:cents,monthly_interest_due_cents:cents,next_reset_month:cents.nullable(),next_rate_bps:cents}).strict()).length(2),changes:z.array(z.object({month:cents,old_rate_bps:cents,new_rate_bps:cents}).strict()),history:z.array(z.object({month:cents,policy_rate_bps:cents,variable_rate_bps:cents,fixed_rate_bps:cents,machine_offer_bps:cents,state_offer_bps:cents}).strict())}).strict();
export const WorldSchema = z.object({
  world_id: z.string(), revision: z.number().int(), month: z.number().int(), phase: z.number().int().min(-1).max(4), phase_label: z.string(), nodes: z.array(NodeSchema).length(11), transactions: z.array(TransactionSchema), notices: z.array(z.object({ month: z.number().int(), phase: z.number().int(), node: z.string(), text: z.string() })),
  history: z.array(z.object({ month: z.number().int(), consumption_cents: cents, employment: cents, household_cash_cents: cents, government_cash_cents: cents, cash_by_sector: z.record(Sector, cents) })), pending: z.array(z.string()), active: z.array(z.object({ event: z.string(), month: z.number().int() })), rules: z.record(Sector, z.string()),
  audit: z.object({ total_money_cents: cents, current_money_cents: cents, transaction_count: cents, open_obligations_cents: cents, loan_principal_cents: cents, llm_calls: z.literal(0) }), month_open: z.record(z.string(), cents), initial_balances: z.record(z.string(), cents), parameters: z.object({ energy_multiplier: z.number().int(), consumption_percent: z.number().int(), essential_budget_cents: cents }), classification: z.literal('illustrative_circular_flow_v7'), horizon_months: z.literal(24), completed: z.boolean(),
  foreign_trade: ForeignTrade, public_finance: PublicFinance, monetary_policy: MonetaryPolicy,
  banking: z.object({ balance: BalanceSchema, loan: LoanSchema, events: z.array(TransactionSchema), initial_deposits_cents: cents, credit_created_cents: cents, principal_repaid_cents: cents, interest_received_cents: cents, distributed_cents: cents, expected_deposits_cents: cents }).strict(),
}).strict().superRefine((w, c) => {
  const keys = new Set(w.nodes.map(n => n.id));
  const b = w.banking.balance;
  if (keys.size !== 11 || w.nodes.filter(n => n.sector !== 'bank').reduce((s, n) => s + n.cash_cents, 0) !== w.audit.current_money_cents || b.customer_deposits_cents !== w.banking.expected_deposits_cents || b.assets_cents !== b.liabilities_and_equity_cents || b.assets_cents !== b.customer_deposits_cents + b.equity_cents) c.addIssue({ code: 'custom', message: 'Ungültige Bank-/Einlagenbilanz' });
  const r=w.monetary_policy;
  for(const contract of r.contracts) {
    const n=w.nodes.find(n=>n.id===contract.borrower);
    if(n?.loan_rate_bps!==contract.annual_rate_bps || n?.loan_next_rate_bps!==contract.next_rate_bps || contract.monthly_interest_due_cents!==Math.floor(contract.principal_cents*contract.annual_rate_bps/120000)) c.addIssue({code:'custom',message:'Ungültiger Betriebskreditzins'});
  }
  if(r.machine_offer_bps!==r.rate_bps+r.machine_spread_bps || r.state_offer_bps!==Math.max(0,r.rate_bps+r.state_spread_bps)) c.addIssue({code:'custom',message:'Ungültiges Neukreditangebot'});
  const loan=w.banking.loan;
  if(loan.issue_month!==null && (loan.policy_rate_at_issue_bps===null || loan.annual_rate_bps!==loan.policy_rate_at_issue_bps+loan.spread_bps)) c.addIssue({code:'custom',message:'Ungültige Maschinenzinsbindung'});
  const g=w.public_finance;
  if(g.tranches.reduce((s,t)=>s+t.outstanding_cents,0)!==g.outstanding_cents || g.annual_rate_bps!==r.state_offer_bps || g.tranches.some(t=>t.outstanding_cents>t.original_cents || t.annual_rate_bps!==Math.max(0,t.policy_rate_at_issue_bps+t.spread_bps))) c.addIssue({code:'custom',message:'Ungültige Staatskreditbeträge'});
  if(g.outstanding_cents!==w.nodes.find(n=>n.id==='staat')?.government_loan_cents || g.outstanding_cents!==g.credit_created_cents-g.principal_repaid_cents || g.outstanding_cents+g.remaining_credit_cents!==g.credit_limit_cents || g.interest_charged_cents-g.interest_paid_cents!==g.overdue_interest_cents || b.loan_assets_cents!==w.nodes.filter(n=>n.sector==='firms').reduce((s,n)=>s+(n.loan??0),0)+w.banking.loan.outstanding_cents+g.outstanding_cents) c.addIssue({code:'custom',message:'Ungültige Staatskredit-Gegenforderung'});
  for(const m of [...g.history,g.monthly]) {
    if(m.interest_basis.reduce((s,t)=>s+t.interest_cents,0)!==m.new_interest_charge_cents || Math.floor(m.interest_basis.reduce((s,t)=>s+t.principal_cents*t.annual_rate_bps,0)/120000)!==m.new_interest_charge_cents) c.addIssue({code:'custom',message:'Ungültige Staatszinsbasis'});
    if(m.closing_cash_cents!==m.opening_cash_cents-m.cash_deficit_cents+m.credit_cents-m.principal_repaid_cents || m.closing_principal_cents!==m.opening_principal_cents+m.credit_cents-m.principal_repaid_cents) c.addIssue({code:'custom',message:'Ungültiger Staatskassen-/Schuldenabgleich'});
  }
  const f=w.foreign_trade;
  if(f.domestic_cash_cents!==w.nodes.filter(n=>n.sector!=='bank'&&n.sector!=='external').reduce((s,n)=>s+n.cash_cents,0) || f.foreign_cash_cents!==w.nodes.find(n=>n.id==='ausland')?.cash_cents || f.plan.budget_cents>f.plan.opening_cash_cents || f.month_exports_cents>f.plan.budget_cents || f.net_inflow_cents!==f.month_exports_cents-f.month_imports_cents || f.cumulative_net_inflow_cents!==f.cumulative_exports_cents-f.cumulative_imports_cents) c.addIssue({code:'custom',message:'Ungültiger Außenhandelsabgleich'});
  for(const d of f.deliveries) {
    if(d.inventory_before-d.inventory_after!==d.units || d.amount_cents!==d.units*d.unit_price_cents) c.addIssue({code:'custom',message:'Ungültige Exportlieferung'});
    if(d.month===w.month) {
      const t=w.transactions.find(t=>t.id===d.transaction_id);
      if(!t || t.kind!=='export_sale' || t.source!==d.buyer || t.target!==d.seller || t.amount_cents!==d.amount_cents) c.addIssue({code:'custom',message:'Exportzahlung ohne passende Warenlieferung'});
    }
  }
  for (const n of w.nodes.filter(n => n.sector === 'firms')) {
    const p=n.company?.plan;
    if (!n.company || (p && 'opening_units' in p && (n.inventory !== p.opening_units+n.metrics.produced_units-n.metrics.sold_units || n.company.inventory_value_cents !== p.opening_value_cents+n.metrics.production_cost-n.metrics.cost_of_sales))) c.addIssue({code:'custom', message:'Ungültiger Warenbestand'});
  }
  for (const t of w.transactions) {
    const debit = t.ledger_effect === 'loan_creation' ? 0 : t.amount_cents;
    const credit = t.ledger_effect === 'principal_repayment' ? 0 : t.amount_cents;
    if (!keys.has(t.source) || !keys.has(t.target) || t.source_before - t.source_after !== debit || t.target_after - t.target_before !== credit || t.bank_after.assets_cents !== t.bank_after.liabilities_and_equity_cents) c.addIssue({ code: 'custom', message: 'Ungültige Gegenbuchung' });
  }
});
export type World = z.infer<typeof WorldSchema>;
