"""t3 fuzzer: Corollary-M-like circuits (every leaf: single OR reader, elim(v,0)=1) on bad-leaf graphs.
metric = 100*penalty + #good options (in family). Records all P=0 circuits seen to a jsonl pool."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
import fz
from t2lib import *
from psun import psun
class FG(Graph):
    def ok(s,c): return ok(s,c)
GR={'net':[(0,4),(1,5),(2,3),(3,4),(3,5),(4,5)],
 '2tri+bridge':[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)],
 'constrS7':[(0,1),(0,4),(0,5),(1,2),(1,4),(2,6),(3,5),(3,6),(5,6)],
 'sun5':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9)],
 'C5+2p':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(2,6)],
 'C6+2p':[(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(3,7)],
 'spider':[(0,1),(1,2),(1,3),(2,4),(3,5)],
}
def getG(name):
    if name in GR: return GR[name]
    # psun:n:s1,s2,..
    _,n,S=name.split(':'); return psun(int(n),[int(x) for x in S.split(',')])[0]
def leaves(g): return [v for v in g.sup if len(g.N[v])==1]
def penalty(g,c,mode):
    p=0
    for v in leaves(g):
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        rd=[x for x in c if v in x[2:]]
        if len(rd)!=1 or rd[0][1]!='|': p+=1; continue
        if mode in ('M','ML','M2') and elim(g,c,{v:0})!=1: p+=1; continue
        if mode=='M2' and elim(g,c,{v:1})>=len(g.N[u]): p+=1
    return p
def metric(g,c,mode,opts):
    p=penalty(g,c,mode)
    if p: return 100*p,None
    r=evaluate(g,c,opts)
    if mode in ('ML','SL'):
        good={(x[0],x[1]) for x in r if x[4]}; best=10**6
        for v in leaves(g):
            u=next(iter(g.N[v]))
            if len(g.N[u])<3: continue
            best=min(best,sum(1 for k in [('N',v),('B',u),('A',u)] if k in good))
        return best,r
    return sum(1 for x in r if x[4]),r
def search(name,mode,secs,K,seed,pool):
    g=FG(getG(name)); rnd=random.Random(seed); opts=g.options()
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(g,c,mode,opts); best=10**9; t0=time.time(); it=0; nrec=0; seen=set()
    f=open(pool,'a')
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(g,c2,mode,opts)
        if r is not None:
            k=fmt(c2)
            if k not in seen:
                seen.add(k); nrec+=1
                f.write(json.dumps(dict(g=name,E=g.E,c=k,s=len(c2)-g.P,good=[[x[0],x[1],x[2],x[3]] for x in r if x[4]]))+'\n')
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2
            best=min(best,m)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(g,c,mode,opts)
    f.close()
    return dict(name=name,mode=mode,best=best,it=it,rec=nrec)
if __name__=='__main__':
    name,mode,secs,K,seed,pool=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
    print(json.dumps(search(name,mode,secs,K,seed,pool)),flush=True)
