# per-node full potential: |cone(p)| >= |E_p| + tau(E_p) + |S_p| - 1 ; and AND-cone >= tau(E_p) (+?)
from lib10 import *
from t2lib import sing, starall_viol, tau
st=collections.Counter(); ex={}
for src,g,c in corpus(only_g5=False):
    if not c4free(g): continue
    T=tables(g,c,{})
    clean=not any(t=='N3' for i,t in starall_viol(g,c))
    cone={u:frozenset() for u in range(g.n)}
    for i,o,j,k in c: cone[i]=cone[j]|cone[k]|{i}
    kind=('g5' if girth5(g) else 'tri', 'clean' if clean else 'junk')
    st[kind]+=1; bad=collections.Counter()
    ands={x[0] for x in c if x[1]=='&'}
    for i,o,j,k in c:
        S=sing(g,T,i)
        Ep=tuple(e for e in g.E if e[0] not in S and e[1] not in S and (T[i]>>((1<<e[0])|(1<<e[1])))&1)
        t=tau(Ep) if Ep else 0
        if len(cone[i])<len(Ep)+t+len(S)-1: bad['V']+=1
        if len(cone[i]&ands)<t: bad['A']+=1
        if len(cone[i]-ands)<len(Ep)+len(S)-1: bad['W2']+=1
    for nm in bad:
        st[(kind,nm)]+=1
        if (kind,nm) not in ex or len(c)<len(ex[(kind,nm)][1].split()): ex[(kind,nm)]=(g.E,fmt(c),len(c)-g.P)
for k in sorted(st,key=str): print(k,st[k])
for k,v in sorted(ex.items(),key=str): print(k,v)
