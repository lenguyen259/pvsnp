# test formal-complexity-measure property of mu' = |X2| + |T| - D on the 2-slice KW game
import itertools, sys, functools
n=int(sys.argv[1]); E=[tuple(sorted(e)) for e in eval(sys.argv[2])]; useD=int(sys.argv[3])
Es=set(E); NE=[p for p in itertools.combinations(range(n),2) if p not in Es]
def cover_min(edges, forced):
    rest=[e for e in edges if e[0] not in forced and e[1] not in forced]
    for k in range(n+1):
        for T in itertools.combinations(range(n),k):
            if all(a in T or b in T for a,b in rest): return len(forced)+k
@functools.lru_cache(None)
def mu(X, Ys, Yn):
    X2=[e for e in X if e[0] in Ys and e[1] in Ys]
    X1=[e for e in X if (e[0] in Ys)!=(e[1] in Ys)]
    X0=[e for e in X if e[0] not in Ys and e[1] not in Ys]
    forced=frozenset(e[1] if e[0] in Ys else e[0] for e in X1)
    m=len(X2)+cover_min(X0+X2,forced)
    if useD: m-=Dval(X,Ys,Yn)
    return m
@functools.lru_cache(None)
def rects(X,Ys,Yn):
    # candidate rectangles: subsets H of X2 bipartite (VA,VB) with all non-edges VA x VB not in Yn ; savings>0
    X2=[e for e in X if e[0] in Ys and e[1] in Ys]
    out=[]
    for k in range(3,len(X2)+1):
        for H in itertools.combinations(X2,k):
            V=sorted(set(itertools.chain(*H)))
            # 2-colour
            col={}
            ok=True
            adj={v:[] for v in V}
            for a,b in H: adj[a].append(b); adj[b].append(a)
            comps=[]
            for v in V:
                if v in col: continue
                col[v]=0; st=[v]; comp=[v]
                while st:
                    x=st.pop()
                    for y in adj[x]:
                        if y not in col: col[y]=1-col[x]; st.append(y); comp.append(y)
                        elif col[y]==col[x]: ok=False
                comps.append(comp)
            if not ok: continue
            # try all flips of components
            best=None
            for flips in itertools.product([0,1],repeat=len(comps)-1):
                c=dict(col)
                for comp,f in zip(comps[1:],flips):
                    if f:
                        for v in comp: c[v]=1-c[v]
                VA=[v for v in V if c[v]==0]; VB=[v for v in V if c[v]==1]
                if any(tuple(sorted((a,b))) in Yn for a in VA for b in VB): continue
                sv=len(H)-max(len(VA),len(VB))
                if sv>0 and (best is None or sv>best): best=sv
            if best: out.append((frozenset(H),best))
    return out
@functools.lru_cache(None)
def Dval(X,Ys,Yn):
    R=rects(X,Ys,Yn)
    best=0
    def rec(i,used,val):
        nonlocal best
        best=max(best,val)
        for j in range(i,len(R)):
            H,s=R[j]
            if not (H&used): rec(j+1,used|H,val+s)
    rec(0,frozenset(),0)
    return best
def downsets():
    for ys in range(1<<n):
        Ys=frozenset(u for u in range(n) if ys>>u&1)
        cand=[p for p in NE if p[0] in Ys and p[1] in Ys]
        for ns in range(1<<len(cand)):
            yield Ys, frozenset(cand[i] for i in range(len(cand)) if ns>>i&1)
DS=list(downsets()); print('downsets',len(DS))
def sub_downsets(Ys,Yn):
    for ys in range(1<<len(Ys)):
        pass
fails=0; checked=0
Xs=[frozenset(c) for k in range(1,len(E)+1) for c in itertools.combinations(E,k)]
import random
random.seed(1)
for X in Xs:
    for Ys,Yn in DS:
        m=mu(X,Ys,Yn)
        # leaf check
        for i in range(n):
            if all(i in e for e in X) and i not in Ys and m>1: print('LEAF FAIL',X,Ys,Yn,m); fails+=1
        # AND splits: Y1,Y2 down-closed subfamilies, union = Y.  enumerate Y1 by its singleton set Ys1 and pairs subset; Y2 must contain rest
        Yl=sorted(Ys); 
        for s1 in range(1<<len(Yl)):
            Ys1=frozenset(Yl[i] for i in range(len(Yl)) if s1>>i&1)
            for s2 in range(1<<len(Yl)):
                Ys2=frozenset(Yl[i] for i in range(len(Yl)) if s2>>i&1)
                if Ys1|Ys2!=Ys: continue
                # pairs: each pair of Yn must go to a side containing both endpoints; take maximal choice: put pair in every side that can hold it (max Y_i is allowed? not nec. best) -> enumerate assignments
                P=list(Yn); opts=[]
                for p in P:
                    o=[]
                    if p[0] in Ys1 and p[1] in Ys1: o.append(1)
                    if p[0] in Ys2 and p[1] in Ys2: o.append(2)
                    if len(o)==2: o.append(3)
                    opts.append(o)
                if any(not o for o in opts): continue
                for ch in itertools.product(*opts):
                    Yn1=frozenset(p for p,c in zip(P,ch) if c&1); Yn2=frozenset(p for p,c in zip(P,ch) if c&2)
                    checked+=1
                    if m>mu(X,Ys1,Yn1)+mu(X,Ys2,Yn2):
                        fails+=1
                        if fails<=8: print('AND FAIL',sorted(X),sorted(Ys),sorted(Yn),'|',sorted(Ys1),sorted(Yn1),'|',sorted(Ys2),sorted(Yn2),m,mu(X,Ys1,Yn1),mu(X,Ys2,Yn2))
        # OR splits
        Xl=sorted(X)
        for k in range(1,len(Xl)):
            for c in itertools.combinations(Xl,k):
                X1=frozenset(c); X2=X-X1
                if min(c)!=Xl[0]: continue
                if m>mu(X1,Ys,Yn)+mu(X2,Ys,Yn):
                    fails+=1
                    if fails<=8: print('OR FAIL',sorted(X1),sorted(X2),sorted(Ys),sorted(Yn))
print('checked',checked,'fails',fails,'root',mu(frozenset(E),frozenset(range(n)),frozenset(NE)))
