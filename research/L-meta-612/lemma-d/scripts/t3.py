import base,collections
from t2h import minimal_ors
L=base.get(); H=collections.Counter(); EX={}
for d in L:
    E=d['E']; ds=d['ds']; sup=d['sup']; md=min(ds.values()); g=tuple(E)
    chv={v:base.ch(d,v) for v in sup}
    mo=minimal_ors(d)
    # verify |S1|<=1 for every minimal OR
    for i in mo:
        S=d['chg'][i]; S1=[v for v in S if chv[v]==1]
        H[g,'|S1|<=1',len(S1)<=1]+=1
    k=max(sum(1 for v in d['chg'][i] if ds[v]==md) for i in mo)
    H[g,'max #mindeg in minOR support',k]+=1
    if k<2: EX.setdefault(g,[]).append(d)
for k in sorted(H): print(k,H[k])
for g,l in EX.items():
    for d in l[:3]:
        print(g,{i:d['R'][i] for i in sorted(d['R'])},{v:base.ch(d,v) for v in d['sup']})
