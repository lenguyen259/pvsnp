# validation: a 27-gate circuit (star of vertex 1 written as (x1&x7)|(x1&(x9|x13)) ) must be reduced to 26
import random,sys
from lns import *
random.seed(int(sys.argv[1]))
C=[]; W=lambda: n+len(C)-1
def g(*x): C.append(x); return W()
S=[g('and',1,7)]; o=g('or',9,13); S.append(g('and',1,o))
adj={v:[] for v in range(n)}
for a,b in E: adj[a].append(b)
for v in [0,2,3,4,5,6]:
    nb=adj[v]; o=nb[0]
    for u in nb[1:]: o=g('or',o,u)
    S.append(g('and',v,o))
while len(S)>1:
    random.shuffle(S); a=S.pop(); b=S.pop(); S.append(g('or',a,b))
assert ok(C); print(len(C)); t0=time.time()
for it in range(5000):
    Wset=rand_window(C,random.randint(3,7)); pr=window_problem(C,Wset)
    if not pr or pr=='BUG': continue
    Wset,ins,outs,rows=pr
    r=synth(rows,len(ins),len(outs),len(Wset)-1,True)
    if r is None: r=synth(rows,len(ins),len(outs),len(Wset),True)
    if r is None: continue
    nc=rebuild(C,Wset,ins,outs,*r)
    if nc and ok(nc) and len(nc)<=len(C):
        if len(nc)<len(C): print('it',it,len(nc),round(time.time()-t0,1)); break
        C=nc
