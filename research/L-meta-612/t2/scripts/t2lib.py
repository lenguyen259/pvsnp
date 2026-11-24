"""T2 harness: restriction options for circuits of f_G.
Circuit: list of (i,op,j,k), i>=n increasing, output = last gate."""
import itertools, functools, collections, json, glob, sys
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'

@functools.lru_cache(maxsize=None)
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def phi(E):
    E=tuple(sorted(E)); return 0 if not E else len(E)+tau(E)-1

def parse(s):
    c=[]
    for t in s.split():
        i,rest=t.split('='); o='&' if '&' in rest else '|'; j,k=rest.split(o); c.append((int(i),o,int(j),int(k)))
    return c
def fmt(c): return ' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c)

class Graph:
    def __init__(s,E,n=None):
        s.E=tuple(sorted(tuple(sorted(e)) for e in E))
        s.n=n if n else max(max(e) for e in s.E)+1
        s.sup=sorted({x for e in s.E for x in e})
        s.N={v:set() for v in range(s.n)}
        for a,b in s.E: s.N[a].add(b); s.N[b].add(a)
        s.full=(1<<(1<<s.n))-1
        s.X=[sum(1<<r for r in range(1<<s.n) if (r>>u)&1) for u in range(s.n)]
        s.f=0
        for a,b in s.E: s.f|=s.X[a]&s.X[b]
        s.P=phi(s.E); s.t=tau(s.E)
    def Eminus(s,X): return tuple(e for e in s.E if e[0] not in X and e[1] not in X)
    def options(s):
        """list of (name, v, rho, need) for the T2 family"""
        out=[]
        for v in s.sup:
            Nv=s.N[v]
            Ev=s.Eminus({v})
            if Ev: out.append(('A',v,{v:0},s.P-phi(Ev)))
            EN=s.Eminus(Nv|{v})
            if EN:
                out.append(('N',v,{u:0 for u in Nv|{v}},s.P-phi(EN)))
            # x_v:=1 with forced accounting (Fact F)
            P1=len(Nv)+phi(EN) if EN else len(Nv)-1
            out.append(('B',v,{v:1},s.P-P1))
        return out

def tables(g,c,rho):
    T={}
    for u in range(g.n):
        T[u]=(g.full if rho[u] else 0) if u in rho else g.X[u]
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T

def red(g,c,rho=None):
    """functional reduction: constants, duplicates (first occurrence), dead. returns list circuit"""
    rho=rho or {}
    T=tables(g,c,rho); full=g.full; canon={}; first={}; real={}
    for u in range(g.n):
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
    return [(i,)+real[i] for i in sorted(seen)]

def ruleR(g,c,rho):
    """syntactic rule R; returns surviving list circuit (inputs renamed to representatives)"""
    val={}  # node -> ('c',b) or ('n',rep)
    for u in range(g.n):
        val[u]=('c',rho[u]) if u in rho else ('n',u)
    gates={}
    for i,o,j,k in c:
        a,b=val[j],val[k]
        if o=='&':
            if a==('c',0) or b==('c',0): val[i]=('c',0); continue
            if a==('c',1): val[i]=b; continue
            if b==('c',1): val[i]=a; continue
        else:
            if a==('c',1) or b==('c',1): val[i]=('c',1); continue
            if a==('c',0): val[i]=b; continue
            if b==('c',0): val[i]=a; continue
        if a==b: val[i]=a; continue
        val[i]=('n',i); gates[i]=(o,a[1],b[1])
    o=val[c[-1][0]]
    if o[0]=='c': return []
    seen=set(); st=[o[1]]
    while st:
        x=st.pop()
        if x in gates and x not in seen: seen.add(x); st.extend(gates[x][1:])
    return [(i,)+gates[i] for i in sorted(seen)]

def elim(g,c,rho):
    s=len(c)
    r1=red(g,c,rho)
    r2=ruleR(g,c,rho); r2=red(g,r2,rho) if r2 else r2
    return s-min(len(r1),len(r2))

def nand(c): return sum(1 for x in c if x[1]=='&')

def ok(g,c):
    return tables(g,c,{})[c[-1][0]]==g.f

def evaluate(g,c,opts=None):
    """c reduced. returns dict name->list of (v,elim,need,good)"""
    opts=opts or g.options()
    res=[]
    for name,v,rho,need in opts:
        e=elim(g,c,rho); res.append((name,v,e,need,e>=need))
    return res

def renum(n,c):
    m={u:u for u in range(n)}; out=[]
    for t,(i,o,j,k) in enumerate(c):
        m[i]=n+t; out.append((n+t,o,m[j],m[k]))
    return out

def load_cached():
    for d in ['s_case/circs','tf/circs','nf/circs']:
        for fn in sorted(glob.glob(SC+'/'+d+'/*.json')):
            D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
            for c in D['circs']:
                yield fn,n,E,[tuple(x) for x in c]

# singleton sets & STAR-ALL check
def sing(g,T,q):
    return frozenset(u for u in range(g.n) if (T[q]>>(1<<u))&1)
def starall_viol(g,c):
    T=tables(g,c,{}); v=[]
    for i,o,j,k in c:
        if o!='&': continue
        S1,S2=sing(g,T,j),sing(g,T,k)
        if S1&S2: v.append((i,'N1'))
        if not S1 or not S2: v.append((i,'N2'))
        for a in S1-S2:
            for b in S2-S1:
                if tuple(sorted((a,b))) not in g.E: v.append((i,'N3')); break
            else: continue
            break
    return v

def minimal_ands(c):
    isand={i for i,o,j,k in c if o=='&'}; anc={}
    for i,o,j,k in c:
        anc[i]=(anc.get(j,False) or j in isand) or (anc.get(k,False) or k in isand)
    return [i for i in isand if not anc[i]]
def support(g,c,i):
    # variables in cone of i
    d={x[0]:x for x in c}; st=[i]; S=set(); seen=set()
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x)
        if x<g.n: S.add(x)
        else: st.extend(d[x][2:])
    return S

# ---- local (first-order) lower bounds ----
def lo_bounds(g,c,X,b):
    """b=0: D={gates p <= OR_X}, count |D|+|OR gates outside D reading D|.
       b=1 (X={v}): R={gates p(e_v)=1}, count |R|+|AND gates outside R reading R|."""
    T=tables(g,c,{})
    if b==0:
        M=0
        for x in X: M|=g.X[x]
        inD=lambda p: (T[p] & ~M & g.full)==0
        D={p for p in list(X)+[x[0] for x in c] if inD(p)}
        bd=sum(1 for i,o,j,k in c if i not in D and o=='|' and (j in D or k in D))
        return len(D - set(X)) + bd
    else:
        v=next(iter(X)); bit=1<<(1<<v)
        R={p for p in [v]+[x[0] for x in c] if T[p]&bit}
        bd=sum(1 for i,o,j,k in c if i not in R and o=='&' and (j in R or k in R))
        return len(R-{v})+bd
def charged(g,c,v):
    T=tables(g,c,{})
    D={p for p in [v]+[x[0] for x in c] if (T[p]&~g.X[v]&g.full)==0}
    return sum(1 for i,o,j,k in c if o=='|' and (j in D or k in D))

def viol_counts(g,c):
    v=starall_viol(g,c); by=collections.defaultdict(set)
    for i,t in v: by[t].add(i)
    allv={i for i,t in v}
    return len(by['N1']),len(by['N2']),len(by['N3']),len(allv)
def triangle_free(g):
    return not any(g.N[a]&g.N[b] for a,b in g.E)
