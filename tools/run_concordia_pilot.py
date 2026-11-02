#!/usr/bin/env python3
"""Bounded experiment using Concordia's existing agents, memory and forums.

--verify-only performs no language-model requests. Live access is configured with
CONCORDIA_BASE_URL, CONCORDIA_MODEL and optionally CONCORDIA_API_KEY. This is a
thin OpenAI-compatible HTTP adapter, not a new agent or influence engine.
"""
import argparse
import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path
import time
import urllib.error
import urllib.request

import numpy as np
from concordia.associative_memory import basic_associative_memory
from concordia.contrib.components.game_master.forum import ForumState
from concordia.language_model import language_model, no_language_model
from concordia.prefabs.entity import minimal
from concordia.typing import entity as entity_lib

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/004-concordia-group-influence'


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def digest(data):
    def canonical(value, key=None):
        if isinstance(value,dict): return {k:canonical(v,k) for k,v in value.items()}
        if isinstance(value,list):
            values=[canonical(v) for v in value]
            return sorted(values) if key=='stored_hashes' else values
        return value
    return hashlib.sha256(json.dumps(canonical(data),ensure_ascii=False,sort_keys=True).encode()).hexdigest()


class BoundedHTTPModel(language_model.LanguageModel):
    def __init__(self, design, output):
        self.base=os.environ.get('CONCORDIA_BASE_URL','').rstrip('/')
        self.model=os.environ.get('CONCORDIA_MODEL','')
        self.key=os.environ.get('CONCORDIA_API_KEY','')
        if not self.base or not self.model:
            raise ValueError('Model endpoint and model name must be configured before execution.')
        self.design=design;self.output=output;self.calls=0;self.started=time.monotonic()
        self.context={};self.usage=[]

    def sample_text(self,prompt,*,max_tokens=400,terminators=(),temperature=.7,top_p=.95,top_k=64,timeout=45,seed=None):
        del top_k
        if self.calls>=self.design['max_model_calls']:
            raise RuntimeError('Model-call budget exhausted; no fallback responses generated.')
        if time.monotonic()-self.started>self.design['max_total_seconds']:
            raise RuntimeError('Total runtime limit exceeded.')
        if len(prompt)>self.design['max_prompt_characters']:
            raise RuntimeError('Prompt-size limit exceeded.')
        self.calls+=1
        token_param=os.environ.get('CONCORDIA_TOKEN_PARAMETER','max_tokens')
        if token_param not in ['max_tokens','max_completion_tokens']:
            raise ValueError('Unsupported token-limit parameter.')
        body={'model':self.model,'messages':[{'role':'user','content':prompt}],token_param:min(max_tokens,self.design['max_output_tokens_per_call'])}
        if os.environ.get('CONCORDIA_SEND_SAMPLING','true')=='true':
            body.update(temperature=.7,top_p=.95)
        if self.design.get('disable_thinking'):
            body['extra_body']={'chat_template_kwargs':{'enable_thinking':False}}
        if terminators:body['stop']=list(terminators)
        headers={'Content-Type':'application/json'}
        if self.key:headers['Authorization']='Bearer '+self.key
        req=urllib.request.Request(self.base+'/chat/completions',json.dumps(body).encode(),headers=headers)
        record={'call':self.calls,**self.context,'requested_model':self.model,'prompt':prompt,'requested_output_limit':body[token_param]}
        try:
            with urllib.request.urlopen(req,timeout=min(timeout,self.design['timeout_seconds_per_call'],self.design['max_total_seconds']-(time.monotonic()-self.started))) as response:
                data=json.load(response)
            choice=data['choices'][0]
            text=choice['message']['content']
            record.update(resolved_model=data.get('model'),usage=data.get('usage'),finish_reason=choice.get('finish_reason'),thinking_disabled_requested=bool(self.design.get('disable_thinking')))
            if not isinstance(text,str) or not text.strip():raise ValueError('Empty model response.')
            record.update(response=text,resolved_model=data.get('model'),usage=data.get('usage'),finish_reason=choice.get('finish_reason'))
            if choice.get('finish_reason')=='length':
                record['truncated']=True
                raise RuntimeError('Output limit reached; incomplete answer preserved, execution stopped.')
            self.usage.append(data.get('usage'))
            return text
        except urllib.error.HTTPError as err:
            record.update(error_type='HTTPError',http_status=err.code)
            raise RuntimeError('Model endpoint rejected request; details omitted to protect credentials.') from None
        except Exception as err:
            record.setdefault('error_type',type(err).__name__)
            raise
        finally:
            with self.output.open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')

    def sample_choice(self,*args,**kwargs):
        raise NotImplementedError('This experiment uses free text only; no implicit choice fallback.')


