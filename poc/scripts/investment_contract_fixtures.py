"""Actual low/high-rate project states in addition to the phase contract fixtures."""
import sys,json
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World
from scripts.stability_contract_fixtures import fixtures

rows=fixtures();base=World.stable()
for _ in range(112*5):base.step(False)
for rate in (200,500):
    w=deepcopy(base)
    if rate!=200:w.monetary.queue(w,rate)
    for _ in range(5):w.step(False)
    rows.append(dict(label='project-'+str(rate),world=w.snapshot()))
p=Path(sys.argv[1] if len(sys.argv)>1 else '.framework-review/investment-contract.json')
p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(rows))
