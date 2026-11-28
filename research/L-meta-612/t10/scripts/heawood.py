# per-node potential W2 refuted on the Heawood graph (girth 6): node p = OR(points) & OR(lines)
from lib10 import *
from t2lib import sing, ok, red, renum, fmt
lines=[(0,1,3),(1,2,4),(2,3,5),(3,4,6),(4,5,0),(5,6,1),(6,0,2)]
E=[(p,7+i) for i,L in enumerate(lines) for p in L]
g=Graph(E,14); print('girth5',girth5(g),'|E|',len(E),'tau',g.t,'Phi',g.P)
c=[];nx=[14]
def G(o,a,b): i=nx[0]; nx[0]+=1; c.append((i,o,a,b)); return i
def OR(xs):
    x=xs[0]
    for y in xs[1:]: x=G('|',x,y)
    return x
p=G('&',OR(list(range(7))),OR(list(range(7,14))))
# star circuit on centres = lines
U=OR([G('&',7+i,OR(list(L))) for i,L in enumerate(lines)])
out=G('&',p,U)
print('correct',ok(g,c),'size',len(c))
T=tables(g,c,{})
S=sing(g,T,p); Ep=[e for e in g.E if (T[p]>>((1<<e[0])|(1<<e[1])))&1 and e[0] not in S and e[1] not in S]
cone=[x for x in c if x[0]<=p]
print('node p: |E_p|=',len(Ep),'|S_p|=',len(S),'#OR in cone',sum(1 for x in cone if x[1]=='|'),'W2 needs',len(Ep)+len(S)-1)
r=renum(14,red(g,c)); print('reduced size',len(r), 'p still present:', any(x[1]=='&' and len(sing(g,tables(g,r,{}),x[0]))==0 for x in r))