def build(person,groups,people,model):
    group=next(g for g in groups if g['id']==person['group'])
    names=', '.join(p['name'] for p in people if p['group']==person['group'] and p['id']!=person['id'])
    instructions=(f"Du bist {person['name']}, eine fiktive erwachsene Person in einem Workshop-Szenario. "
      f"Lebenslage: {person['background']} Ausgangssicht: {person['starting_view']} "
      f"Soziales Umfeld: {group['context']} Bekannte in diesem Kreis: {names}. "
      "Du bist kein Assistent und kein Berufsberater. Du darfst Zweifel haben, widersprechen, nichts tun oder deine Meinung ändern. "
      "Erfinde keine neuen Lebensereignisse, Nachrichtentatsachen oder erhaltenen Gespräche. "
      "Trenne Gefühle, Einschätzung und Handlungsabsicht. Berichte nur über deine eigene Perspektive; es gibt keine gewünschte richtige Antwort.")
    # Minimal prefab uses recent observations, not semantic similarity retrieval.
    # The constant vector satisfies storage; no semantic-memory capability is claimed.
    bank=basic_associative_memory.AssociativeMemoryBank(sentence_embedder=lambda _:np.ones(1))
    return minimal.Entity(params={'name':person['name'],'custom_instructions':instructions,'randomize_choices':False}).build(model=model,memory_bank=bank)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--output',type=Path,default=RUN/'exports/attempt-01')
    args=parser.parse_args()
    info=json.loads((RUN/'inputs/people.json').read_text())
    scenario=json.loads((RUN/'inputs/scenario.json').read_text())
    design=json.loads((RUN/'inputs/design.json').read_text())
    people=info['people'];groups=info['groups']
    source_root=Path(minimal.__file__).resolve().parents[3]
    actual_commit=subprocess.check_output(['git','-C',str(source_root),'rev-parse','HEAD'],text=True).strip()
    if actual_commit!=design['framework_commit']:
        raise RuntimeError('Installed Concordia source differs from the planned commit.')
    assert len(people)==8 and len(groups)==2
    for item in json.loads((RUN/'inputs/input-manifest.json').read_text()):
        assert hashlib.sha256((RUN/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    dummy=no_language_model.NoLanguageModel()
    actors={p['id']:build(p,groups,people,dummy) for p in people}
    for a in actors.values():a.observe('[N01] '+scenario['text'])
    initial={pid:copy.deepcopy(a.get_state()) for pid,a in actors.items()}
    for p in people:
        if p['group']=='G01':actors[p['id']].observe('GROUP_ISOLATION_MARKER')
    assert all('GROUP_ISOLATION_MARKER' not in json.dumps(actors[p['id']].get_state()) for p in people if p['group']=='G02')
    for pid,a in actors.items():
        a.set_state(copy.deepcopy(initial[pid]));assert digest(a.get_state())==digest(initial[pid])
    if args.verify_only:
        write(ROOT/'qa/concordia-pilot-readiness.json',{'checked_on':'2026-11-02','passed':True,'people':8,'groups':2,'input_checksums':'passed','group_observation_isolation':'passed','state_round_trip':'passed','llm_calls':0,'model_access_checked':False,'scope':'offline preflight only; model access and budget require separate verification','limits':'Technical setup only; no simulated opinions generated.'})
        print('Offline preparation verified; no model calls. Model access was not checked by this command.');return
    if args.output.exists():parser.error('Output exists; choose a fresh attempt directory. No result overwrite.')
    # Validate connection configuration before creating a result directory.
    model=BoundedHTTPModel(design,args.output/'model-calls.jsonl')
    args.output.mkdir(parents=True)
    write(args.output/'input-snapshot.json',{'people':info,'scenario':scenario,'design':design})
    status={'execution_status':'running','llm_calls':0,'model':model.model,'provider':'configured_openai_compatible_endpoint','endpoint_redacted':True,'framework_commit':design['framework_commit'],'conditions':[]}
    write(args.output/'status.json',status)
    records=[]
    def act(pid,agent,question,phase):
        model.context={'actor_id':pid,'phase':phase}
        response=agent.act(entity_lib.free_action_spec(call_to_action=question))
        records.append({'id':f'E{len(records)+1:03d}','actor_id':pid,'phase':phase,'response':response})
        agent.observe('[Eigene Äußerung] '+response)
        write(args.output/'responses.json',records)
        write(args.output/'latest-states.json',{i:a.get_state() for i,a in agents.items()})
        return response
    try:
        agents={p['id']:build(p,groups,people,model) for p in people}
        for a in agents.values():a.observe('[N01] '+scenario['text'])
        for p in people:act(p['id'],agents[p['id']],scenario['assessment_question'],'initial')
        states={pid:copy.deepcopy(a.get_state()) for pid,a in agents.items()}
        write(args.output/'initial-states.json',states)
        for condition in design['conditions']:
            agents={p['id']:build(p,groups,people,model) for p in people}
            for pid,a in agents.items():
                a.set_state(copy.deepcopy(states[pid]));assert digest(a.get_state())==digest(states[pid])
            write(args.output/(condition+'-starting-hashes.json'),{pid:digest(a.get_state()) for pid,a in agents.items()})
            forums={g['id']:ForumState(player_names=[p['name'] for p in people if p['group']==g['id']]) for g in groups}
            deliveries=[]
            if condition=='B_within_group_exchange':
                for round_index in range(design['discussion_rounds']):
                    for p in people:
                        response=act(p['id'],agents[p['id']],scenario['discussion_question'],f'{condition}/round-{round_index+1}')
                        post_id=forums[p['group']].create_post(author=p['name'],title=f"Beitrag {p['id']}",content=response)
                        for peer in people:
                            if peer['group']==p['group'] and peer['id']!=p['id']:
                                ref=f"{p['group']}/post-{post_id}"
                                agents[peer['id']].observe(f"[{ref}] {p['name']} sagt: {response}")
                                deliveries.append({'post_ref':ref,'sender':p['id'],'recipient':peer['id'],'round':round_index+1})
                        write(args.output/(condition+'-forums.json'),{gid:f.get_state() for gid,f in forums.items()})
                        write(args.output/(condition+'-deliveries.json'),deliveries)
            for p in people:act(p['id'],agents[p['id']],scenario['assessment_question'],condition+'/final')
            write(args.output/(condition+'-states.json'),{pid:a.get_state() for pid,a in agents.items()})
            status['conditions'].append(condition);write(args.output/'status.json',status)
        assert model.calls==design['planned_text_calls']
        status['execution_status']='completed'
    except Exception as err:
        status.update(execution_status='failed',error_type=type(err).__name__)
        # Do not persist raw exception text, URLs, headers, or local paths.
        raise
    finally:
        status.update(llm_calls=model.calls,usage=model.usage,elapsed_seconds=round(time.monotonic()-model.started,2))
        write(args.output/'status.json',status)
    print('Completed bounded experiment; interpret records before drawing conclusions.')


if __name__=='__main__':main()
