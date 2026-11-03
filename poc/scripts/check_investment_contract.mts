import fs from 'node:fs';
import assert from 'node:assert/strict';
import {WorldSchema} from '../src/world-schema.ts';
const rows:{label:string;world:unknown}[]=JSON.parse(fs.readFileSync(process.argv[2]??'.framework-review/investment-contract.json','utf8'));
for(const r of rows)assert(WorldSchema.safeParse(r.world).success,r.label);
const low=WorldSchema.parse(rows.find(r=>r.label==='project-200')!.world);
const high=WorldSchema.parse(rows.find(r=>r.label==='project-500')!.world);
assert(low.capital_orders.assessment!.cash_npv_cents>0);
assert(high.capital_orders.assessment!.cash_npv_cents<0);
for(const key of ['monthly_before_tax_cents','cash_npv_cents','loan_interest_cents','cash_required_cents'] as const){
 const bad=structuredClone(low);bad.capital_orders.assessment![key]++;
 assert(!WorldSchema.safeParse(bad).success,key);
}
const missing=structuredClone(low) as unknown as {capital_orders:Record<string,unknown>};
delete missing.capital_orders.assessment;assert(!WorldSchema.safeParse(missing).success);
const old=structuredClone(low) as unknown as {classification:string};old.classification='illustrative_circular_flow_v19';assert(!WorldSchema.safeParse(old).success);
const ineligible=structuredClone(high);ineligible.capital_orders.assessment!.decision='invest';assert(!WorldSchema.safeParse(ineligible).success);
const debt=structuredClone(low);debt.capital_orders.assessment!.loan_schedule[0].principal_cents++;assert(!WorldSchema.safeParse(debt).success);
console.log(rows.length+' actual phase/project snapshots accepted; eight malformed states rejected.');
