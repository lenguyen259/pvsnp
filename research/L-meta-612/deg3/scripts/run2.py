import sys,random,json,time
from fz import *
from lib import tau,phi
class G2(G):
    def __init__(s,E):
        G.__init__(s,E)
        s.N={v:{b for a,b in s.E if a==v}|{a for a,b in s.E if b==v} for v in s.sup}
        s.EN={v:[e for e in s.E if e[0] not in s.N[v]|{v} and e[1] not in s.N[v]|{v}] for v in s.sup}
        s.needPN={v:s.P-phi(s.EN[v]) for v in s.sup}
        s.needAN={v:s.t-tau(s.EN[v]) if s.EN[v] else None for v in s.sup}
        s.star=(s.t==1)
def marg(g,c,target):
    a0,o0,R,out=redc(g.n,c,g.X)
    so={};sa={}
    for v in g.sup:
        a1,o1,_,_=redc(g.n,R,g.X,{v:0}); so[v]=o0-o1; sa[v]=a0-a1
    r=dict(size=a0+o0,nor=o0,nand=a0,so=so,sa=sa)
    if target=='OR': r['OR']=sum(1 for v in g.sup if so[v]>=g.needOR[v])
    if target in ('ORpair','ANDpair'):
        import itertools
        cntg=0
        for X in itertools.combinations(g.sup,2):
            EX=[e for e in g.E if e[0] not in X and e[1] not in X]
            if not EX: continue
            a1,o1,_,_=redc(g.n,R,g.X,{x:0 for x in X})
            e=len(g.E)-len(EX)
            if target=='ORpair' and o0-o1>=e: cntg+=1
            if target=='ANDpair' and a0-a1>=g.t-tau(EX): cntg+=1
        if target=='ORpair': cntg+=sum(1 for v in g.sup if so[v]>=g.needOR[v])
        else: cntg+=sum(1 for v in g.sup if sa[v]>=g.needAND[v] and g.Ev[v])
        r[target]=cntg
    if target=='ORcnt': r['ORcnt']=max(0,o0-len(g.E)+2)
    if target=='ORcnt2': r['ORcnt2']=max(0,o0-len(g.E)+3)
    if target=='M0': r['M0']=sum(1 for v in g.sup if sa[v]>=1)
    if target=='ANDcnt': r['ANDcnt']=max(0,a0-g.t+1)
    if target=='SIZE': r['SIZE']=max(0,a0+o0-g.P+1)
    if target in ('TOT2','AND2'):
        sN={};aN={}
        for v in g.sup:
            if not g.EN[v]: continue
            a1,o1,_,_=redc(g.n,R,g.X,{u:0 for u in g.N[v]|{v}}); sN[v]=a0+o0-a1-o1; aN[v]=a0-a1
        if target=='TOT2':
            r['TOT2']=sum(1 for v in g.sup if (so[v]+sa[v]>=g.needP[v] and (g.Ev[v] or g.star))) + sum(1 for v in sN if sN[v]>=g.needPN[v])
        else:
            r['AND2']=sum(1 for v in g.sup if sa[v]>=g.needAND[v] and g.Ev[v]) + sum(1 for v in aN if aN[v]>=g.needAN[v])
        r['sN']=sN; r['aN']=aN
    return r
def search(E,target,secs,K,seed):
    rnd=random.Random(seed); g=G2(E)
    def fresh():
        c=star_circuit(g,rnd); return renum(g.n,redc(g.n,c,g.X)[2])
    c=fresh(); m=marg(g,c,target); t0=time.time(); found=[]; it=0; best=m[target]
    while time.time()-t0<secs:
        it+=1
        c2=mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        m2=marg(g,c2,target)
        if m2[target]<=m[target] or rnd.random()<0.1:
            c,m=c2,m2; best=min(best,m[target])
            if m[target]==0:
                found.append(({k:m[k] for k in m if k!=target},' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c))); break
        if it%2000==0 and rnd.random()<0.2: c=fresh(); m=marg(g,c,target)
    return found,it,best
if __name__=='__main__':
    E=json.loads(sys.argv[1]); target=sys.argv[2]; secs=float(sys.argv[3]); K=int(sys.argv[4]); seed=int(sys.argv[5])
    f,it,best=search(E,target,secs,K,seed)
    print(json.dumps(dict(E=E,target=target,K=K,seed=seed,it=it,best=best,found=f)),flush=True)
