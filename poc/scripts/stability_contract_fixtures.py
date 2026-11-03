"""Snapshots at production, order, closure, energy and rate boundaries."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world import World


def fixtures():
    rows=[]
    for name,factory in [('historical',World),('stable',World.stable)]:
        w=factory();rows.append(dict(label=name+'-initial',world=w.snapshot()))
        for step in range(40):
            w.step(False)
            if step in (0,3,4,23,24,25,29,39):rows.append(dict(label=f'{name}-{step}',world=w.snapshot()))
        w.queue('energy');w.monetary.queue(w,500);w.crisis.queue(w,'both',2,6000)
        for step in range(15):
            w.step(False)
            if step in (0,4,9,14):rows.append(dict(label=f'{name}-shock-{step}',world=w.snapshot()))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='.framework-review/stability-contract.json');a=p.parse_args()
    target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(fixtures()))
