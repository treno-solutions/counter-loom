import { z } from 'zod';
const cents = z.number().int().nonnegative();
const signedCents = z.number().int();
export const Sector = z.enum(['households', 'firms', 'government', 'bank', 'external']);
export type SectorId = z.infer<typeof Sector>;
const Metric = z.object({ income: cents, tax: cents, sales: cents, operating_costs: cents, wages: cents, interest: cents, sold_units: cents, unmet_units: cents, produced_units: cents, investment: cents, transfers: cents, consumption_plan: cents, consumption_budget: cents, consumption_paid: cents, reserve_used: cents, unfunded_units: cents, production_plan: cents, cost_of_sales: cents, production_cost: cents, idle_cost: cents, interest_expense: cents, unpaid_wages: cents });
const CompanyPlan = z.object({ demand_units: cents, target_units: cents, opening_units: cents, opening_value_cents: cents, capacity_units: cents, needed_units: cents, production_units: cents, funded_units: cents, energy_unit_cents: cents, wages_due_cents: cents, interest_due_cents: cents, debt_service_cents: cents, staff: cents }).strict();
const CompanyResult = z.object({ funded_orders_units: cents, profit_before_tax_cents: signedCents, tax_due_cents: cents, tax_paid_cents: cents, after_tax_cents: signedCents, distribution_cents: cents, retained_result_cents: signedCents, reserve_cents: cents, desired_staff: cents, next_staff: cents, staff_reason: z.string(), distribution_reason: z.string() }).strict();
const Company = z.object({ forecast_milli: cents, inventory_value_cents: cents, staff_signal: signedCents, short_months: cents, last_investment_month: cents, plan: z.union([CompanyPlan,z.object({}).strict()]), result: z.union([CompanyResult,z.object({}).strict()]) }).strict();
export const NodeSchema = z.object({ id: z.string(), name: z.string(), sector: Sector, cash_cents: cents, metrics: Metric, employees: z.array(z.string()).optional(), employer: z.string().nullable().optional(), inventory: cents.optional(), capital: cents.optional(), loan: cents.optional(), loan_assets: cents.optional(), price: cents.optional(), productivity: cents.optional(), weak_months: cents.optional(), dividend_carry: cents.optional(), reserved_units: cents.optional(), machine_loan_cents: cents.optional(), company: Company.optional() }).strict();
export type WorldNode = z.infer<typeof NodeSchema>;
const BalanceSchema = z.object({ reserves_cents: cents, loan_assets_cents: cents, customer_deposits_cents: cents, equity_cents: cents, assets_cents: cents, liabilities_and_equity_cents: cents }).strict();
const TransactionSchema = z.object({ id: z.number().int(), month: z.number().int(), phase: z.number().int().min(0).max(4), source: z.string(), target: z.string(), amount_cents: cents, kind: z.string(), label: z.string(), source_before: cents, source_after: cents, target_before: cents, target_after: cents, ledger_effect: z.enum(['transfer', 'bank_income', 'bank_distribution', 'loan_creation', 'principal_repayment']), deposit_delta_cents: signedCents, loan_delta_cents: signedCents, equity_delta_cents: signedCents, bank_before: BalanceSchema, bank_after: BalanceSchema }).strict();
export type Transaction = z.infer<typeof TransactionSchema>;
const LoanSchema = z.object({ status: z.enum(['available', 'requested', 'credited', 'delivered', 'repaying', 'repaid']), amount_cents: cents, outstanding_cents: cents, annual_rate_bps: cents, monthly_principal_cents: cents, term_months: cents, borrower: z.string(), supplier: z.string(), units: cents, issue_month: cents.nullable(), delivery_month: cents.nullable(), last_service_month: cents.nullable(), principal_paid_cents: cents, interest_paid_cents: cents, interest_charged_cents: cents, overdue_interest_cents: cents, overdue_principal_cents: cents, message: z.string() }).strict();
export const WorldSchema = z.object({
  world_id: z.string(), revision: z.number().int(), month: z.number().int(), phase: z.number().int().min(-1).max(4), phase_label: z.string(), nodes: z.array(NodeSchema).length(11), transactions: z.array(TransactionSchema), notices: z.array(z.object({ month: z.number().int(), phase: z.number().int(), node: z.string(), text: z.string() })),
  history: z.array(z.object({ month: z.number().int(), consumption_cents: cents, employment: cents, household_cash_cents: cents, government_cash_cents: cents, cash_by_sector: z.record(Sector, cents) })), pending: z.array(z.string()), active: z.array(z.object({ event: z.string(), month: z.number().int() })), rules: z.record(Sector, z.string()),
  audit: z.object({ total_money_cents: cents, current_money_cents: cents, transaction_count: cents, open_obligations_cents: cents, loan_principal_cents: cents, llm_calls: z.literal(0) }), month_open: z.record(z.string(), cents), initial_balances: z.record(z.string(), cents), parameters: z.object({ energy_multiplier: z.number().int(), consumption_percent: z.number().int(), essential_budget_cents: cents }), classification: z.literal('illustrative_circular_flow_v4'), horizon_months: z.literal(24), completed: z.boolean(),
  banking: z.object({ balance: BalanceSchema, loan: LoanSchema, events: z.array(TransactionSchema), initial_deposits_cents: cents, credit_created_cents: cents, principal_repaid_cents: cents, interest_received_cents: cents, distributed_cents: cents, expected_deposits_cents: cents }).strict(),
}).strict().superRefine((w, c) => {
  const keys = new Set(w.nodes.map(n => n.id));
  const b = w.banking.balance;
  if (keys.size !== 11 || w.nodes.filter(n => n.sector !== 'bank').reduce((s, n) => s + n.cash_cents, 0) !== w.audit.current_money_cents || b.customer_deposits_cents !== w.banking.expected_deposits_cents || b.assets_cents !== b.liabilities_and_equity_cents || b.assets_cents !== b.customer_deposits_cents + b.equity_cents) c.addIssue({ code: 'custom', message: 'Ungültige Bank-/Einlagenbilanz' });
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
