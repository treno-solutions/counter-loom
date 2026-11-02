#!/usr/bin/env python3
"""Offline boundary checks against pinned local checkouts; never calls an LLM.

TinyTroupe methods are extracted with AST, without decorators/import side effects,
and run against test doubles. Concordia checks use its installed real classes.
These checks do not establish opinion change or simulation fidelity.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace


def identity(*args, **kwargs):
    return lambda f: f


class Person:
    def __init__(self, name):
        self.name = name
        self.inbox = []
        self.accessible = []

    def listen(self, text, source=None):
        self.inbox.append(text)

    def socialize(self, text, source=None):
        self.inbox.append(text)

    def make_agent_accessible(self, other):
        self.accessible.append(other.name)

    def make_all_agents_inaccessible(self):
        self.accessible = []


class WorldDouble:
    def __init__(self, name, broadcast_if_no_target=True):
        self.name = name
        self.broadcast_if_no_target = broadcast_if_no_target
        self.agents = []
        self.reached = []

    def get_agent_by_name(self, name):
        return next((a for a in self.agents if a.name == name), None)

    def _handle_reach_out(self, source, content, target):
        self.reached.append(target)

    def _step(self, **kwargs):
        return None

    def broadcast(self, text, source=None):
        for a in self.agents:
            if a is not source:
                a.listen(text, source)


def load_source_node(path, class_name, method=None, namespace=None):
    tree = ast.parse(path.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)
    if method:
        node = next(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == method)
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
            child.decorator_list = []
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), node], type_ignores=[])
    ast.fix_missing_locations(module)
    env = {'TinyWorld': WorldDouble, 'TinyPerson': Person, 'logger': SimpleNamespace(debug=lambda *a: None), 'name_or_empty': lambda a: a.name if a else '', 'transactional': identity}
    env.update(namespace or {})
    exec(compile(module, path.name, 'exec'), env)
    return env[method or class_name]


def commit(path):
    return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tinytroupe', type=Path, required=True)
    ap.add_argument('--concordia', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    tiny = args.tinytroupe
    expected = {'tinytroupe': '7ce8be378a37ee73f9745d6781452712318afa04', 'concordia': 'f1d3ae6da20b32f686cefc13458cafc695c3b6a2'}
    if commit(tiny) != expected['tinytroupe'] or commit(args.concordia) != expected['concordia']:
        ap.error('Checkouts differ from the reviewed commits; review new source before running probes.')
    world_path = tiny/'tinytroupe/environment/tiny_world.py'
    network_path = tiny/'tinytroupe/environment/tiny_social_network.py'
    network_class = load_source_node(network_path, 'TinySocialNetwork')
    talk = load_source_node(world_path, 'TinyWorld', '_handle_talk')
    results = []
    a,b,c = [Person(n) for n in ['Person_A','Person_B','Person_C']]
    net = network_class('test')
    net.agents = [a,b,c]
    net.add_relation(a,b)
    net._update_agents_contexts()
    assert b.name in a.accessible and c.name not in a.accessible
    results.append({'id':'T01','finding':'Declared contacts mark non-neighbors inaccessible','observed':True,'scope':'isolated source methods with doubles'})
    talk(net,a,'OUTSIDE_GROUP_MARKER',c.name)
    assert 'OUTSIDE_GROUP_MARKER' in c.inbox
    results.append({'id':'T02','finding':'Explicit TALK target outside declared contacts receives message','observed':True,'requirement':'R03','requirement_satisfied':False})
    talk(net,a,'BROADCAST_MARKER',None)
    assert 'BROADCAST_MARKER' in c.inbox
    results.append({'id':'T03','finding':'Default untargeted TALK broadcasts to whole world, not only relations','observed':True,'requirement':'R03','requirement_satisfied':False})
    net._handle_reach_out(a,'hello',b.name)
    assert b.name in net.reached and any('cannot reach out' in x for x in a.inbox)
    results.append({'id':'T04','finding':'Allowed REACH_OUT also issues denial to source after calling base handler','observed':True,'requirement':'R08','requirement_satisfied':False})
    try:
        net._step(timedelta_per_step=None,randomize_agents_order=False,parallelize=False)
        raise AssertionError('Expected incompatible signature')
    except TypeError as e:
        assert 'unexpected keyword argument' in str(e)
    results.append({'id':'T05','finding':'TinySocialNetwork._step rejects keyword arguments used by TinyWorld.run','observed':True,'requirement':'R07','requirement_satisfied':False})
    sys.path.insert(0,str(args.concordia.resolve()))
    from concordia.contrib.components.game_master.forum import ForumState
    fs=ForumState(player_names=['Person_A','Person_B','Person_C'])
    fs.create_post(author='Person_A',title='PUBLIC_MARKER',content='shared')
    assert 'PUBLIC_MARKER' in fs.get_forum_summary_for_player('Person_C')
    results.append({'id':'C01','finding':'Single forum exposes public posts to its players; group boundaries need separate forums or routing','observed':True,'requirement':'R03','scope':'real Concordia class, offline'})
    fs.send_direct_message(sender='Person_A',recipient='Person_B',content='PRIVATE_MARKER')
    assert 'PRIVATE_MARKER' in json.dumps(fs.drain_notifications('Person_B'))
    assert 'PRIVATE_MARKER' not in json.dumps(fs.drain_notifications('Person_C'))
    assert fs.get_direct_message_threads_for_player('Person_C') == {}
    results.append({'id':'C02','finding':'Direct-message notification reaches its recipient, not an unrelated player','observed':True,'requirement':'R03','requirement_satisfied':True})
    restored=ForumState(player_names=['Person_A','Person_B','Person_C'])
    restored.set_state(json.loads(json.dumps(fs.get_state())))
    assert restored.get_recent_posts()[0].title=='PUBLIC_MARKER'
    assert 'PRIVATE_MARKER' in json.dumps(restored.get_direct_message_thread('Person_A','Person_B'))
    results.append({'id':'C03','finding':'Forum posts and direct-message threads survive JSON state round trip','observed':True,'requirement':'R04','requirement_satisfied':True,'scope':'forum state, not a full human-memory validation'})
    out={'checked_on':'2026-11-02','classification':'technical_screen_not_persona_pilot','llm_calls':0,'paid_model_cost':0,'frameworks':{'tinytroupe':{'commit':commit(tiny),'method':'isolated AST-extracted source methods; decorators removed; test doubles used; framework not installed'},'concordia':{'commit':commit(args.concordia),'method':'installed framework; real ForumState class; no model'}},'source_sha256':{str(p.relative_to(tiny)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [world_path,network_path]},'results':results,'limits':['No autonomous persona conversations executed.','No opinion change, causal social influence or teaching outcomes tested.','TinyTroupe checks omit wrappers and full runtime; findings need full-runtime confirmation before fixes.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checks':len(results),'llm_calls':0,'findings':[r['id'] for r in results]}))


if __name__=='__main__':
    main()
