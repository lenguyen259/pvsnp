"""fuzz: circuits with a bad leaf v (deg u>=3, delta_v=1) where ALL local options at v,u are bad:
A(v),B(v),N(v),N'(v),A(u),B(u). Log them; metric = #good options overall (A,N,B + N'(leaf))."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz
from gen import *
from t3fuzz import getG,FG,leaves
LOC=lambda u,v:{'Av':({v},()),'Bv':((),{v}),'Nv':({u,v},()),"N'v":({u},{v}),'Au':({u},()),'Bu':((),{u})}
def locbad(g,c):
    out=[]
    for v in leaves(g):
        u=next(iter(g.N[v]))
        if len(g.N[u])<3 or g.t-tau(g.Eminus({v}))!=1: continue
        ok_=True
        for k,(S0,S1) in LOC(u,v).items():
            r=gopt(g,c,S0,S1)
            if r and r[2]: ok_=False;break
        if ok_: out.append(v)
    return out
def search(name,secs,K,seed,pool):
    g=FG(getG(name)); rnd=random.Random(seed); opts=g.options()
    def metric(c):
        L=locbad(g,c)
        if not L: return 1000,None
        r=evaluate(g,c,opts); return sum(1 for x in r if x[4]),(L,[x[:4] for x in r if x[4]])
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(c); best=10**9; t0=time.time(); it=0; seen=set(); f=open(pool,'a')
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(c2)
        if r is not None and fmt(c2) not in seen:
            seen.add(fmt(c2)); f.write(json.dumps(dict(g=name,E=g.E,c=fmt(c2),s=len(c2)-g.P,L=r[0],good=r[1]))+'\n')
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2; best=min(best,m)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(c)
    return dict(name=name,best=best,it=it,ninst=len(seen))
if __name__=='__main__':
    a=sys.argv; print(json.dumps(search(a[1],float(a[2]),int(a[3]),int(a[4]),a[5])),flush=True)
