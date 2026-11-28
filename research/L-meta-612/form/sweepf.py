import sys, json, time
from drv import run, tau
fn=sys.argv[1]; mode=sys.argv[2]; to=int(sys.argv[3]) if len(sys.argv)>3 else 900
for l in open(fn):
    E=[tuple(e) for e in json.loads(l)]
    n=max(max(e) for e in E)+1
    t=tau(n,E); t0=time.time()
    m,w=run(n,E,mode,len(E)+t,timeout=to,maxs=150000000)
    print(json.dumps(dict(n=n,E=E,tau=t,phi=len(E)+t-1,minleaves=m,w=w,sec=round(time.time()-t0,1))),flush=True)
