from lib8 import *
from t5an import load
files=sys.argv[1:]
src=allsrc() if not files else (('f',d) for d in load(files))
st=collections.Counter(); ex=[]
for s_,d in src:
    g=Graph(d['E']); c=parse(d['c'])
    if not ok(g,c): continue
    st['circ']+=1; ad=anddepth(c); st['ad%d'%ad]+=1
    v=starall_viol(g,c); sa=not v
    st['starall']+=sa
    A={v:LD(g,c,rho)-need for nm,v,rho,need in g.options() if nm=='A'}
    cs=centres(g,c)
    allc=all(A.get(x,-9)>=0 for x in cs); somec=any(A.get(x,-9)>=0 for x in cs)
    key=('SL' if ad==1 else 'SA' if sa else 'other')
    st[key+'_every']+=allc; st[key+'_some']+=somec; st[key]+=1
    if key=='SL' and not allc: ex.append(d['c'])
    if key=='SA' and not somec and len(ex)<5: ex.append(('SA',d['g'],d['E'],d['c'],A,cs))
print(dict(st)); [print(e) for e in ex[:6]]
