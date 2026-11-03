import fs from 'node:fs';
import assert from 'node:assert/strict';
import { WorldSchema } from '../src/world-schema.ts';
const rows: {label:string;world:unknown}[]=JSON.parse(fs.readFileSync(process.argv[2]??'.framework-review/bank-v19-contract.json','utf8'));
for(const row of rows)assert(WorldSchema.safeParse(row.world).success,row.label);
const closed=rows.map(r=>WorldSchema.parse(r.world)).find(w=>w.banking.profit.monthly.closed)!;
assert(closed);
for(const field of ['profit_tax_due_cents','distribution_cents','retained_earnings_cents','closing_equity_cents'] as const){
 const bad=structuredClone(closed);
 bad.banking.profit.monthly[field]+=(field==='closing_equity_cents'?-1000000:1);
 assert(!WorldSchema.safeParse(bad).success,field);
}
const missing=structuredClone(closed) as unknown as {banking:Record<string,unknown>};
delete missing.banking.profit;
assert(!WorldSchema.safeParse(missing).success,'missing bank profit');
const wrongVersion=structuredClone(closed) as unknown as {classification:string};
wrongVersion.classification='illustrative_circular_flow_v18';
assert(!WorldSchema.safeParse(wrongVersion).success,'old model contract');
const wrongCounter=structuredClone(closed);wrongCounter.banking.profit_tax_paid_cents++;
assert(!WorldSchema.safeParse(wrongCounter).success,'bank tax bridge counter');
const wrongRate=structuredClone(closed);wrongRate.banking.profit.profit_tax_bps=0;
assert(!WorldSchema.safeParse(wrongRate).success,'bank tax rate');
console.log(`${rows.length} phase snapshots accepted; eight malformed/incompatible snapshots rejected.`);
