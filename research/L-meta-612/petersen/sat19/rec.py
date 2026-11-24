# recursive gate-elimination + SAT lower bounds for induced subgraphs of Petersen
import itertools, json, subprocess, sys, time, os
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
TO=int(sys.argv[1]) if len(sys.argv)>1 else 900
MAXV=int(sys.argv[2]) if len(sys.argv)>2 else 10
RES='rec_res.json'; res=json.load(open(RES)) if os.path.exists(RES) else {}
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
classes=[]  # (graph nx, edges relabeled)
def cls_of(edges):
    if not edges: return None
    G=nx.Graph(edges); h=nx.weisfeiler_lehman_graph_hash(G,iterations=4)
    for idx,(H,hh,_) in enumerate(classes):
        if hh==h and nx.is_isomorphic(G,H): return idx
    vs=sorted(G.nodes()); m={v:i for i,v in enumerate(vs)}
    classes.append((G,h,[(m[a],m[b]) for a,b in edges])); return len(classes)-1
def induced(E,Z): return [(a,b) for a,b in E if a not in Z and b not in Z]
for r in range(10,1,-1):
    for keep in itertools.combinations(range(10),r):
        Z=set(range(10))-set(keep); cls_of(induced(PET,Z))
info={}
for idx,(G,h,E) in enumerate(classes):
    n=G.number_of_nodes(); key='%d:%s'%(idx,json.dumps(E))
    ch={}; 
    for v in range(n): ch[(v,)]=cls_of(induced(E,{v}))
    for u,w in itertools.combinations(range(n),2): ch[(u,w)]=cls_of(induced(E,{u,w}))
    if os.environ.get('TRIP')=='1':
        for t3 in itertools.combinations(range(n),3): ch[t3]=cls_of(induced(E,set(t3)))
    info[idx]=dict(n=n,E=E,m=len(E),tau=tau(E),ch=ch)
# children added during loop may have created new classes; recompute for them
for idx in range(len(classes)):
    if idx not in info:
        G,h,E=classes[idx]; n=G.number_of_nodes(); ch={}
        for v in range(n): ch[(v,)]=cls_of(induced(E,{v}))
        for u,w in itertools.combinations(range(n),2): ch[(u,w)]=cls_of(induced(E,{u,w}))
        info[idx]=dict(n=n,E=E,m=len(E),tau=tau(E),ch=ch)
order=sorted(info,key=lambda i:(info[i]['n'],info[i]['m']))
print(len(order),'classes',flush=True)
L={}
ASSUME=os.environ.get('ASSUME')=='1'
ONLY=os.environ.get('ONLY')
SIZES=os.environ.get('SIZES')
def Lof(c):
    if c is None: return 0
    if ASSUME: I=info[c]; return I['m']+I['tau']-1
    return L[c]
def solve(idx):
    I=info[idx]; E=I['E']; n=I['n']; phi=I['m']+I['tau']-1; k=json.dumps(E)
    if k in res and res[k].get('to',TO)>=TO or (k in res and res[k]['status']=='tight'): return res[k]
    lo=max(Lof(c)+1 for t,c in I['ch'].items() if len(t)==1)
    log=[]; status='tight'; lb=phi
    rng=range(lo,phi) if not SIZES else [int(x) for x in SIZES.split(',')]
    for s in rng:
        el=[[list(t),s-Lof(c)] for t,c in I['ch'].items() if c is not None]
        if any(b<0 for _,b in el): log.append((s,'triv',0)); continue
        el=[[t,b] for t,b in el if b<s]
        cmd=['python3','enc3.py',str(s),'--graph',k,'--chain','--factc','--viol','--elim',json.dumps(el)]
        if n==10: cmd.append('--symb')
        t0=time.time()
        try:
            out=subprocess.run(cmd,capture_output=True,text=True,timeout=TO).stdout
        except subprocess.TimeoutExpired:
            log.append((s,'TO',TO)); status='open'; lb=s; break
        dt=round(time.time()-t0,1)
        if 'RESULT UNSAT' in out: log.append((s,'UNSAT',dt)); continue
        if 'RESULT SAT' in out:
            log.append((s,'SAT',dt,[l for l in out.splitlines() if 'VERIF' in l])); status='BELOW_PHI'; lb=s; break
        log.append((s,'ERR',out[-300:])); status='err'; lb=s; break
    r=dict(E=E,n=n,m=I['m'],tau=I['tau'],phi=phi,lo=lo,lb=lb,status=status,log=log,to=TO)
    return r
if ONLY:
    for i in order:
        if info[i]['n']==int(ONLY.split(':')[0]) and info[i]['m']==int(ONLY.split(':')[1]):
            r=solve(i); print('ONLY',i,r,flush=True)
    sys.exit()
levels={}
for i in order: levels.setdefault(info[i]['n'],[]).append(i)
for nv in sorted(levels):
    if nv>MAXV: break
    with ThreadPoolExecutor(2) as ex:
        rs=list(ex.map(solve,levels[nv]))
    for i,r in zip(levels[nv],rs):
        L[i]=r['lb']; res[json.dumps(info[i]['E'])]=r
        print(nv,i,'m',r['m'],'tau',r['tau'],'phi',r['phi'],'lo',r['lo'],'LB',r['lb'],r['status'],r['log'],flush=True)
    json.dump(res,open(RES,'w'))
