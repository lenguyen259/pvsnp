import collections,sys,itertools
from lib import *
st=collections.Counter(); ex=collections.defaultdict(list)
def threads(sup,deg,N):
    V2=[v for v in sup if deg[v]==2]; seen=set(); out=[]
    for v in V2:
        if v in seen: continue
        comp=set(); st2=[v]
        while st2:
            x=st2.pop()
            if x in comp: continue
            comp.add(x); st2+=[y for y in N[x] if deg[y]==2]
        seen|=comp; out.append(comp)
    return out
for n,E,c in data():
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    if min(deg.values())<2: continue
    N={v:{b for a,b in E if a==v}|{a for a,b in E if b==v} for v in sup}
    R,T,o=red(n,c); a0,o0=cnt(R)
    def sav(X):
        R1,_,_=red(n,c,{x:0 for x in X}); return o0-cnt(R1)[1]
    def need(X):
        e=sum(1 for a,b in E if a in X or b in X); return e-(1 if e==len(E) else 0)
    st['n']+=1
    ths=threads(sup,deg,N)
    ok=True
    for t in ths:
        s=sav(t); nd=need(t); st['thr']+=1
        if s>=nd: st['thr ok']+=1
        else:
            ok=False
            if len(ex[(tuple(E),len(t))])<1: ex[(tuple(E),len(t))].append((' '.join('%d=%d%s%d'%(i,j,op,k) for i,op,j,k in c),sorted(t),s,nd))
    st['all threads ok']+=ok
    for a,b in E:
        if deg[a]==2 and deg[b]==2:
            st['e22']+=1; st['e22 ok']+=sav({a,b})>=need({a,b})
    for v in sup:
        st['Nv']+=1; st['Nv ok']+=sav(N[v])>=need(N[v])
print(dict(st))
for k,v in list(ex.items())[:12]: print(k,v)
