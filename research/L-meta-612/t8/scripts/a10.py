from lib8 import *
from t2lib import triangle_free
st=collections.Counter(); ex={}
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c']); key=d.get('g')
    res=[]
    for v in g.sup:
        if not g.Eminus({v}): continue
        res.append(DV(g,c,v))
    st[(key,'all')]+=1
    if any(x[3] for x in res): st[(key,'cert')]+=1
    else:
        hyp=any(x[0] for x in res)
        st[(key,'nohyp' if not hyp else 'pen')]+=1
        if triangle_free(g) and key not in ex: ex[key]=d['c']
for k in sorted(set(k for k,_ in st)): print(k,{t:st[(k,t)] for t in ['all','cert','nohyp','pen']})
for k,v in ex.items(): print(k,v)
