# Exact-synthesis encoding for the L-meta-10531 edge function in the HasCircuitSize model:
# gates AND(a,b), OR(a,b) with a<b distinct wires, NOT(a); every gate counts; output = last gate.
# (AND/OR on a repeated wire is a copy, fan-in<2 AND/OR is a copy/constant: never in a minimal circuit.)
# Symmetry breaking: every non-output gate is read; NOT(NOT g) forbidden; adjacent independent gates
# in colex key order (lexicographically least topological order, valid by an exchange argument);
# equal keys: only AND then OR (duplicates are non-minimal).
import random
n = 9
E = [(0,5),(0,6),(1,6),(2,6),(1,7),(3,7),(4,7),(2,8),(3,8),(5,8),(7,8)]
def f(t): return int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
def key(c): return (0,c[1],0) if c[0]=='u' else (1,c[2],c[1])
class Enc:
    def __init__(s_, s, mono=False, add=None, extra_sb=True):
        s_.s=s; s_.cnt=0; s_.CL=[]; s_.addc = add or s_.CL.append
        add=s_.addc; nv=s_.nv
        s_.ch=[];s_.sel=[];s_.op=[]
        for i in range(s):
            m=n+i; L=[] if mono else [('u',j,None) for j in range(m)]
            L+=[('b',j,k) for k in range(m) for j in range(k)]
            s_.ch.append(L); s_.sel.append([nv() for _ in L]); s_.op.append(nv())
            add(list(s_.sel[i]))
            for a in range(len(L)):
                for b in range(a+1,len(L)): add([-s_.sel[i][a],-s_.sel[i][b]])
        ch,sel,op=s_.ch,s_.sel,s_.op
        s_.isnot=[nv() for i in range(s)]
        for i in range(s):
            us=[sel[i][a] for a,c in enumerate(ch[i]) if c[0]=='u']
            for u in us: add([-u,s_.isnot[i]])
            add([-s_.isnot[i]]+us)
            add([-s_.isnot[i],op[i]])
            for a,c in enumerate(ch[i]):
                if c[0]=='u' and c[1]>=n: add([-sel[i][a],-s_.isnot[c[1]-n]])
        uses={}
        for i in range(s):
            for a,c in enumerate(ch[i]):
                for w in (c[1],c[2]):
                    if w is not None and w>=n: uses.setdefault(w-n,[]).append(sel[i][a])
        for g in range(s-1): add(uses.get(g,[]))
        for i in range(s-1):
            keys_i=[key(c) for c in ch[i]]
            for b,c in enumerate(ch[i+1]):
                if n+i in (c[1],c[2]): continue
                kb=key(c)
                for a,ca in enumerate(ch[i]):
                    if keys_i[a]>kb: add([-sel[i+1][b],-sel[i][a]])
                    elif keys_i[a]==kb and c[0]=='b':
                        add([-sel[i+1][b],-sel[i][a],-op[i]]); add([-sel[i+1][b],-sel[i][a],op[i+1]])
                    elif keys_i[a]==kb: add([-sel[i+1][b],-sel[i][a]])
        if extra_sb:
            # binary gate reading g and NOT(g): constant -> forbidden (sound structural pruning)
            for i in range(s):
                for a,c in enumerate(ch[i]):
                    if c[0]=='b' and c[2]>=n:
                        k=c[2]-n
                        for b2,c2 in enumerate(ch[k]):
                            if c2[0]=='u' and c2[1]==c[1]: add([-sel[i][a],-sel[k][b2]])
                # AND(a, AND(a,b)) / OR(a, OR(a,b)) are copies: forbidden
                for a,c in enumerate(ch[i]):
                    if c[0]!='b': continue
                    for (p,q) in ((c[1],c[2]),(c[2],c[1])):
                        if q<n: continue
                        k=q-n
                        for b2,c2 in enumerate(ch[k]):
                            if c2[0]=='b' and p in (c2[1],c2[2]):
                                add([-sel[i][a],-sel[k][b2],op[i],op[k]])
                                add([-sel[i][a],-sel[k][b2],-op[i],-op[k]])
        s_.X={}
    def nv(s_): s_.cnt+=1; return s_.cnt
    def addrow(s_,t):
        add=s_.addc; s=s_.s
        xs=[s_.nv() for i in range(s)]; s_.X[t]=xs
        def lit(w,v):
            if w<n: return ((t>>w)&1)==v
            return xs[w-n] if v else -xs[w-n]
        for i in range(s):
            for a,c in enumerate(s_.ch[i]):
                sv=s_.sel[i][a]
                if c[0]=='u':
                    for v in (0,1):
                        l=lit(c[1],v); out=xs[i] if v==0 else -xs[i]
                        if l is True: add([-sv,out])
                        elif l is not False: add([-sv,-l,out])
                else:
                    for a1 in (0,1):
                        for b1 in (0,1):
                            lj=lit(c[1],a1); lk=lit(c[2],b1)
                            if lj is False or lk is False: continue
                            pre=[-sv]+([-lj] if lj is not True else [])+([-lk] if lk is not True else [])
                            if a1==b1: add(pre+[xs[i] if a1 else -xs[i]])
                            else: add(pre+[-s_.op[i],xs[i]]); add(pre+[s_.op[i],-xs[i]])
        add([xs[s-1] if f(t) else -xs[s-1]])
    def decode(s_,model):
        M=set(l for l in model if l>0); G=[]
        for i in range(s_.s):
            c=s_.ch[i][[a for a in range(len(s_.ch[i])) if s_.sel[i][a] in M][0]]
            G.append(('not',c[1]) if c[0]=='u' else (('or' if s_.op[i] in M else 'and'),c[1],c[2]))
        return G
    def assume(s_,G):
        """literals fixing circuit G (canonical order assumed)"""
        A=[]
        for i,g in enumerate(G):
            c=('u',g[1],None) if g[0]=='not' else ('b',min(g[1:]),max(g[1:]))
            A.append(s_.sel[i][s_.ch[i].index(c)])
            if g[0]!='not': A.append(s_.op[i] if g[0]=='or' else -s_.op[i])
        return A
def ev(G,t):
    w=[(t>>j)&1 for j in range(n)]
    for g in G:
        if g[0]=='not': w.append(1-w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w[-1]
def check(G): return [t for t in range(512) if ev(G,t)!=f(t)]
def canon(G):
    """lexicographically least topological order (greedy min key); returns reordered circuit"""
    N=len(G); pos={j:j for j in range(n)}; placed=[]; out=[]
    rem=set(range(N))
    while rem:
        best=None
        for g in rem:
            ins=G[g][1:]
            if all((w<n) or (w-n) in placed for w in ins):
                if g==N-1 and len(rem)>1: continue
                iw=[pos[w] if w<n else pos[w] for w in ins]
                if G[g][0]=='not': c=('u',iw[0],None)
                else: c=('b',min(iw),max(iw))
                k=(key(c),0 if G[g][0]=='and' else 1)
                if best is None or k<best[0]: best=(k,g,iw)
        k,g,iw=best
        pos[n+g]=n+len(out); placed.append(g); rem.discard(g)
        out.append((G[g][0],*sorted(iw)) if G[g][0]!='not' else ('not',iw[0]))
    return out
def initial_rows():
    init=set([0])
    for a,b in E: init.add((1<<a)|(1<<b))
    F=[r for r in range(512) if not f(r)]
    for r in F:
        if not any(q!=r and q&r==r for q in F): init.add(r)
    return sorted(init)
