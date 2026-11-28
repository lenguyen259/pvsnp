"""fuzz struct-3 (min-cex reader structure) circuits on partial suns; minimise best margin of family PB
(x_{P u B}:=1, B indep subset of run vertices). Also run-vertex reader constraints (Cor M.4)."""
import sys,random,json,time,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz
from lib6 import *
class FG(Graph):
    def ok(s,c): return ok(s,c)
def setup(n,S):
    E,L=psun(n,S); g=FG(E); P=list(L); R=runs(n,S); rv=[w for r in R for w in r]
    fam=[]
    for r in range(len(rv)+1):
        for B in itertools.combinations(rv,r):
            sub={x:('c',1) for x in P+list(B)}; nd=need_sub(g,sub)
            if nd is None or nd=='bad': continue
            fam.append((B,sub,nd))
    nb={w:gneed(g,[],[w]) for w in rv}
    return g,P,L,R,rv,fam,nb
def pen(g,c,P,L,rv,nb):
    p=0
    for v in P:
        u=L[v]; rd=[x for x in c if v in x[2:]]
        if len(rd)!=1 or rd[0][1]!='|': p+=1; continue
        rg=[x for x in c if rd[0][0] in x[2:]]
        if len(rg)!=1 or rg[0][1]!='&': p+=1
        if sum(1 for x in c if u in x[2:])!=1: p+=1
    for w in rv:
        rd=[x for x in c if w in x[2:]]; ka=sum(1 for x in rd if x[1]=='&'); ko=len(rd)-ka
        if len(rd)+min(ka,2)>2: p+=1
        if len(rd)+min(ko,2)>nb[w]-1: p+=1
    return p
def margin(g,c,fam):
    best=-99; arg=None
    for B,sub,nd in fam:
        d=elim_sub(g,c,sub)-nd
        if d>best: best,arg=d,B
    return best,arg
def search(n,S,secs,K,seed,pool,minsize=0):
    g,P,L,R,rv,fam,nb=setup(n,S); rnd=random.Random(seed); name='psun:%d:%s'%(n,','.join(map(str,S)))
    def met(c):
        p=pen(g,c,P,L,rv,nb)
        if p: return 100*p+len(c)-g.P,None
        m,B=margin(g,c,fam); return m*10+ (len(c)-g.P),(m,B)
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=met(c); best=10**9; t0=time.time(); it=0; seen=set(); f=open(pool,'a'); nrec=0
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=met(c2)
        if r is not None:
            k=fmt(c2)
            if k not in seen:
                seen.add(k); nrec+=1
                f.write(json.dumps(dict(g=name,c=k,s=len(c2)-g.P,m=r[0],B=r[1]))+'\n'); f.flush()
        if m2<=m or rnd.random()<0.05:
            c,m=c2,m2; best=min(best,m)
        if it%4000==0 and rnd.random()<0.3: c=fresh(); m,_=met(c)
    return dict(name=name,best=best,it=it,rec=nrec)
if __name__=='__main__':
    a=sys.argv; n=int(a[1]); S=[int(x) for x in a[2].split(',')]
    print(json.dumps(search(n,S,float(a[3]),int(a[4]),int(a[5]),a[6])),flush=True)
