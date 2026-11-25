import random
from lns import *
random.seed(3)
C=star('left')
# bloat: replace each star v & OR(nb) by OR of (v & u)  (dnf), size |E| + |E|-1 = 39
C=[]; T=[]
for a,b in E:
    C.append(('and',a,b)); T.append(n+len(C)-1)
while len(T)>1:
    a=T.pop(0); b=T.pop(0); C.append(('or',a,b)); T.append(n+len(C)-1)
assert ok(C); print(len(C))
t0=time.time()
for it in range(3000):
    Wset=rand_window(C,random.randint(3,7)); pr=window_problem(C,Wset)
    if not pr or pr=='BUG': continue
    Wset,ins,outs,rows=pr
    r=synth(rows,len(ins),len(outs),len(Wset)-1,True)
    if r is None: r=synth(rows,len(ins),len(outs),len(Wset),True)
    if r is None: continue
    nc=rebuild(C,Wset,ins,outs,*r)
    if nc and ok(nc) and len(nc)<=len(C):
        if len(nc)<len(C): print(it,len(nc),round(time.time()-t0))
        C=nc
    if len(C)<=26: break
