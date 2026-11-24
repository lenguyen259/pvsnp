import sys,random,json,time
from fz import *
def margins(g,c):
    a0,o0,so,sa,R=g.stats(c)
    md=min(g.deg.values())
    gOR=[v for v in g.sup if so[v]>=g.needOR[v]]
    return dict(OR=len(gOR),ORmin=sum(1 for v in gOR if g.deg[v]==md),
                AND=sum(1 for v in g.sup if sa[v]>=g.needAND[v]),
                TOT=sum(1 for v in g.sup if so[v]+sa[v]>=g.needP[v]),size=a0+o0,nor=o0,nand=a0,
                so=so,sa=sa,M0=sum(1 for v in g.sup if sa[v]>=1),CHmin=sum(1 for v in g.sup if g.deg[v]==md and g.ch[v]>=g.deg[v]))
def search(E,target,secs,K,seed):
    rnd=random.Random(seed); g=G(E)
    def fresh():
        c=star_circuit(g,rnd); return renum(g.n,redc(g.n,c,g.X)[2])
    c=fresh(); m=margins(g,c); t0=time.time(); found=[]; it=0; acc=0; best=m[target]
    while time.time()-t0<secs:
        it+=1
        c2=mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        m2=margins(g,c2)
        if m2[target]<=m[target] or rnd.random()<0.1:
            c,m=c2,m2; acc+=1; best=min(best,m[target])
            if m[target]==0:
                found.append(({k:m[k] for k in ('size','nor','nand','so','sa')},' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c))); break
        if it%2000==0 and rnd.random()<0.2: c=fresh(); m=margins(g,c)
    return found,it,acc,best
if __name__=='__main__':
    E=json.loads(sys.argv[1]); target=sys.argv[2]; secs=float(sys.argv[3]); K=int(sys.argv[4]); seed=int(sys.argv[5])
    f,it,acc,best=search(E,target,secs,K,seed)
    print(json.dumps(dict(E=E,target=target,K=K,seed=seed,it=it,acc=acc,best=best,found=f)),flush=True)
