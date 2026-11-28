import collections,sys
from lib import *
st=collections.Counter(); ex=collections.defaultdict(list)
cache={}
for n,E,c in data():
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    k=tuple(E)
    if k not in cache:
        P=phi(E); t=tau(E)
        cache[k]={v:P-phi([e for e in E if v not in e]) for v in sup}
    need=cache[k]
    if any(need[v]==P for v in sup) if False else False: pass
    R,T,o=red(n,c); a0,o0=cnt(R)
    xv={v:sum(1<<r for r in range(1<<n) if (r>>v)&1) for v in range(n)}
    core=lambda q:{v for v in range(n) if T[q]&~xv[v]==0}
    ch=collections.Counter(); da=collections.Counter()
    for i,(op,j,kk) in R.items():
        if op=='|':
            for v in core(j)|core(kk): ch[v]+=1
        else:
            for v in core(i): da[v]+=1
    tot={}
    for v in sup:
        R1,_,_=red(n,c,{v:0}); a1,o1=cnt(R1); tot[v]=a0+o0-a1-o1
    md=min(deg.values())
    nonbase=[v for v in sup if [e for e in E if v not in e]]
    if not nonbase: continue
    st['n']+=1
    kap={v:ch[v]+da[v] for v in sup}
    st['K1 some kappa']+=any(kap[v]>=need[v] for v in nonbase)
    st['tot some']+=any(tot[v]>=need[v] for v in nonbase)
    st['tot some mindeg']+=any(tot[v]>=need[v] for v in nonbase if deg[v]==md)
    st['tot all mindeg']+=all(tot[v]>=need[v] for v in nonbase if deg[v]==md)
    st['tot all']+=all(tot[v]>=need[v] for v in nonbase)
    if md>=2:
        st['md2 n']+=1
        st['md2 tot all deg2']+=all(tot[v]>=need[v] for v in nonbase if deg[v]==2)
        st['md2 kappa some']+=any(kap[v]>=need[v] for v in nonbase)
        st['md2 kappa some deg2']+=any(kap[v]>=need[v] for v in nonbase if deg[v]==2)
    if not any(kap[v]>=need[v] for v in nonbase) and len(ex['K1'])<4: ex['K1'].append((E,c,{v:(kap[v],tot[v],need[v]) for v in sup}))
    if not any(tot[v]>=need[v] for v in nonbase if deg[v]==md) and len(ex['mindeg'])<4: ex['mindeg'].append((E,c,{v:(tot[v],need[v]) for v in sup}))
print(dict(st))
for k,v in ex.items():
    for e in v: print(k,e)
