"""Truncated (degree<=2) semantics of monotone circuits, reduction and restriction."""
import sys, json, glob
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
import networkx as nx

def t_or(a,b):
    S=a[0]|b[0]
    P=frozenset(p for p in (a[1]|b[1]) if not (p & S))
    return (S,P)
def t_and(a,b):
    S1,P1=a; S2,P2=b
    S=S1&S2
    P=set()
    for u in S1:
        for v in S2:
            if u!=v: P.add(frozenset((u,v)))
    for p in P1:
        if p & S2: P.add(p)
    for p in P2:
        if p & S1: P.add(p)
    P|= (P1&P2)
    P=frozenset(p for p in P if not (p & S))
    return (S,P)
ZERO=(frozenset(),frozenset())

def values(n,c,dead=()):
    V={}
    for u in range(n): V[u]=ZERO if u in dead else (frozenset([u]),frozenset())
    for i,o,j,k in c:
        V[i]=t_and(V[j],V[k]) if o=='&' else t_or(V[j],V[k])
    return V

def reduce(n,c,dead=()):
    """return dict of real gates i->(op,j,k) (inputs canonical), reachable from output, and V."""
    V=values(n,c,dead)
    canon={}; first={}
    for u in range(n):
        if V[u]==ZERO: canon[u]='Z'
        else: canon[u]=u; first[V[u]]=u
    real={}
    for i,o,j,k in c:
        if V[i]==ZERO: canon[i]='Z'; continue
        if V[i] in first: canon[i]=first[V[i]]; continue
        first[V[i]]=i; canon[i]=i
        real[i]=(o,canon[j],canon[k])
        assert canon[j]!='Z' and canon[k]!='Z'
    out=canon[c[-1][0]]
    seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen:
            seen.add(x); st.extend(real[x][1:])
    return {i:real[i] for i in seen}, V, out

def counts(R):
    a=sum(1 for g in R.values() if g[0]=='&'); return a, len(R)-a

def load(dirs):
    for d in dirs:
        for fn in sorted(glob.glob(d+'/*.json')):
            D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
            for c in D['circs']:
                yield fn,n,E,D.get('X',0),[tuple(x) for x in c]
DIRS=[SC+'/s_case/circs',SC+'/tf/circs',SC+'/nf/circs']
def tau(E):
    import itertools
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def deg(E,v): return sum(1 for e in E if v in e)

def bvalues(n,c,dead=()):
    M=(1<<(1<<n))-1
    T={}
    for u in range(n): T[u]=0 if u in dead else sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
def breduce(n,c,dead=()):
    T=bvalues(n,c,dead); canon={}; first={}; real={}
    for u in range(n):
        if T[u]==0: canon[u]='Z'
        else: canon[u]=u; first[T[u]]=u
    for i,o,j,k in c:
        if T[i]==0: canon[i]='Z'; continue
        if T[i] in first: canon[i]=first[T[i]]; continue
        first[T[i]]=i; canon[i]=i; real[i]=(o,canon[j],canon[k])
    out=canon[c[-1][0]]; seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(real[x][1:])
    return {i:real[i] for i in seen},T,out
