"""fuzz: minimise over bad leaves v (single OR reader [+ elim(v,0)=1 if M]) the number of good options in FAM(v)."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz,os
AGG=os.environ.get('AGG','min')
from gen import *
from t3fuzz import getG,leaves,penalty,FG
def fam(g,v,which):
    u=next(iter(g.N[v])); W=g.N[u]-{v}; Nu=g.N[u]|{u}
    F={"N'v":({u},{v}),'Bu':((),{u}),"N'u":(Nu-{v},{v}),'Nv':({u,v},()),'Nu':(Nu,())}
    return {k:F[k] for k in which}
def metric(g,c,mode,which):
    p=penalty(g,c,mode)
    if p: return 100*p,None
    best=10**6; rec={}
    for v in leaves(g):
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        n=0; rr={}
        for k,(S0,S1) in fam(g,v,which).items():
            r=gopt(g,c,S0,S1)
            if r and r[2]: n+=1
            rr[k]=r
        rec[v]=rr; best=min(best,n) if AGG=='min' else (0 if best==10**6 else best)+n
    return best,rec
def search(name,mode,secs,K,seed,which,out):
    g=FG(getG(name)); rnd=random.Random(seed)
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(g,c,mode,which); best=10**9; t0=time.time(); it=0; found=[]
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(g,c2,mode,which)
        if m2==0 and len(found)<20:
            found.append(fmt(c2))
            with open(out,'a') as f: f.write(json.dumps(dict(g=name,E=g.E,c=fmt(c2),s=len(c2)-g.P,rec={str(k):v for k,v in r.items()}))+'\n')
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2; best=min(best,m)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(g,c,mode,which)
    return dict(name=name,mode=mode,which=which,best=best,it=it,nfound=len(found))
if __name__=='__main__':
    name,mode,secs,K,seed,which,out=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6].split(','),sys.argv[7]
    print(json.dumps(search(name,mode,secs,K,seed,which,out)),flush=True)
