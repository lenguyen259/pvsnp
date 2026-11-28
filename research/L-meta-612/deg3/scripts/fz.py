"""Adversarial fuzzer: random function-preserving edits of circuits for f_G; minimise a margin.
Circuit = list of (i,op,j,k) with i>=n increasing."""
import sys,random,itertools,collections,json,time
from lib import tau,phi
def TT(n):
    return [sum(1<<r for r in range(1<<n) if (r>>u)&1) for u in range(n)]
def evalc(n,c,X,rho=None):
    full=(1<<(1<<n))-1; T={}
    for u in range(n):
        T[u]=X[u] if not rho or u not in rho else (full if rho[u] else 0)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
def redc(n,c,X,rho=None):
    """reduced circuit: returns (#AND,#OR, reduced list renumbered)"""
    full=(1<<(1<<n))-1
    T=evalc(n,c,X,rho); canon={}; first={}; real={}
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
    keep=sorted(seen)
    a=sum(1 for i in keep if real[i][0]=='&')
    return a,len(keep)-a,[(i,)+real[i] for i in keep],out
def renum(n,c):
    m={u:u for u in range(n)}; out=[]
    for t,(i,o,j,k) in enumerate(c):
        m[i]=n+t; out.append((n+t,o,m[j],m[k]))
    return out
class G:
    def __init__(s,E):
        s.E=[tuple(e) for e in E]; s.n=max(max(e) for e in E)+1; s.X=TT(s.n)
        s.f=0
        for a,b in s.E: s.f|=s.X[a]&s.X[b]
        s.sup=sorted({x for e in s.E for x in e})
        s.deg={v:sum(1 for e in s.E if v in e) for v in s.sup}
        s.P=phi(s.E); s.t=tau(s.E)
        s.Ev={v:[e for e in s.E if v not in e] for v in s.sup}
        s.needP={v:s.P-phi(s.Ev[v]) for v in s.sup}
        s.needOR={v:s.deg[v]-(0 if s.Ev[v] else 1) for v in s.sup}
        s.needAND={v:s.t-(tau(s.Ev[v]) if s.Ev[v] else 0) for v in s.sup}
    def ok(s,c): return evalc(s.n,c,s.X)[c[-1][0]]==s.f
    def stats(s,c):
        a0,o0,R,out=redc(s.n,c,s.X)
        so={};sa={}
        for v in s.sup:
            a1,o1,_,_=redc(s.n,R,s.X,{v:0}); so[v]=o0-o1; sa[v]=a0-a1
        T=evalc(s.n,R,s.X); full=(1<<(1<<s.n))-1
        core=lambda q:{v for v in range(s.n) if T[q]&~s.X[v]&full==0}
        ch=collections.Counter()
        for i,o,j,k in R:
            if o=='|':
                for v in core(j)|core(k): ch[v]+=1
        s.ch=ch
        return a0,o0,so,sa,R
def star_circuit(g,rnd):
    # random min-ish cover and assignment, random tree shapes
    E=g.E[:]; n=g.n
    # random vertex cover: greedy random
    T=set()
    for a,b in rnd.sample(E,len(E)):
        if a not in T and b not in T: T.add(rnd.choice((a,b)))
    # remove redundant
    for v in rnd.sample(sorted(T),len(T)):
        if all((a in T-{v}) or (b in T-{v}) for a,b in E): T.discard(v)
    L=collections.defaultdict(list)
    for a,b in E:
        cs=[x for x in (a,b) if x in T]; t=rnd.choice(cs); L[t].append(b if t==a else a)
    c=[]; nxt=[n]
    def gte(o,j,k):
        i=nxt[0]; nxt[0]+=1; c.append((i,o,j,k)); return i
    def OR(xs):
        xs=xs[:]; rnd.shuffle(xs)
        while len(xs)>1:
            i,j=rnd.sample(range(len(xs)),2); a,b=xs[i],xs[j]
            xs=[x for t,x in enumerate(xs) if t not in (i,j)]+[gte('|',a,b)]
        return xs[0]
    terms=[gte('&',t,OR(L[t])) for t in L]
    OR(terms); return c
def mutate(g,c,rnd,maxsize):
    n=g.n
    for _ in range(50):
        c2=list(c); mv=rnd.random()
        if mv<0.55 and len(c2)<maxsize:
            # insert t=op(q,r) and redirect a random subset of readers of q to t
            nodes=list(range(n))+[x[0] for x in c2]
            q=rnd.choice(nodes); r=rnd.choice(nodes)
            if q==r: continue
            op=rnd.choice('&|')
            pos=max([t for t,x in enumerate(c2) if x[0] in (q,r)],default=-1)+1
            new=max(x[0] for x in c2)+1
            readers=[t for t,x in enumerate(c2) if t>=pos and q in x[2:]]
            if not readers: continue
            sub=[t for t in readers if rnd.random()<0.6] or [rnd.choice(readers)]
            for t in sub:
                i,o,j,k=c2[t]; c2[t]=(i,o,new if j==q else j,new if k==q else k)
            c2.insert(pos,(new,op,q,r))
            c2=renum(n,c2)
        else:
            # rewire one input of a gate to another earlier node
            t=rnd.randrange(len(c2)); i,o,j,k=c2[t]
            nodes=list(range(n))+[x[0] for x in c2[:t]]
            r=rnd.choice(nodes)
            if rnd.random()<0.5: c2[t]=(i,o,r,k)
            else: c2[t]=(i,o,j,r)
        if g.ok(c2):
            a,o,R,out=redc(n,c2,g.X)
            if not R: continue
            return renum(n,R) if R[-1][0]==out else None
    return None
