# check minimal-gate single-charge lemma (PROVED) on all data
import base,collections
from t2h import minimal_ors
L=base.get(); H=collections.Counter()
for d in L:
    E=set(map(frozenset,d['E'])); ds=d['ds']; n=d['n']
    N={v:{u for u in d['sup'] if frozenset((u,v)) in E} for v in d['sup']}
    chv={v:base.ch(d,v) for v in d['sup']}
    for i in minimal_ors(d):
        j,k=d['ors'][i]; A,B=d['core'][j],d['core'][k]
        for v in A|B:
            if chv[v]!=1: continue
            if v in A and v in B:
                ok = len(N[v])==2 and {A,B}=={frozenset({v,u}) for u in N[v]}; H['AnB',ok]+=1
            else:
                X,Y=(A,B) if v in A else (B,A)
                indep=not any(frozenset((p,q)) in E for p in Y for q in Y if p<q)
                ok = X=={v} and (not indep or (len(Y)>=ds[v] and not (N[v]&Y) and all(N[u]&Y for u in N[v]) and not any(v in N[b] for b in Y)))
                H['A-B',indep,ok]+=1
print(H)
