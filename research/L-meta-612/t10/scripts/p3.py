from lib10 import *
from t2lib import minimal_ands, support, sing
st=collections.Counter(); ex={}
def note(k,ex_,g,c):
    st[(k,ex_)]+=1
    if (k,ex_) not in ex: ex[(k,ex_)]=(g.E,fmt(c))
for src,g,c in corpus():
    ex_=len(c)-g.P; T=tables(g,c,{})
    paid=collections.defaultdict(set)
    for nm,v,rho,need in g.options():
        if LD(g,c,rho)>=need: paid[v].add(nm)
    gate={x[0]:x for x in c}
    mins=minimal_ands(c)
    ok1=all(any(paid[v] for v in support(g,c,i)) for i in mins)
    if not ok1: note('V1fail',ex_,g,c)
    ok2=any(any(paid[v]&{'A','B'} for v in support(g,c,i)) for i in mins)
    if not ok2: note('V2fail',ex_,g,c)
    # star minimal ANDs: x_c & OR_B
    stars=[]
    for i in mins:
        _,o,j,k=gate[i]; S1,S2=sing(g,T,j),sing(g,T,k)
        for A_,B_ in ((S1,S2),(S2,S1)):
            if len(A_)==1 and not (A_&B_):
                cc=next(iter(A_)); stars.append((i,cc,B_))
    if stars:
        st[('hasstar',ex_)]+=1
        ok4=any(('A' in paid[cc]) or any(paid[b] for b in B_) for i,cc,B_ in stars)
        if not ok4: note('V4fail',ex_,g,c)
        ok5=all(('A' in paid[cc]) or any(paid[b] for b in B_|{cc}) for i,cc,B_ in stars)
        if not ok5: note('V5fail',ex_,g,c)
    else: note('nostar',ex_,g,c)
    if not any('A' in paid[v] or 'B' in paid[v] for v in g.sup): note('ABfail',ex_,g,c)
for k in sorted(st,key=str): print(k,st[k])
for k,v in sorted(ex.items(),key=str): print(k,v)
