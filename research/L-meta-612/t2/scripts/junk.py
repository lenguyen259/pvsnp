import collections
from t2lib import *
st=collections.Counter(); seen=set(); ex={}
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1: continue
    c=renum(n,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k)
    tf=triangle_free(g)
    n1,n2,n3,na=viol_counts(g,c); sl=len(c)-g.P
    key='tf' if tf else 'tri'
    st[key]+=1
    for nm,val in [('N3',n3),('N13',len({0})*0 or None),('all',na),('N1',n1),('N2',n2)]:
        if val is None: continue
        if sl<val:
            st[key+'_fail_'+nm]+=1
            if (key,nm) not in ex or sl<ex[(key,nm)][0]: ex[(key,nm)]=(sl,val,g.E,fmt(c))
print(dict(st))
for k in sorted(ex): print(k,ex[k])
