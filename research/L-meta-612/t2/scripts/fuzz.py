import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz
from t2lib import *
class FG(Graph):
    def ok(s,c): return ok(s,c)
GR={'net':[(0,4),(1,5),(2,3),(3,4),(3,5),(4,5)],
 'bull':[(0,1),(0,2),(1,2),(0,3),(1,4)],
 '2tri+bridge':[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)],
 'constrS7':[(0,1),(0,4),(0,5),(1,2),(1,4),(2,6),(3,5),(3,6),(5,6)],
 'n8':[(0,1),(2,3),(0,4),(2,4),(1,5),(2,5),(0,6),(3,6),(1,7),(3,7)],
 'P6':[(0,1),(1,2),(2,3),(3,4),(4,5)],
 'C7':[(i,(i+1)%7) for i in range(7)],
 'Pet-v':[(0,1),(0,5),(1,2),(1,6),(2,3),(2,7),(3,8),(4,6),(4,7),(5,7),(5,8),(6,8)],
 'Pet':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)],
 'C5':[(i,(i+1)%5) for i in range(5)],
 'P5':[(0,1),(1,2),(2,3),(3,4)],
 'C5+p':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5)],
 'C5+2p':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(2,6)],
 'sun5':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9)],
 'C6+2p':[(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(3,7)],
 'paw+':[(0,1),(1,2),(0,2),(0,3),(1,4),(2,5)]}
def metric(g,c,kinds,opts):
    if kinds=='CYC':
        n=sum(1 for v in g.sup if charged(g,c,v)>=2 and (lo_bounds(g,c,{v},0)>=3 or lo_bounds(g,c,{v},1)>=4))
        return n,None
    if kinds in ('J1','J2','J3','JA'):
        n1,n2,n3,na=viol_counts(g,c); j={'J1':n1,'J2':n2,'J3':n3,'JA':na}[kinds]
        return max(0,len(c)-g.P-j+1),None
    if kinds=='LO':
        n=0
        for name,v,rho,need in opts:
            X={v} if name!='N' else g.N[v]|{v}
            L=lo_bounds(g,c,X,0 if name!='B' else 1)
            if L>=need: n+=1
        return n,None
    oo=[o for o in opts if o[0] in kinds]
    if kinds.startswith('m'):
        S=set()
        for i in minimal_ands(c): S|=support(g,c,i)
        oo=[o for o in oo if o[1] in S]
    r=evaluate(g,c,oo)
    return sum(1 for x in r if x[4]),r
def search(name,kinds,secs,K,seed):
    g=FG(GR[name]); rnd=random.Random(seed); opts=g.options()
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(g,c,kinds,opts); best=m; t0=time.time(); it=0
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(g,c2,kinds,opts)
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2
            if m<best: best=m
            if m==0:
                return dict(name=name,kinds=kinds,found=fmt(c),size=len(c),P=g.P,nand=nand(c),it=it,t=time.time()-t0)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(g,c,kinds,opts)
    return dict(name=name,kinds=kinds,found=None,best=best,it=it)
if __name__=='__main__':
    name,kinds,secs,K,seed=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
    print(json.dumps(search(name,kinds,secs,K,seed)),flush=True)
