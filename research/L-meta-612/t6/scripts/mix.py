from lib6 import *
import itertools
for n,S in [(6,(0,1)),(8,(0,1)),(6,(0,3)),(5,(0,1,2))]:
    E,L=psun(n,S); g=Graph(E); P=sorted(L); R=runs(n,S); rv=[w for r in R for w in r]
    print(n,S,'runs',R)
    res=[]
    for assign in itertools.product('01f',repeat=len(rv)):
        A1=[w for w,a in zip(rv,assign) if a=='1']; A0=[w for w,a in zip(rv,assign) if a=='0']
        nd=gneed(g,A0,P+A1)
        if nd is None: continue
        ex=nd-2*len(P)-2*len(A1)-2*len(A0)
        res.append((ex,''.join(assign)))
    res.sort()
    print('  min excess',res[:12])
