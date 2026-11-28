import base,collections,itertools
L=base.get(); H=collections.Counter(); EX={}
for d in L:
    E=d['E']; ds=d['ds']; sup=d['sup']; g=tuple(E)
    Hi={v for v in sup if ds[v]>=3}
    if not Hi: continue
    q=base.QX(d,Hi); e=base.eX(d,Hi); rest=len(E)-e
    need=e if rest>0 else e-1
    H[g,'Q_H-need',q-need]+=1
    if q<need: EX.setdefault(g,d)
    # best X overall
    best=max(base.QX(d,set(X))-(base.eX(d,set(X)) - (1 if base.eX(d,set(X))==len(E) else 0)) for r in range(1,len(sup)) for X in itertools.combinations(sup,r))
    H[g,'best proper X slack',best]+=1
for k in sorted(H): print(k,H[k])
for g,d in EX.items(): print(g,{i:d['R'][i] for i in sorted(d['R'])})
