"""Sanity check of the Leaf Lemma on cached circuits + forest rule."""
import collections
from t2lib import *
st=collections.Counter(); seen=set()
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1: continue
    c=renum(n,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k)
    opts={(o[0],o[1]):o for o in g.options()}
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        dv=g.t-tau(g.Eminus({v}))
        if dv==0 or len(g.N[u])<=2:
            r=evaluate(g,c,[opts[('A',v)],opts[('B',v)]])
            st['leafcase']+=1
            if not any(x[4] for x in r): st['VIOL']+=1; print('VIOL',g.E,fmt(c),v,r)
        else:
            # bad leaf: record structure
            readers=[x for x in c if v in x[2:]]
            st['bad_leaf']+=1
            st['bad_leaf_F%d_%s'%(len(readers),''.join(sorted(x[1] for x in readers)))]+=1
print(dict(st))
