import collections, random, sys
from sat import solve
from batch import G, tau
from core import *
random.seed(1)
st=collections.Counter()
def check(n,E,Cg):
    C=[(op,a,b) for op,a,b in Cg]
    R=dedead(n,C,n+len(C)-1)[1]
    assert evalc(n,R)[-1]==fG(n,E)
    if nand(R)<tau(n,E): st['TAUVIOL']+=1; print('TAUVIOL',E,R)
    analyze(n,R,E,st); st['circ']+=1
def inflate(n,C,k):
    # add redundant gates: replace output o by o OR (o AND g) / insert g' = g AND (g OR h) etc, keeps function
    C=list(C)
    for _ in range(k):
        N=n+len(C); g=random.randrange(N); h=random.randrange(N)
        if g==h: continue
        typ=random.random()
        # new gate h2 = g OR h ; g2 = g AND h2 (==g); redirect one reader of g (later gate) to g2 -- must insert before reader: append at end only works for output
        # simpler: rebuild output: out' = out OR (out AND h) or out AND (out OR h)
        o=N-1
        if typ<0.5: C.append(('AND',o,h)); C.append(('OR',o,N))
        else: C.append(('OR',o,h)); C.append(('AND',o,N))
    return C
names=sys.argv[1:]
for nm in names:
    n,E=G[nm]; t=tau(n,E); m=len(E)
    for s in range(m-1+t, m-1+t+3):
        sols=solve(n,E,s,s,limit=150)
        for C in sols:
            Cg=[(op,a,b) for op,a,b in C]
            check(n,E,Cg)
            for k in (1,2): check(n,E,inflate(n,Cg,k))
    print(nm,dict(st),flush=True)
