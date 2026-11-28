from lib8 import *
from t2lib import minimal_ands, support
st=collections.Counter(); bad=[]
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1; anyc=False
    for nm,v,rho,need in g.options():
        if nm!='A': continue
        hyp,b,ld,cert=DV(g,c,v)
        if hyp:
            st['hyp']+=1
            if ld<b: st['DVviol']+=1; bad.append((d['c'],v))
            if cert: st['cert']+=1; anyc=True; st['cert_pays']+= ld>=need
    st['circ_with_cert']+=anyc
print(dict(st)); print(bad[:3])
