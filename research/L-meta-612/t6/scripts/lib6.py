import sys,itertools,json
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t4/scripts')
from gen import *
from psun import psun
def tab_sub(g,c,sub):
    T={}
    for u in range(g.n):
        if u in sub:
            k,x=sub[u]; T[u]=(g.full if x else 0) if k=='c' else g.X[x]
        else: T[u]=g.X[u]
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
def red_T(g,c,T):
    full=g.full; canon={}; first={}; real={}
    for u in range(g.n):
        if T[u] in (0,full): canon[u]='K'
        else:
            canon[u]=first.setdefault(T[u],u)
    for i,o,j,k in c:
        if T[i] in (0,full): canon[i]='K'; continue
        if T[i] in first: canon[i]=first[T[i]]; continue
        first[T[i]]=i; canon[i]=i; real[i]=(o,canon[j],canon[k])
    out=canon[c[-1][0]]; seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(y for y in real[x][1:] if y!='K')
    return [(i,)+real[i] for i in sorted(seen)]
def elim_sub(g,c,sub):
    return len(c)-len(red_T(g,c,tab_sub(g,c,sub)))
def is_pf_c4free(E):
    V=sorted({x for e in E for x in e}); N={v:set() for v in V}
    for a,b in E: N[a].add(b); N[b].add(a)
    # C4
    for a in V:
        for b in V:
            if a<b and len(N[a]&N[b])>=2: return False
    # pseudoforest: each component edges<=vertices
    seen=set()
    for v in V:
        if v in seen: continue
        comp={v}; st=[v]
        while st:
            x=st.pop()
            for y in N[x]:
                if y not in comp: comp.add(y); st.append(y)
        seen|=comp
        ne=sum(1 for a,b in E if a in comp)
        if ne>len(comp): return False
    return True
def need_sub(g,sub):
    """None if invalid. image function = OR_F v f_H"""
    F=set(); H=set()
    img=lambda u: sub.get(u,('v',u))
    for a,b in g.E:
        A,B=img(a),img(b)
        if A==('c',0) or B==('c',0): continue
        if A==('c',1) and B==('c',1): return None
        if A==('c',1): F.add(B[1]); continue
        if B==('c',1): F.add(A[1]); continue
        if A==B: F.add(A[1]); continue
        H.add(tuple(sorted((A[1],B[1]))))
    H=tuple(sorted(e for e in H if e[0] not in F and e[1] not in F))
    if not F and not H: return None
    if H and not is_pf_c4free(H): return 'bad'
    LB=(len(F)+phi(H) if H else len(F)-1) if F else phi(H)
    return g.P-LB
def struct(g,c,P,L):
    lv=3
    for v in P:
        u=L[v]; rd=[x for x in c if v in x[2:]]
        if len(rd)!=1 or rd[0][1]!='|': return 0
        rg=[x for x in c if rd[0][0] in x[2:]]
        if len(rg)!=1 or rg[0][1]!='&': lv=min(lv,1); continue
        if sum(1 for x in c if u in x[2:])!=1: lv=min(lv,2)
    return lv
def runs(n,S):
    S=set(S); out=[]
    if not S: return []
    start=min(S)
    i=start; cur=[]
    for t in range(1,n+1):
        w=(start+t)%n
        if w in S:
            if cur: out.append(cur); cur=[]
        else: cur.append(w)
    return out
