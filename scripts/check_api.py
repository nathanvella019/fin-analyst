"""Check the running API against known notebook examples (not a load test)."""
import argparse
import json
from pathlib import Path
import urllib.error
import urllib.request

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url',default='http://127.0.0.1:8008')
args=parser.parse_args()
cases=[
 ("What was Birner Dental Management Services's revenue in fiscal 2015?",200,63843837),
 ("What was Solera Holdings's revenue for the quarter ended 31 December 2015?",200,308045000),
 ("What was Futurefuel's sales for the quarter ended 30 September 2016?",200,69306000),
 ("tell me a joke",200,None),
 ("What were Apple's assets at 31 February 2016?",422,None),
]
records=[]
for question,status,value in cases:
 request=urllib.request.Request(args.url+'/ask',data=json.dumps({'question':question}).encode(),headers={'Content-Type':'application/json'})
 try:
  response=urllib.request.urlopen(request,timeout=120)
 except urllib.error.HTTPError as error:
  response=error
 with response:
  body=json.load(response)
  assert response.status==status,(question,response.status)
 if status==200:
  assert body['candidate']['value']==value,(question,body)
  assert body['decision']=='refer'
  assert body['answer'] is None
 records.append({'question':question,'status_code':status,'response':body})
 print(f'PASS {status}: {question}')
folder=Path('data/evaluation');folder.mkdir(parents=True,exist_ok=True)
(folder/'docker_api_checks.json').write_text(json.dumps(records,indent=2)+'\n')
local=folder/'local_api_checks.json'
if local.exists():
 assert records==json.loads(local.read_text()),'Local and container responses differ'
 print('All five container responses exactly match saved local API responses.')
