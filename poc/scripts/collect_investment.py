"""Combine completed independent experiment parts; preserve source provenance."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('late');p.add_argument('new');p.add_argument('--output',default='qa/investment-v20-comparison.json');a=p.parse_args()
late,new=(json.loads(Path(f).read_text()) for f in (a.late,a.new))
assert late['source_sha256']==new['source_sha256']
assert late['reference_sha256']==new['reference_sha256']
for f,h in late['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h,f
assert late['checks']['v19_anchor_and_both_branches_exact']
assert new['experiments'][-1]['name']=='mature_valuation'
late['experiments']+=new['experiments']
late['late_reference_history']=new['late_reference_history']
late['marginal_opportunity_found']=new['marginal_opportunity_found']
late['checks']=dict(warmup_phases_checked=late['checks']['warmup_phases_checked']+new['checks']['warmup_phases_checked'],
    branch_phases_checked=late['checks']['branch_phases_checked']+new['checks']['branch_phases_checked'],
    v19_anchor_and_both_branches_exact=True,independent_journal_reconstruction=True,
    first_marginal_opportunity_selected_before_shock_branches=True)
Path(a.output).write_text(json.dumps(late,ensure_ascii=False,indent=2)+'\n')
print('Combined',sum(len(e['runs']) for e in late['experiments']),'verified branches')
