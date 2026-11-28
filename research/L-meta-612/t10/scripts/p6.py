# per-node cone potential: #OR in cone(p) >= |P_p|+|S_p|-1
from lib10 import *
from t2lib import sing, starall_viol
st=collections.Counter(); ex={}
for src,g,c in corpus(only_g5=False):
    if not c4free(g): continue
    T=tables(g,c,{}); gate={x[0]:x for x in c}
    clean=not any(t=='N3' for i,t in starall_viol(g,c))
    cone={u:frozenset() for u in range(g.n)}
    for i,o,j,k in c: cone[i]=cone[j]|cone[k]|({i} if o=='|' else frozenset())
    kind=('g5' if girth5(g) else 'tri', 'clean' if clean else 'junk')
    st[kind]+=1; bad1=bad2=False
    for i,o,j,k in c:
        S=sing(g,T,i)
        P=[(a,b) for a in range(g.n) for b in range(a+1,g.n) if a not in S and b not in S and (T[i]>>((1<<a)|(1<<b)))&1]
        PE=[e for e in P if e in g.E]
        w1=len(P)+len(S)-1; w2=len(PE)+len(S)-1
        if len(cone[i])<w1: bad1=True
        if len(cone[i])<w2: bad2=True
    for nm,b in (('W1',bad1),('W2',bad2)):
        if b:
            st[(kind,nm)]+=1
            if (kind,nm) not in ex or len(c)<len(ex[(kind,nm)][1].split()): ex[(kind,nm)]=(g.E,fmt(c),len(c)-g.P)
for k in sorted(st,key=str): print(k,st[k])
for k,v in sorted(ex.items(),key=str): print(k,v)
