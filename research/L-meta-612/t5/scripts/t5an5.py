import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
from t5an3 import row
import collections
bad=[]
for d in load(sys.argv[1:]):
    g=Graph(d['E']); c=parse(d['c'])
    for rec in d['rec']:
        i,a,b=rec[:3]; R=[row(g,c,v) for v in (a,b)]
        if not any(r and r['elim']>=r['need'] for r in R):
            bad.append((d['s'],len(c),d['g'],d['c'],a,b,R))
bad.sort(key=lambda x:(x[0],x[1]))
print(len(bad),collections.Counter(x[2] for x in bad))
for x in bad[:4]:
    s,_,gn,cs,a,b,R=x; print(gn,'s=Phi+%d'%s,cs,'ab',a,b); [print('  ',r) for r in R]
    g=Graph(dict(load(sys.argv[1:]).__next__())['E']) if False else None
