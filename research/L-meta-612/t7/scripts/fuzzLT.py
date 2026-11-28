"""adversarial fuzzer against T2-LT: minimise #options paid by |K u Cp u Top|-1 (and slack)."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
import fz, graphs, t3fuzz
from lib7 import *
from t2lib import red, renum, fmt, ok
t3fuzz.GR.update({'n8':[(0,1),(2,3),(0,4),(2,4),(1,5),(2,5),(0,6),(3,6),(1,7),(3,7)],'P6':[(0,1),(1,2),(2,3),(3,4),(4,5)],'C7':[(i,(i+1)%7) for i in range(7)]})
class FG(Graph):
    def ok(s,c): return ok(s,c)
def score(g,c,opts,mode):
    n=0; sl=0
    for nm,v,rho,need in opts:
        K,cp,Tp,T=parts(g,c,rho) if mode!='LR' else (0,0,0,0)
        x=(LR(g,c,rho) if mode=='LR' else (len(K|cp|Tp)-1 if mode=='LT' else len(K|cp)))-need
        if x>=0: n+=1; sl+=x+1
    return 1000*n+sl, n
def search(name,secs,K,seed,mode):
    g=FG(t3fuzz.getG(name)); rnd=random.Random(seed); opts=g.options()
    def fresh(): return renum(g.n,red(g,fz.star_circuit(g,rnd)))
    c=fresh(); m,n=score(g,c,opts,mode); best=(n,fmt(c)); t0=time.time(); it=0
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        if not c2 or not ok(g,c2): continue
        m2,n2=score(g,c2,opts,mode)
        if m2<=m or rnd.random()<0.05:
            c,m,n=c2,m2,n2
            if n<best[0] or (n==best[0] and len(c)<len(best[1].split())): best=(n,fmt(c))
            if n==0: return dict(name=name,mode=mode,found=fmt(c),size=len(c),P=g.P,it=it)
        if it%4000==0 and rnd.random()<0.3: c=fresh(); m,n=score(g,c,opts,mode)
    return dict(name=name,mode=mode,found=None,minpaid=best[0],ex=best[1],P=g.P,it=it)
if __name__=='__main__':
    name,secs,K,seed,mode=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
    print(json.dumps(search(name,secs,K,seed,mode)),flush=True)
