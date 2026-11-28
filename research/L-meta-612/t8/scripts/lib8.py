import sys,json,collections
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
sys.path.insert(0,SC+'/t7'); sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t7/scripts')
from lib7 import *          # Graph, parse, tables, LR, pools, ruleR, ...
def readers(c):
    R=collections.defaultdict(list)
    for i,o,j,k in c: R[j].append(i); R[k].append(i)
    return R
def decomp(g,c,rho):
    """K = gates constant under rho (first order = syntactic), Cp = non-K gates with an input in K or x_rho,
       Dead = other gates all of whose paths to the output meet K."""
    T=tables(g,c,rho); full=g.full
    K={i for i,o,j,k in c if T[i] in (0,full)}
    Kn=K|set(rho)
    Cp={i for i,o,j,k in c if i not in K and (j in Kn or k in Kn)}
    R=readers(c); out=c[-1][0]
    ok={out} if out not in K else set()
    for i,o,j,k in reversed(c):
        if i in ok:
            for x in (j,k):
                if x>=g.n and x not in K: ok.add(x)
    Dead={i for i,o,j,k in c if i not in ok and i not in K and i not in Cp}
    return K,Cp,Dead
def LD(g,c,rho):
    K,Cp,Dd=decomp(g,c,rho); return len(K)+len(Cp)+len(Dd)
def allsrc(extra=True):
    import t3fuzz, graphs
    ex=[('Pet-v',"9=4|2 10=4|1 11=10|8 12=8|2 13=3&12 14=7|8 15=14|0 16=5&15 17=6&11 18=7&9 19=16|18 20=1|19 21=19|13 22=2|0 23=20&22 24=23|17 25=21|24"),
     ('Pet',"10=1|5 11=10|4 12=0&11 13=3|7 14=1|13 15=2&14 16=8|1 17=16|9 18=6&17 19=8|4 20=3&19 21=4|7 22=9&21 23=7|8 24=5&23 25=18|20 26=25|12 27=26|24 28=15|22 29=28|27")]
    for n,s in ex: yield 'ex',{'E':t3fuzz.GR[n],'c':s,'g':n}
    yield from pools()
def zone(g,c,rho):
    """Z = gates all of whose out-paths meet K (incl. K), L = Cp \\ Z, I = external inputs of Z, arcsI, excess"""
    T=tables(g,c,rho); full=g.full
    K={i for i,o,j,k in c if T[i] in (0,full)}
    Kn=K|set(rho)
    Cp={i for i,o,j,k in c if i not in K and (j in Kn or k in Kn)}
    out=c[-1][0]; ok={out} if out not in K else set()
    for i,o,j,k in reversed(c):
        if i in ok and i not in K:
            for x in (j,k):
                if x>=g.n: ok.add(x)
    Z={i for i,o,j,k in c if i not in ok}|K
    L=Cp-Z
    R=readers(c)
    arcsI=sum(1 for i,o,j,k in c if i in Z for x in (j,k) if x not in Z and x not in rho)
    I={x for i,o,j,k in c if i in Z for x in (j,k) if x not in Z and x not in rho}
    F=sum(len(R[u]) for u in rho)
    exc=sum(len(R[z])-1 for z in Z)
    return Z,L,I,arcsI,F,exc
def anddepth(c):
    d={}
    for i,o,j,k in c:
        d[i]=max(d.get(j,0),d.get(k,0))+(o=='&')
    return max(d.values())
def singT(g,T,q): return frozenset(u for u in range(g.n) if (T[q]>>(1<<u))&1)
def centres(g,c):
    """for single-level/star AND gates x_c & y: centre set"""
    T=tables(g,c,{}); cs=set()
    for i,o,j,k in c:
        if o!='&': continue
        S1,S2=singT(g,T,j),singT(g,T,k)
        if len(S1)==1: cs|=S1
        if len(S2)==1: cs|=S2
    return cs
def DV(g,c,v):
    """Theorem DV data for A(v): returns (hyp, bound, LD, cert)"""
    rho={v:0}; Z,L,I,aI,F,exc=zone(g,c,rho); gate={x[0]:x for x in c}
    hyp=not any(v in (gate[q][2],gate[q][3]) for q in L)
    T0=tables(g,c,{})
    Nv=g.N[v]; Ivar={x for x in I if x<g.n}; Ig=[y for y in I if y>=g.n]
    pen=0
    for y in Ig:
        Sy={w for w in Nv if (T0[y]>>((1<<v)|(1<<w)))&1 and not (T0[y]>>(1<<v))&1}
        pen+=max(len(Sy)-1,0)
    bound=F+len(Nv)-pen
    return hyp,bound,F+aI+exc,(hyp and pen==0)
def evalpt(g,c,x,override=None):
    """x: set of vertices =1. override: gate id whose x_c-input is forced to 1 (pair (gate,var))"""
    val={u:(u in x) for u in range(g.n)}
    for i,o,j,k in c:
        a,b=val[j],val[k]
        if override and i==override[0]:
            if j==override[1]: a=True
            if k==override[1]: b=True
        val[i]=(a and b) if o=='&' else (a or b)
    return val[c[-1][0]]
def DV2(g,c,v):
    rho={v:0}; Z,L,I,aI,F,exc=zone(g,c,rho); gate={x[0]:x for x in c}; R=readers(c)
    T0=tables(g,c,{}); Nv=g.N[v]
    K={i for i,o,j,k in c if (T0[i] & ~g.X[v] & g.full)==0}
    kL=[q for q in L if v in gate[q][2:]]; kZ=len(R[v])-len(kL)
    # D-carried: some K node with an L reader has value 1 at e_v+e_w
    srcs={j for q in L for j in gate[q][2:] if j in K}
    ND={w for w in Nv if any((T0[s]>>((1<<v)|(1<<w)))&1 for s in srcs)}
    Ig=[y for y in I if y>=g.n]; pen=0
    for y in Ig:
        Sy={w for w in Nv if (T0[y]>>((1<<v)|(1<<w)))&1 and not (T0[y]>>(1<<v))&1}
        pen+=max(len(Sy)-1,0)
    singok=all(any((T0[(gate[q][3] if gate[q][2]==v else gate[q][2])]>>(1<<u))&1 for u in range(g.n)) for q in kL)
    rest=Nv-ND; car={}
    single=True
    for w in rest:
        js=[q for q in kL if evalpt(g,c,{w},(q,v))]
        if not js: single=False
        car[w]=js
    return dict(F=F,kZ=kZ,kL=len(kL),ND=ND,rest=rest,pen=pen,singok=singok,single=single,LD=F+aI+exc,car=car)
def cert2(g,c,v):
    r=DV2(g,c,v)
    return r['kZ']>=1 and r['pen']==0 and (len(r['rest'])==0 or (r['singok'] and r['single']))
