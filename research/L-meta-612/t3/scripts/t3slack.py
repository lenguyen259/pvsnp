"""slack fuzz: for bad leaves v with single OR reader, margin(v)=max_{X in FAM(v)} (elim-need) + (s-Phi+1).
minimise min_v margin(v); <0 refutes the slack per-leaf lemma."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz
from gen import *
from t3fuzz import getG,leaves,FG
def FAM(g,v,which):
    u=next(iter(g.N[v])); Nu=g.N[u]|{u}
    F={"N'v":({u},{v}),'Bu':((),{u}),"N'u":(Nu-{v},{v}),'Nv':({u,v},()),'Nu':(Nu,()),'Av':({v},()),'Bv':((),{v}),'Au':({u},())}
    for i,w in enumerate(sorted(g.N[u]-{v})):
        F['Aw%d'%i]=({w},()); F['Bw%d'%i]=((),{w}); F['Nw%d'%i]=(g.N[w]|{w},())
    if which==['ALLW']: return F
    return {k:F[k] for k in which if k in F}
def badleaves(g,c):
    out=[]
    for v in leaves(g):
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        if g.t-tau(g.Eminus({v}))!=1: continue
        rd=[x for x in c if v in x[2:]]
        if len(rd)==1 and rd[0][1]=='|': out.append(v)
    return out
def metric(g,c,which):
    B=badleaves(g,c)
    if not B: return 10**6,None
    sl=len(c)-g.P+1; best=10**6; rec={}
    for v in B:
        mm=-10**6; rr={}
        for k,(S0,S1) in FAM(g,v,which).items():
            r=gopt(g,c,S0,S1)
            if r: mm=max(mm,r[0]-r[1]); rr[k]=r[:2]
        rec[v]=rr; best=min(best,mm+sl)
    return best,rec
def search(name,secs,K,seed,which,out):
    g=FG(getG(name)); rnd=random.Random(seed)
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(g,c,which); best=10**9; t0=time.time(); it=0; nf=0
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(g,c2,which)
        if m2<0 and nf<10:
            nf+=1
            with open(out,'a') as f: f.write(json.dumps(dict(g=name,E=g.E,c=fmt(c2),s=len(c2)-g.P,m=m2,rec={str(k):v for k,v in r.items()}))+'\n')
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2; best=min(best,m)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(g,c,which)
    return dict(name=name,which=which,best=best,it=it,nfound=nf)
if __name__=='__main__':
    name,secs,K,seed,which,out=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5].split(','),sys.argv[6]
    print(json.dumps(search(name,secs,K,seed,which,out)),flush=True)
