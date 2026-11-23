import base,collections
L=base.get(); H=collections.Counter(); EX={}
def minimal_ors(d):
    R=d['R']; n=d['n']
    # node has an OR below?
    hasor={}
    for i in sorted(R):
        op,j,k=R[i]
        hasor[i]=any((q>=n and (R[q][0]=='|' or hasor[q])) for q in (j,k))
    return [i for i in d['ors'] if not hasor[i]]
for d in L:
    E=d['E']; ds=d['ds']; sup=d['sup']; md=min(ds.values())
    chv={v:base.ch(d,v) for v in sup}
    good={v for v in sup if chv[v]>=ds[v]}
    mo=minimal_ors(d); g=tuple(E)
    def rec(k,b):
        H[g,k,b]+=1
        if not b: EX.setdefault((g,k),d)
    rec('every minOR has good',all(d['chg'][i]&good for i in mo))
    rec('every minOR with mindeg v has good mindeg',all(any(ds[v]==md for v in d['chg'][i]&good) for i in mo if any(ds[v]==md for v in d['chg'][i])))
    rec('some minOR has good mindeg',any(any(ds[v]==md for v in d['chg'][i]&good) for i in mo))
    rec('every minOR has v ch>=2',all(any(chv[v]>=2 for v in d['chg'][i]) for i in mo))
    rec('every minOR with mindeg v has mindeg ch>=2',all(any(chv[v]>=2 and ds[v]==md for v in d['chg'][i]) for i in mo if any(ds[v]==md for v in d['chg'][i])))
    rec('ch>=deg for every v of degree 2 that is in no ... (all deg2 good)', all(chv[v]>=2 for v in sup if ds[v]==2))
for k in sorted(H): print(k,H[k])
import pickle; pickle.dump(EX,open('/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemD/ex2.pkl','wb'))
for k,d in EX.items():
    if 'all deg2' in k[1]: continue
    print(k, d['ds'], {i:(d['R'][i]) for i in sorted(d['R'])}, {v:base.ch(d,v) for v in d['sup']})
