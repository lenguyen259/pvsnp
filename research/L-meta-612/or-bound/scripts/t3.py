import collections
from tr import *
H=collections.Counter(); seen=set(); ex={}
def chs(R,V,sup):
    out={}
    for v in sup:
        ch=0
        for i,(op,j,k) in R.items():
            if op=='|':
                for q in (j,k):
                    S,P=V[q]
                    if S<=frozenset([v]) and all(v in p for p in P): ch+=1;break
        out[v]=ch
    return out
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    ds={v:deg(E,v) for v in sup}
    if min(ds.values())<2: continue
    R,V,out=reduce(n,c)
    ch=chs(R,V,sup)
    # monomial nodes: inputs, AND of monomials
    mono={u:frozenset([u]) for u in range(n)}
    for i in sorted(R):
        op,j,k=R[i]
        if op=='&' and j in mono and k in mono: mono[i]=mono[j]|mono[k]
    mins=[i for i in R if R[i][0]=='|' and R[i][1] in mono and R[i][2] in mono]
    res=[any(ch[v]>=ds[v] for v in mono[R[i][1]]|mono[R[i][2]]) for i in mins]
    k=('some',any(res)); H[k]+=1; ex.setdefault(k,(E,c))
    k=('all',all(res)); H[k]+=1; ex.setdefault(k,(E,c))
    # leaf-type: vertices v such that x_v read only by OR gates?
for k in sorted(H): print(k,H[k], ex[k] if not k[1] else '')
