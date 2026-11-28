# single-charged vertices: type X (a=x_v) vs R; check Lemma R (OR charged to each neighbour below g_v)
import base,collections
L=base.get(); H=collections.Counter()
def below(d,i):
    R=d['R']; n=d['n']; seen=set(); st=[i]
    while st:
        x=st.pop()
        for q in R[x][1:]:
            if q>=n and q not in seen: seen.add(q); st.append(q)
    return seen
for d in L:
    E=set(map(frozenset,d['E'])); n=d['n']; sup=d['sup']
    N={v:{u for u in sup if frozenset((u,v)) in E} for v in sup}
    chv={v:base.ch(d,v) for v in sup}
    for v in sup:
        if chv[v]!=1: continue
        g=[i for i in d['ors'] if v in d['chg'][i]][0]
        j,k=d['ors'][g]; a=j if v in d['core'][j] else k
        if a==v: H['typeX',d['ds'][v]]+=1; continue
        bl=below(d,a)|{a}
        ok=all(any(u in d['chg'][i] for i in bl if i in d['ors']) for u in N[v])
        H['typeR',d['ds'][v],ok]+=1
print(H)
