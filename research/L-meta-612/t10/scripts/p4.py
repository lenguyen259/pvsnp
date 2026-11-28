# classify pen witnesses (girth>=5) and the first AND on live paths above them
from lib10 import *
from t2lib import sing
def pure_pairs(g,T,q):
    S=sing(g,T,q); out=[]
    for a in range(g.n):
        for b in range(a+1,g.n):
            if a in S or b in S: continue
            if (T[q]>>((1<<a)|(1<<b)))&1: out.append((a,b))
    return out
st=collections.Counter(); ex={}
for src,g,c in corpus():
    T=tables(g,c,{}); gate={x[0]:x for x in c}; R=readers(c); out=c[-1][0]
    for v in g.sup:
        if not g.Eminus({v}): continue
        rho={v:0}; Z,L,I,aI,F,exc=zone(g,c,rho)
        K={i for i,o,j,k in c if (T[i] & ~g.X[v] & g.full)==0}
        for y in I:
            if y<g.n: continue
            if (T[y]>>(1<<v))&1: continue
            W={w for w in g.N[v] if (T[y]>>((1<<v)|(1<<w)))&1}
            if len(W)<2: continue
            Sy=sing(g,T,y); typ='S' if W<=Sy else ('P' if not (W&Sy) else 'M')
            st['wit',typ]+=1
            # live paths: DFS upward avoiding K, record first AND
            cls=set(); stack=[(y,y)]; seen=set()
            while stack:
                x,prev=stack.pop()
                for q in R[x]:
                    if q in K or (q,x) in seen: continue
                    seen.add((q,x))
                    _,o,j,k=gate[q]
                    if o=='|': stack.append((q,q)); continue
                    s=k if j==x else j
                    Sr,Ss=sing(g,T,x),sing(g,T,s)
                    junk=any(tuple(sorted(e)) not in g.E for e in pure_pairs(g,T,q))
                    if Sr&Ss: cls.add('N1')
                    elif junk: cls.add('N3')
                    elif not Ss: cls.add('N2')
                    elif Ss=={v}: cls.add('REC')
                    else: cls.add('OTHER')
            for cl in cls: st['first',typ,cl]+=1
            if typ=='S' and 'OTHER' in cls: ex.setdefault('SOTHER',(g.E,fmt(c),v,y))
            st['wit_has_nonviol',typ]+= bool(cls-{'N1','N2','N3'})
for k in sorted(st,key=str): print(k,st[k])
print(ex)
