#!/usr/bin/env python3
"""Bounded TinyPerson/TinyWorld pilot; registered transport, no framework patches.
Use --offline-test for technical fixtures only. Set TINYTROUPE_SOURCE and
CONCORDIA_BASE_URL / CONCORDIA_MODEL / CONCORDIA_API_KEY locally for live use.
"""
import argparse,copy,hashlib,json,os,subprocess,sys,time,urllib.request
from pathlib import Path
from datetime import datetime
SCRIPT=Path(__file__).resolve()
ROOT=SCRIPT.parents[1]
RUN=ROOT/'runs/005-tinytroupe-group-influence'
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

class Transport:
 def __init__(self,design,out,offline):
  self.design,self.out,self.offline=design,out,offline
  self.calls=0;self.started=time.monotonic();self.phase='setup';self.actor=None
  self.base=os.environ.get('CONCORDIA_BASE_URL','').rstrip('/')
  self.key=os.environ.get('CONCORDIA_API_KEY','');self.model=os.environ.get('CONCORDIA_MODEL','')
  if not offline and not (self.base and self.model):raise RuntimeError('Missing local model configuration')
 def send_message(self,messages,response_format=None,**kwargs):
  if self.calls>=self.design['max_model_calls'] or time.monotonic()-self.started>self.design['max_total_seconds']:raise RuntimeError('Resource ceiling reached')
  self.calls+=1;rec={'call':self.calls,'actor_id':self.actor,'phase':self.phase,'messages':copy.deepcopy(messages),'requested_model':self.model if not self.offline else 'offline-fixture'}
  try:
   if self.offline:
    content='Technische Testantwort. Keine simulierte Personenmeinung.'
    if response_format:content=json.dumps({'actions':[{'type':'THINK','content':'Technical fixture only.','target':''},{'type':'TALK','content':content,'target':''},{'type':'DONE','content':'','target':''}],'cognitive_state':{'goals':'test','context':[],'attention':'test','emotions':'test'}})
    data={'model':'offline-fixture','choices':[{'message':{'content':content},'finish_reason':'stop'}],'usage':{}}
   else:
    body={'model':self.model,'messages':messages,'temperature':.7,'top_p':.95,'max_tokens':self.design['max_output_tokens_per_call'],'extra_body':{'chat_template_kwargs':{'enable_thinking':False}}}
    if response_format:body['response_format']={'type':'json_schema','json_schema':{'name':'persona_action','strict':False,'schema':response_format.model_json_schema()}}
    rec['generation_parameters']={k:v for k,v in body.items() if k not in ['messages','model']}
    if len(json.dumps(messages))>self.design['max_prompt_characters']:raise RuntimeError('Prompt ceiling reached')
    headers={'Content-Type':'application/json','Authorization':'Bearer '+self.key}
    with urllib.request.urlopen(urllib.request.Request(self.base+'/chat/completions',data=json.dumps(body).encode(),headers=headers),timeout=min(60,self.design['max_total_seconds']-(time.monotonic()-self.started))) as r:data=json.load(r)
   choice=data['choices'][0];content=choice['message']['content']
   rec.update(response=content,resolved_model=data.get('model'),usage=data.get('usage'),finish_reason=choice.get('finish_reason'))
   if not isinstance(content,str) or not content.strip() or choice.get('finish_reason')=='length':raise RuntimeError('Empty or incomplete visible response')
   if response_format:response_format.model_validate_json(content)
   return {'role':'assistant','content':content}
  except Exception as err:
   rec['error_type']=type(err).__name__
   # Prevent framework retry decorators from hiding format/transport errors.
   raise RuntimeError('Model request failed; consult redacted request record') from None
  finally:
   with (self.out/'model-calls.jsonl').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--offline-test',action='store_true');args=parser.parse_args()
 out=args.output.resolve()
 if out.exists():parser.error('Output exists; choose a fresh directory')
 source=Path(os.environ.get('TINYTROUPE_SOURCE',ROOT/'.framework-review/tinytroupe')).resolve()
 design=json.loads((RUN/'inputs/design.json').read_text());info=json.loads((RUN/'inputs/people.json').read_text());scenario=json.loads((RUN/'inputs/scenario.json').read_text())
 assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD']).decode().strip()==design['framework_commit']
 for e in json.loads((RUN/'inputs/input-manifest.json').read_text()):assert hashlib.sha256((RUN/e['path']).read_bytes()).hexdigest()==e['sha256']
 # All framework startup/debug output goes to a private working directory.
 work=ROOT/'.framework-review/tinytroupe-runtime';work.mkdir(exist_ok=True);os.chdir(work)
 os.environ.setdefault('OPENAI_API_KEY','unused-no-default-api-calls');sys.path.insert(0,str(source))
 from tinytroupe import config_manager
 config_manager.update_multiple({'enable_memory_consolidation':False,'enable_continuous_contextual_semantic_memory_retrieval':False,'parallel_agent_actions':False,'max_attempts':1,'action_generator_enable_quality_checks':False,'action_generator_enable_regeneration':False,'action_generator_enable_direct_correction':False,'loglevel':'ERROR','loglevel_console':'ERROR','loglevel_file':'ERROR','model':os.environ.get('CONCORDIA_MODEL','offline-fixture')})
 from tinytroupe.agent import TinyPerson
 from tinytroupe.agent.action_generator import ActionGenerator
 from tinytroupe.environment import TinyWorld
 from tinytroupe.clients import register_client,force_api_type
 assert Path(sys.modules['tinytroupe'].__file__).resolve().is_relative_to(source)
 out.mkdir(parents=True)
 transport=Transport(design,out,args.offline_test);register_client('counterloom_bounded',transport);force_api_type('counterloom_bounded')
 people=info['people'];actors={};responses=[];deliveries=[];worlds={}
 status={'execution_status':'running','classification':'offline_technical_fixture' if args.offline_test else 'generative_exploratory_pilot','framework_commit':design['framework_commit'],'runner_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'completed_phases':[]}
 write(out/'input-snapshot.json',{'people':info,'scenario':scenario,'design':design})
 def states():return {pid:a.encode_complete_state() for pid,a in actors.items()}
 def checkpoint():write(out/'responses.json',responses);write(out/'latest-states.json',states());write(out/'deliveries.json',deliveries)
 def act(p,phase,question):
  transport.phase,transport.actor=phase,p['id'];a=actors[p['id']]
  a.listen(question+' Antworte auf Deutsch. Nutze den normalen Ablauf THINK, dann genau eine TALK-Aktion mit deinem Beitrag, danach DONE. Ziel leer lassen. Kein ausgeführter Handel.')
  result=a.act(until_done=True,return_actions=True,communication_display=False)
  if not any(x['action']['type']=='TALK' for x in result):raise RuntimeError('No TALK produced in the completed turn')
  record={'id':f'T{len(responses)+1:03}','actor_id':p['id'],'phase':phase,'actions':result}
  responses.append(record);a.pop_latest_actions();checkpoint();return result
 try:
  TinyPerson.communication_display=False;TinyWorld.communication_display=False
  for p in people:
   generator=ActionGenerator(max_attempts=1,enable_quality_checks=False,enable_regeneration=False,enable_direct_correction=False,enable_multi_action_output=True,enable_reasoning_step=False)
   a=TinyPerson(p['name'],action_generator=generator,enable_basic_action_repetition_prevention=False)
   # This source version ignores False in the constructor; set the attribute explicitly.
   a.enable_basic_action_repetition_prevention=False
   a.define('background',p['background']);a.define('starting_view',p['starting_view']);actors[p['id']]=a
  for g in info['groups']:
   members=[actors[p['id']] for p in people if p['group']==g['id']]
   w=TinyWorld(g['id'],agents=members,initial_datetime=datetime(2026,11,2,12),broadcast_if_no_target=True);worlds[g['id']]=w
   for a in members:
    for b in members:
     if a!=b:a.make_agent_accessible(b)
    a.listen(g['context']);a.listen(scenario['text'])
  for p in people:act(p,'initial',scenario['assessment_question'])
  initial=states();write(out/'initial-states.json',initial)
  for phase in ['A_no_peer_exchange','B_within_group_exchange']:
   for pid,a in actors.items():a.decode_complete_state(copy.deepcopy(initial[pid]))
   hashes={pid:digest(a.encode_complete_state()) for pid,a in actors.items()}
   assert hashes=={pid:digest(s) for pid,s in initial.items()}
   write(out/(phase+'-starting-hashes.json'),hashes)
   if phase.startswith('B'):
    for p in people:
     result=act(p,phase+'/discussion',scenario['discussion_question']);a=actors[p['id']];before=states()
     # Use the existing world dispatcher; no custom speech forwarding.
     worlds[p['group']]._handle_actions(a,[r['action'] for r in result])
     after=states()
     for q in people:
      if digest(before[q['id']])!=digest(after[q['id']]):
       assert p['group']==q['group'] and p['id']!=q['id']
       deliveries.append({'response_ref':responses[-1]['id'],'sender':p['id'],'recipient':q['id'],'memory_before_hash':digest(before[q['id']]['episodic_memory']),'memory_after_hash':digest(after[q['id']]['episodic_memory'])})
     checkpoint()
   for p in people:act(p,phase+'/final',scenario['assessment_question'])
   write(out/(phase+'-states.json'),states());status['completed_phases'].append(phase)
  # Cheap direct-prompt baseline: same case, group context, news and neutral question;
  # no framework system prompt, cognitive state or remembered conversations.
  for p in people:
   transport.phase,transport.actor='direct_prompt_baseline',p['id']
   g=next(g for g in info['groups'] if g['id']==p['group'])
   prompt=json.dumps({'person':p,'group':g,'news':scenario['text'],'question':scenario['assessment_question']},ensure_ascii=False)
   r=transport.send_message([{'role':'user','content':prompt}]);responses.append({'id':f'T{len(responses)+1:03}','actor_id':p['id'],'phase':transport.phase,'response':r['content']});checkpoint()
  assert transport.calls==design['planned_text_calls']
  if args.offline_test:assert len(deliveries)==design['people_count']*(design['people_count']//design['group_count']-1), 'Technical TALK fixture must reach every group peer'
  status['execution_status']='completed'
 except BaseException as err:
  status.update(execution_status='failed',error_type=type(err).__name__);raise
 finally:
  status.update(llm_requests=0 if args.offline_test else transport.calls,transport_requests=transport.calls,elapsed_seconds=round(time.monotonic()-transport.started,2),delivered_peer_messages=len(deliveries));write(out/'status.json',status)
 print(json.dumps(status))
if __name__=='__main__':main()
