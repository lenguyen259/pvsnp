import base,collections,itertools
L=base.get(); H=collections.Counter()
for d in L:
    E=d['E']; ds=d['ds']; sup=d['sup']; n=len(sup)
    chv={v:base.ch(d,v) for v in sup}
    md=min(ds.values())
    g=tuple(E)
    H[g,'all mindeg good',all(chv[v]>=ds[v] for v in sup if ds[v]==md)]+=1
    H[g,'some mindeg good',any(chv[v]>=ds[v] for v in sup if ds[v]==md)]+=1
    H[g,'edge set',any(base.QX(d,{a,b})>=ds[a]+ds[b]-1 for a,b in E)]+=1
    H[g,'avg ch/deg>=n',sum(chv[v]/ds[v] for v in sup)>=n-1e-9]+=1
    H[g,'every v: ch>=2',all(chv[v]>=2 for v in sup)]+=1
    H[g,'every v: ch>=deg-1',all(chv[v]>=ds[v]-1 for v in sup)]+=1
    if max(ds.values())>=3:
        H[g,'all maxdeg good',all(chv[v]>=ds[v] for v in sup if ds[v]==max(ds.values()))]+=1
        H[g,'some deg>=3 good',any(chv[v]>=ds[v] for v in sup if ds[v]>=3)]+=1
for k in sorted(H): print(k,H[k])
