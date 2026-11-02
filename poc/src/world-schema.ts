import { z } from 'zod';
const cents=z.number().int().nonnegative();
export const Sector=z.enum(['households','firms','government','bank','external']);
export type SectorId=z.infer<typeof Sector>;
const Metric=z.object({income:cents,tax:cents,sales:cents,operating_costs:cents,wages:cents,interest:cents,sold_units:cents,unmet_units:cents,produced_units:cents,investment:cents,transfers:cents,consumption_plan:cents,consumption_budget:cents,consumption_paid:cents,reserve_used:cents});
export const NodeSchema=z.object({id:z.string(),name:z.string(),sector:Sector,cash_cents:cents,metrics:Metric,employees:z.array(z.string()).optional(),employer:z.string().nullable().optional(),inventory:cents.optional(),capital:cents.optional(),loan:cents.optional(),loan_assets:cents.optional(),price:cents.optional(),productivity:cents.optional(),weak_months:cents.optional(),dividend_carry:cents.optional()}).strict();
export type WorldNode=z.infer<typeof NodeSchema>;
const Transaction=z.object({id:z.number().int(),month:z.number().int(),phase:z.number().int().min(0).max(4),source:z.string(),target:z.string(),amount_cents:cents,kind:z.string(),label:z.string(),source_before:cents,source_after:cents,target_before:cents,target_after:cents}).strict();
export type Transaction=z.infer<typeof Transaction>;
export const WorldSchema=z.object({world_id:z.string(),revision:z.number().int(),month:z.number().int(),phase:z.number().int().min(-1).max(4),phase_label:z.string(),nodes:z.array(NodeSchema).length(11),transactions:z.array(Transaction),notices:z.array(z.object({month:z.number().int(),phase:z.number().int(),node:z.string(),text:z.string()})),history:z.array(z.object({month:z.number().int(),consumption_cents:cents,employment:cents,household_cash_cents:cents,government_cash_cents:cents,cash_by_sector:z.record(Sector,cents)})),pending:z.array(z.string()),active:z.array(z.object({event:z.string(),month:z.number().int()})),rules:z.record(Sector,z.string()),audit:z.object({total_money_cents:cents,current_money_cents:cents,transaction_count:cents,open_obligations_cents:cents,loan_principal_cents:cents,llm_calls:z.literal(0)}),month_open:z.record(z.string(),cents),initial_balances:z.record(z.string(),cents),parameters:z.object({energy_multiplier:z.number().int(),consumption_percent:z.number().int(),essential_budget_cents:cents}),classification:z.literal('illustrative_circular_flow_v2')}).strict().superRefine((w,c)=>{
 const keys=new Set(w.nodes.map(n=>n.id));
 if(keys.size!==11||w.nodes.reduce((s,n)=>s+n.cash_cents,0)!==w.audit.total_money_cents||w.audit.current_money_cents!==w.audit.total_money_cents)c.addIssue({code:'custom',message:'Ungültige Kontenbilanz'});
 if(w.transactions.some(t=>!keys.has(t.source)||!keys.has(t.target)||t.source_before-t.source_after!==t.amount_cents||t.target_after-t.target_before!==t.amount_cents))c.addIssue({code:'custom',message:'Ungültige Buchung'});
});
export type World=z.infer<typeof WorldSchema>;
