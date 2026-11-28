# SAT search: circuit of size s computing f_G with ch(v) <= deg(v)-1 for every v (Boolean domination)
import sys, json, time
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from mcsat import target_tt
from lib import phiE
SL=int(sys.argv[3]) if len(sys.argv)>3 else 0
E=[tuple(e) for e in json.loads(sys.argv[1])]; X=int(sys.argv[2])
n=max(max(e) for e in E)+1; s=phiE(E)+X; t0=time.time()
tt=target_tt(n,E); rows=range(1<<n)
pool=IDPool(); cl=[]; N=n+s
pairs={i:[(j,k) for j in range(i) for k in range(j+1,i)] for i in range(n,N)}
sel=lambda i,p: pool.id(('s',i,p)); op=lambda i: pool.id(('o',i))
def val(i,r):
    if i<n: return bool((r>>i)&1)
    return pool.id(('v',i,r))
def add(lits):
    out=[]
    for l in lits:
        if l is True: return
        if l is False: continue
        out.append(l)
    cl.append(out)
def neg(l):
    if l is True: return False
    if l is False: return True
    return -l
for i in range(n,N):
    lits=[sel(i,p) for p in range(len(pairs[i]))]; cl.append(lits)
    cl.extend(CardEnc.atmost(lits=lits,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for p,(j,k) in enumerate(pairs[i]):
        sp=sel(i,p); o=op(i)
        for r in rows:
            a,b,c=val(j,r),val(k,r),val(i,r)
            add([-sp,-o,neg(a),neg(b),c]); add([-sp,-o,a,neg(c)]); add([-sp,-o,b,neg(c)])
            add([-sp,o,neg(a),c]); add([-sp,o,neg(b),c]); add([-sp,o,a,b,neg(c)])
out=N-1
for r in rows: add([val(out,r)] if tt[r] else [neg(val(out,r))])
for g in range(n,N-1):
    cl.append([sel(i,p) for i in range(g+1,N) for p,(j,k) in enumerate(pairs[i]) if g in (j,k)])
for i in range(n,N-1):
    for p,(j,k) in enumerate(pairs[i]):
        for q,(j2,k2) in enumerate(pairs[i+1]):
            if i not in (j2,k2) and (j2,k2)<(j,k): cl.append([-sel(i,p),-sel(i+1,q)])
# no gate equal to an earlier node (Boolean), no constant gate
for i in range(n,N):
    for j in range(i):
        d=pool.id(('d',i,j)); lits=[-d]
        for r in rows:
            # d -> exists r with val differ ; encode diff var
            x=pool.id(('x',i,j,r)); lits.append(x)
            a,b=val(i,r),val(j,r)
            add([-x,a,b]); add([-x,neg(a),neg(b)])
        cl.append(lits); cl.append([d])
sup=sorted({x for e in E for x in e})
deg={v:sum(1 for e in E if v in e) for v in sup}
for v in [v for v in sup if deg[v]==2]:
    zr=[r for r in rows if not (r>>v)&1]
    def dom(q):
        if q<n: return q==v
        dq=pool.id(('dom',q,v))
        add([dq]+[val(q,r) for r in zr]); return dq
    D={q:dom(q) for q in range(N)}
    chs=[]
    for i in range(n,N):
        ch=pool.id(('ch',i,v)); chs.append(ch)
        for p,(j,k) in enumerate(pairs[i]):
            for q in (j,k):
                add([-sel(i,p),op(i),neg(D[q]) if not isinstance(D[q],bool) else (False if D[q] else True),ch])
    cl.extend(CardEnc.atmost(lits=chs,bound=1+SL,vpool=pool,encoding=EncType.seqcounter).clauses)
S=Cadical153(bootstrap_with=cl); res=S.solve(); model=None
if res:
    m=set(l for l in S.get_model() if l>0); model=[]
    for i in range(n,N):
        for p,(j,k) in enumerate(pairs[i]):
            if sel(i,p) in m: model.append((i,'&' if op(i) in m else '|',j,k))
print(json.dumps(E),X,res,model,'%.0fs'%(time.time()-t0),flush=True)
