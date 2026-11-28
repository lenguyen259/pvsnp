"""fuzz for config (2): minimal AND x_a&x_b, F_a,F_b>=2, A,B bad at a and b. metric: #good in {N(a),N(b)} (min over such gates).
also logs every config instance (deduped) to pool."""
import sys,random,json,time
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/deg3/scripts')
import fz
from gen import *
from t3fuzz import getG,FG
def configs(g,c,opts):
    out=[]
    for i,o,j,k in c:
        if o!='&' or j>=g.n or k>=g.n: continue
        a,b=j,k
        Fa=sum(1 for x in c if a in x[2:]); Fb=sum(1 for x in c if b in x[2:])
        if Fa<2 or Fb<2: continue
        bad=True
        for w in (a,b):
            for nm,rho in (('A',{w:0}),('B',{w:1})):
                nd=opts[(nm,w)]
                if nd is not None and elim(g,c,rho)>=nd: bad=False;break
            if not bad: break
        if bad: out.append((i,a,b,Fa,Fb))
    return out
def search(name,secs,K,seed,pool,mode):
    g=FG(getG(name)); rnd=random.Random(seed)
    opts={}
    for nm,v,rho,need in g.options(): opts[(nm,v)]=need
    for v in g.sup:
        for nm in 'ANB': opts.setdefault((nm,v),None)
    def metric(c):
        cf=configs(g,c,opts)
        if not cf: return 100,None
        best=10**6; rec=[]
        for i,a,b,Fa,Fb in cf:
            n=0; rr={}
            for w in (a,b):
                nd=opts[('N',w)]
                if nd is None: continue
                e=elim(g,c,{x:0 for x in g.N[w]|{w}}); rr[w]=(e,nd)
                if e>=nd: n+=1
            if mode=='any':
                n=sum(1 for x in evaluate(g,c) if x[4])
            best=min(best,n); rec.append((i,a,b,Fa,Fb,rr))
        return best,rec
    def fresh():
        c=fz.star_circuit(g,rnd); return renum(g.n,red(g,c))
    c=fresh(); m,_=metric(c); best=10**9; t0=time.time(); it=0; seen=set()
    f=open(pool,'a')
    while time.time()-t0<secs:
        it+=1
        c2=fz.mutate(g,c,rnd,g.P+K)
        if c2 is None or len(c2)>g.P+K: continue
        c2=renum(g.n,red(g,c2))
        m2,r=metric(c2)
        if r is not None and fmt(c2) not in seen:
            seen.add(fmt(c2)); f.write(json.dumps(dict(g=name,E=g.E,c=fmt(c2),s=len(c2)-g.P,m=m2,rec=r))+'\n')
        if m2<=m or rnd.random()<0.08:
            c,m=c2,m2; best=min(best,m)
        if it%3000==0 and rnd.random()<0.3: c=fresh(); m,_=metric(c)
    f.close()
    return dict(name=name,best=best,it=it,ninst=len(seen))
if __name__=='__main__':
    a=sys.argv
    print(json.dumps(search(a[1],float(a[2]),int(a[3]),int(a[4]),a[5],a[6] if len(a)>6 else 'N')),flush=True)
