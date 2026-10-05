"""Prueba real de HU-LP-01 a HU-LP-04 contra el stack de LOGISTPULSE."""
import argparse
import json
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime,timezone
parser=argparse.ArgumentParser()
parser.add_argument('--project',choices=['LOGISTPULSE'],required=True)
parser.add_argument('--base',default='http://localhost:8080')
parser.add_argument('--out',default='evidencias/sprint1.json')
args=parser.parse_args();steps=[]
report={'project':args.project,'date':datetime.now(timezone.utc).isoformat(),'base':args.base,'steps':steps,'result':'RUNNING'}
def request(method,path,data=None,key=None):
    headers={'Content-Type':'application/json'}
    if key: headers['X-Idempotency-Key']=key
    req=urllib.request.Request(args.base.rstrip('/')+path,data=json.dumps(data).encode() if data is not None else None,method=method,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=30) as r:return {'http':r.status,'body':json.load(r)}
    except urllib.error.HTTPError as e:
        raw=e.read().decode();
        try: body=json.loads(raw)
        except ValueError:body=raw
        return {'http':e.code,'body':body}
def check(id,result,condition):
    steps.append({'test':id,'result':'PASS' if condition else 'FAIL','response':result})
    if not condition:raise AssertionError(id)
try:
    health=request('GET','/health/fulfillment')
    check('SALUD-LP',health,health['http']==200)
    sample={'storeId':'VRJ-'+uuid.uuid4().hex[:8],'channel':'MOBILE','total':18.50}
    created=request('POST','/api/fulfillment/orders',sample)
    check('T-LP-01',created,created['http']==201 and created['body'].get('status')=='WAITING' and bool(created['body'].get('orderId')))
    ident=created['body']['orderId'];states=['WAITING'];deadline=time.monotonic()+60
    listed=False;polls=[]
    while time.monotonic()<deadline:
        listing=request('GET','/api/fulfillment/orders');rows=listing['body']
        if not listed:
            check('T-LP-02',listing,listing['http']==200 and isinstance(rows,list) and len(rows)<=20 and rows==sorted(rows,key=lambda r:r['createdAt'],reverse=True) and any(r['orderId']==ident for r in rows));listed=True
        item=next((r for r in rows if r['orderId']==ident),None)
        if item:
            observation={'state':item['status'],'updatedAt':str(item['updatedAt'])}
            if not polls or polls[-1]!=observation: polls.append(observation)
            if item['status'] not in states:states.append(item['status'])
            if item['status']=='READY':break
        time.sleep(.2)
    check('T-LP-03',{'orderId':ident,'observed':states},'PREPARING' in states)
    check('T-LP-04',{'orderId':ident,'observed':states,'polls':polls},states==['WAITING','PREPARING','READY'])
    report['result']='PASS'
except Exception as e:
    report['result']='FAIL';report['error']=str(e)
finally:
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if report['result']=='PASS' else 1)
