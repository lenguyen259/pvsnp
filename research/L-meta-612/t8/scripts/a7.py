from lib8 import *
from t5an import load
files=sys.argv[1:]
src=allsrc() if not files else (('f',d) for d in load(files))
st=collections.Counter(); ex=[]
for s_,d in src:
    g=Graph(d['E']); c=parse(d['c'])
    if not ok(g,c): continue
    st['circ']+=1
    val={}
    for nm,v,rho,need in g.options(): val[(nm,v)]=(LD(g,c,rho),LR(g,c,rho),need)
    sAB=[v for v in g.sup if ('A',v) in val and val[('A',v)][0]+val[('B',v)][0]>=val[('A',v)][2]+val[('B',v)][2]]
    sABr=[v for v in g.sup if ('A',v) in val and val[('A',v)][1]+val[('B',v)][1]>=val[('A',v)][2]+val[('B',v)][2]]
    st['sumAB_LD']+=bool(sAB); st['sumAB_LR']+=bool(sABr)
    if not sAB and len(ex)<4: ex.append((d.get('g'),d['c']))
print(dict(st)); [print(e) for e in ex]
