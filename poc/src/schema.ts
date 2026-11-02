import { z } from 'zod';
const finite = z.number().finite();
export const CaseIdSchema = z.enum(['variable_loan', 'fixed_loan', 'deposit']);
export type CaseId = z.infer<typeof CaseIdSchema>;
const RowSchema = z.object({
  period: z.number().int().min(1).max(6), case: CaseIdSchema, label: z.string(), state: z.enum(['routine', 'review_due']),
  annual_rate: finite, contract_rate: finite, income: finite, interest_cost: finite, interest_income: finite,
  essential_expenses: finite, planned_allocation: finite.nonnegative(), cash_open: finite.nonnegative(),
  cash_close: finite.nonnegative(), earmarked_close: finite.nonnegative(), arrears_close: finite.nonnegative(),
  total_income: finite, required_payments: finite, actual_payment: finite, monthly_headroom: finite,
  cash_change: finite, payment_gap: finite.nonnegative(),
}).strict();
export type Row = z.infer<typeof RowSchema>;
export const ResultSchema = z.object({
  meta: z.object({engine: z.literal('BPTK-Py'), version: z.string(), elapsed_ms: finite, llm_calls: z.literal(0),
    classification: z.literal('hypothetical_algorithmic_poc'), run_id: z.string(), generated_at: z.string()}).strict(),
  request: z.object({annual_rate_after: finite.min(0).max(.20)}).strict(),
  periods: z.literal(6), change_month: z.literal(3),
  cases: z.array(z.object({id: CaseIdSchema, label: z.string(), loan: finite, deposit: finite, variable: z.boolean()}).strict()).length(3),
  rows: z.array(RowSchema).length(18), baseline: z.array(RowSchema).length(18),
  events: z.array(z.object({id: z.string(), case: CaseIdSchema, period: z.number().int().min(1).max(6),
    kind: z.enum(['cash_flow_settled', 'contract_repriced', 'investment_earmarked', 'payment_gap']), label: z.string(), amount: finite.nullable()}).strict()),
  assumptions: z.array(z.string()),
}).strict().superRefine((result, ctx) => {
  for (const collection of [result.rows, result.baseline]) {
    const keys = new Set(collection.map(row => `${row.case}-${row.period}`));
    if (keys.size !== 18) ctx.addIssue({code: 'custom', message: 'Der Verlauf ist unvollständig.'});
  }
});
export type Result = z.infer<typeof ResultSchema>;
