import random, collections
from core import *
random.seed(7); st=collections.Counter()
for it in range(30000):
    n=random.randint(3,6); s=random.randint(2,14)
    C=[]
    for g in range(n,n+s):
        a,b=random.sample(range(g),2); C.append((random.choice(['AND','OR']),a,b))
    C=dedead(n,C,n+s-1)[1]
    if not C: continue
    V=evalc(n,C); N=n+len(C); M=(1<<(1<<n))-1; f=V[-1]
    for v in range(n):
        q=set()
        for g,(op,a,b) in enumerate(C,start=n):
            ina=lambda x: x==v or x in q
            if (op=='OR' and (ina(a) or ina(b))) or (op=='AND' and ina(a) and ina(b)): q.add(g)
        if q!={g for g in range(n,N) if V[g]>>(1<<v)&1}: st['Qmis']+=1
        ex=[g for g,(op,a,b) in enumerate(C,start=n) if op=='AND' and g not in q and (a in q or b in q or a==v or b==v)]
        R=restrict(n,C,{v:1}); drop=nand(C)-nand(R)
        if drop< len(ex)+sum(C[g-n][0]=='AND' for g in q): st['exfail']+=1
        fv1=func(n,R)
        dep = any((f>>r&1)!=(f>>(r|1<<v)&1) for r in range(1<<n))
        if dep and fv1!=M:
            st['X1cases']+=1
            if drop<1: st['X1fail']+=1
            if not ex: st['noexit']+=1
        # x_v:=0 with AND reader
        if any(op=='AND' and v in (a,b) for op,a,b in C):
            if nand(C)-nand(restrict(n,C,{v:0}))<1: st['zfail']+=1
    st['circ']+=1
print(dict(st))
