import fs from 'node:fs';
import {WorldSchema} from '../src/world-schema.ts';
const input=process.argv[2]??'.framework-review/stability-contract.json';
const rows: {label:string;world:unknown}[]=JSON.parse(fs.readFileSync(input,'utf8'));
for(const row of rows) {
 const result=WorldSchema.safeParse(row.world);
 if(!result.success)throw new Error(`${row.label}: ${JSON.stringify(result.error.issues)}`);
}
console.log(`${rows.length} phase snapshots passed the UI contract.`);
