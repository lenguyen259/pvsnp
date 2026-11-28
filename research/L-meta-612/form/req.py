import itertools, subprocess, sys, json, os
from drv import vecs
n=int(sys.argv[1]); E=[tuple(sorted(e)) for e in eval(sys.argv[2])]; K=int(sys.argv[3])
g,T=vecs(n,E,'slice')
pts=[1<<i for i in range(n)]+[(1<<a)|(1<<b) for a,b in itertools.combinations(range(n),2)]
idx={p:k for k,p in enumerate(pts)}
env=dict(os.environ,DUMP='dump.txt')
subprocess.run(['./fdp',str(K),'20000000',str(n)]+['%x'%x for x in g]+['0'],env=env,capture_output=True)
funcs=[(int(a,16),int(b)) for a,b in (l.split() for l in open('dump.txt'))]
print('funcs',len(funcs))
Es=set(E); NE=[p for p in itertools.combinations(range(n),2) if p not in Es]
def bit(p): return 1<<idx[(1<<p[0])|(1<<p[1])]
def sbit(u): return 1<<idx[1<<u]
def Lreq(Xm,Ym):
    best=99
    for f,l in funcs:
        if f&Xm==Xm and f&Ym==0 and l<best: best=l
    return best
def mu(X,Ys):
    X2=[e for e in X if e[0] in Ys and e[1] in Ys]
    X1=[e for e in X if (e[0] in Ys)!=(e[1] in Ys)]
    X0=[e for e in X if e[0] not in Ys and e[1] not in Ys]
    forced={e[1] if e[0] in Ys else e[0] for e in X1}
    rest=[e for e in X0+X2 if e[0] not in forced and e[1] not in forced]
    for k in range(n+1):
        for Tt in itertools.combinations(range(n),k):
            if all(a in Tt or b in Tt for a,b in rest): return len(X2)+len(forced)+k
res=[]
for xs in range(1,1<<len(E)):
    X=[E[i] for i in range(len(E)) if xs>>i&1]
    Xm=sum(bit(e) for e in X)
    for ys in range(1<<n):
        Ys=[u for u in range(n) if ys>>u&1]
        cand=[p for p in NE if p[0] in Ys and p[1] in Ys]
        for ns in range(1<<len(cand)):
            Yn=[cand[i] for i in range(len(cand)) if ns>>i&1]
            Ym=sum(sbit(u) for u in Ys)+sum(bit(p) for p in Yn)
            L=Lreq(Xm,Ym); m=mu(X,set(Ys))
            res.append((X,Ys,Yn,L,m))
json.dump(res,open('req_%s.json'%sys.argv[4],'w'))
bad=[r for r in res if r[3]<r[4]]
print(len(res),'L<mu:',len(bad))
for r in bad[:15]: print(r)
