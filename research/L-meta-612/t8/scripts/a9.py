from lib8 import *
st=collections.Counter(); ex=[]
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c'])
    res=[]
    for v in g.sup:
        if not g.Eminus({v}): continue
        hyp,b,ld,cert=DV(g,c,v); res.append((hyp,cert))
    if any(x[1] for x in res): continue
    st['uncert']+=1
    if not any(x[0] for x in res): st['nohyp_anywhere']+=1
    else: st['hyp_but_pen']+=1
    if len(ex)<3 and any(x[0] for x in res): ex.append((d['g'],d['c']))
print(dict(st)); [print(e) for e in ex]
