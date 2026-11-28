import sys,itertools,collections,json,glob
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb')
from tr import load,DIRS
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def phi(E): return 0 if not E else len(E)+tau(E)-1
def tables(n,c,rho):
    full=(1<<(1<<n))-1; T={}
    for u in range(n):
        if u in rho: T[u]=full if rho[u] else 0
        else: T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T,full
def red(n,c,rho={}):
    T,full=tables(n,c,rho); canon={}; first={}; real={}
    for u in range(n):
        if T[u] in (0,full): canon[u]='K'
        else: canon[u]=u; first.setdefault(T[u],u)
    for i,o,j,k in c:
        if T[i] in (0,full): canon[i]='K'; continue
        if T[i] in first: canon[i]=first[T[i]]; continue
        first[T[i]]=i; canon[i]=i; real[i]=(o,canon[j],canon[k])
    out=canon[c[-1][0]]; seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(y for y in real[x][1:] if y!='K')
    return {i:real[i] for i in seen},T,out
def cnt(R):
    a=sum(1 for g in R.values() if g[0]=='&'); return a,len(R)-a
def tolist(R):
    return [(i,)+(R[i][0],R[i][1],R[i][2]) for i in sorted(R)]
def sub3(E):
    d=collections.Counter(x for e in E for x in e); return max(d.values())<=3
def data(maxdeg=3):
    seen=set()
    for fn,n,E,X,c in load(DIRS):
        d=collections.Counter(x for e in E for x in e)
        if max(d.values())>maxdeg: continue
        R,T,o=red(n,c)
        key=(tuple(E),tuple(sorted(R.items())))
        if key in seen: continue
        seen.add(key)
        yield n,E,tolist(R)
