"""T2-LT on jsonl pools: some A/N/B option paid by |K u Cp u Top|-1. Also L1(N[a])>=e(N[a]) smallest failure in config pools."""
import sys,time,collections,json; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an4 import *
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); fails=[]
for fn in sys.argv[2:]:
    for d in load([fn]):
        if time.time()-t0>secs: break
        g=Graph(d['E']); c=parse(d['c']); st['circ']+=1; ok=False
        for nm,v,rho,need in g.options():
            lt,lo=LT(g,c,rho)
            if lt>=need: ok=True; break
        st['LT']+=ok
        if not ok: fails.append((len(c)-g.P,d['g'] if 'g' in d else '',d['E'],d['c']))
print(dict(st)); fails.sort(key=lambda x:x[0]); [print(f) for f in fails[:3]]
