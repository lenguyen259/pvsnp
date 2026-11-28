# for girth>=5 circuits: LD-paid options; DV2 cert (full form pen<=kZ-delta); distance from uncertified vertices to paid options
from lib10 import *
def dist(g,s):
    D={s:0}; q=[s]
    for x in q:
        for y in g.N[x]:
            if y not in D: D[y]=D[x]+1; q.append(y)
    return D
def cert_full(g,c,v,r=None):
    r=r or DV2(g,c,v); d=delta(g,v)
    carr=(len(r['rest'])==0 or (r['singok'] and r['single']))
    return carr and r['pen']<=r['kZ']-d, r
st=collections.Counter(); ex={}
for src,g,c in corpus():
    ex_=len(c)-g.P
    opts=g.options(); paid=[(nm,v) for nm,v,rho,need in opts if LD(g,c,rho)>=need]
    st[('circ',ex_)]+=1
    if not paid: st[('LDfail',ex_)]+=1; ex.setdefault(('LDfail',ex_),(g.E,fmt(c)))
    cv=[v for v in g.sup if g.Eminus({v}) and cert_full(g,c,v)[0]]
    c2=[v for v in g.sup if g.Eminus({v}) and cert2(g,c,v)]
    if not cv: st[('nocertfull',ex_)]+=1; ex.setdefault(('nocertfull',ex_),(g.E,fmt(c)))
    if not c2: st[('nocert2',ex_)]+=1
    pv={v for nm,v in paid}
    md=max(min(dist(g,u).get(v,99) for v in pv) for u in g.sup) if pv else 99
    st[('maxdist',ex_,md)]+=1
    pa={v for nm,v in paid if nm=='A'}; pb={v for nm,v in paid if nm=='B'}; pn={v for nm,v in paid if nm=='N'}
    st[('hasA',ex_)]+=bool(pa); st[('hasAB',ex_)]+=bool(pa|pb)
for k in sorted(st,key=str): print(k,st[k])
for k,v in ex.items(): print(k,v)
