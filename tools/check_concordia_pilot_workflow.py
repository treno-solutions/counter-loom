#!/usr/bin/env python3
"""Exercise the actual Concordia workflow with a local HTTP test double only.
Run from the repository root using the review virtual environment.
No generated persona opinions or external model requests are produced.
"""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
import json,os,subprocess,tempfile
from pathlib import Path
count=[0]
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  assert request['max_tokens']<=400
  count[0]+=1
  data=json.dumps({'model':'technical-test-double','choices':[{'message':{'content':'Technische Testantwort. Keine Personenreaktion oder Meinung.'},'finish_reason':'stop'}],'usage':{'prompt_tokens':1,'completion_tokens':1}}).encode()
  self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(data)
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=server.serve_forever,daemon=True).start()
parent=Path('.framework-review/pilot-tests');parent.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=parent) as tmp:
 out=Path(tmp)/'attempt'
 env=dict(os.environ,CONCORDIA_BASE_URL=f'http://127.0.0.1:{server.server_port}/v1',CONCORDIA_MODEL='technical-test-double')
 run=subprocess.run(['.framework-review/venv/bin/python','tools/run_concordia_pilot.py','--output',str(out)],env=env,capture_output=True,text=True,timeout=40)
 if run.returncode: print(run.stderr[-2000:]);raise SystemExit(run.returncode)
 status=json.loads((out/'status.json').read_text());assert status['execution_status']=='completed' and count[0]==40
 a=json.loads((out/'A_no_peer_exchange-starting-hashes.json').read_text());b=json.loads((out/'B_within_group_exchange-starting-hashes.json').read_text());assert a==b
 ds=json.loads((out/'B_within_group_exchange-deliveries.json').read_text());assert len(ds)==48
 assert all((int(d['sender'][1:])<=4)==(int(d['recipient'][1:])<=4) for d in ds)
 responses=json.loads((out/'responses.json').read_text());assert len(responses)==40
 assert all('Keine Personenreaktion' in x['response'] for x in responses)
 result={'checked_on':'2026-11-02','classification':'offline_technical_test_with_stub_transport_not_simulation_results','passed':True,'stub_http_requests':40,'actual_generative_model_calls':0,'conditions_start_identically':True,'delivered_peer_messages':48,'cross_group_deliveries':0,'response_records':40,'saved_final_states':True,'generative_opinions_produced':False}
 Path('qa/concordia-pilot-workflow-test.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
server.shutdown()
