import sys, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def target_tt(n, edges, forced=()):
    tt=[]
    for r in range(1<<n):
        v=any((r>>a)&1 and (r>>b)&1 for a,b in edges) or any((r>>f)&1 for f in forced)
        tt.append(v)
    return tt

def exists_circuit(n, tt, s, rows=None, timeout=None, want_model=False, max_and=None, max_or=None, enum_all=None):
    """monotone AND/OR fan-in-2 circuit with exactly s gates, last gate = output"""
    if rows is None: rows=range(1<<n)
    pool=IDPool(); cl=[]
    N=n+s
    pairs={i:[(j,k) for j in range(i) for k in range(j+1,i)] for i in range(n,N)}
    sel=lambda i,p: pool.id(('s',i,p))
    op=lambda i: pool.id(('o',i))       # true = AND
    def val(i,r):
        if i<n: return True if (r>>i)&1 else False
        return pool.id(('v',i,r))
    def add(lits):
        out=[]
        for l in lits:
            if l is True: return
            if l is False: continue
            out.append(l)
        cl.append(out)
    def neg(l):
        if l is True: return False
        if l is False: return True
        return -l
    for i in range(n,N):
        lits=[sel(i,p) for p in range(len(pairs[i]))]
        cl.append(lits)
        enc=CardEnc.atmost(lits=lits,bound=1,vpool=pool,encoding=EncType.seqcounter)
        cl.extend(enc.clauses)
        for p,(j,k) in enumerate(pairs[i]):
            sp=sel(i,p); o=op(i)
            for r in rows:
                a,b,c=val(j,r),val(k,r),val(i,r)
                # AND
                add([-sp,-o,neg(a),neg(b),c]); add([-sp,-o,a,neg(c)]); add([-sp,-o,b,neg(c)])
                # OR
                add([-sp,o,neg(a),c]); add([-sp,o,neg(b),c]); add([-sp,o,a,b,neg(c)])
    out=N-1
    for r in rows:
        add([val(out,r)] if tt[r] else [neg(val(out,r))])
    # every non-output gate used
    for g in range(n,N-1):
        cl.append([sel(i,p) for i in range(g+1,N) for p,(j,k) in enumerate(pairs[i]) if g in (j,k)])
    # every input that the function depends on is fine automatically
    # symmetry: consecutive independent gates in lex order
    for i in range(n,N-1):
        for p,(j,k) in enumerate(pairs[i]):
            for q,(j2,k2) in enumerate(pairs[i+1]):
                if i not in (j2,k2) and (j2,k2)<(j,k):
                    cl.append([-sel(i,p),-sel(i+1,q)])
    ops=[op(i) for i in range(n,N)]
    if max_and is not None:
        cl.extend(CardEnc.atmost(lits=ops,bound=max_and,vpool=pool,encoding=EncType.seqcounter).clauses)
    if max_or is not None:
        cl.extend(CardEnc.atmost(lits=[-o for o in ops],bound=max_or,vpool=pool,encoding=EncType.seqcounter).clauses)
    S=Cadical153(bootstrap_with=cl)
    if enum_all is not None:
        allm=[]
        while len(allm)<enum_all and S.solve():
            m=set(l for l in S.get_model() if l>0)
            model=[];blk=[]
            for i in range(n,N):
                for p,(j,k) in enumerate(pairs[i]):
                    if sel(i,p) in m:
                        model.append((i,'&' if op(i) in m else '|',j,k)); blk+= [-sel(i,p), (-op(i) if op(i) in m else op(i))]
            allm.append(model); S.add_clause(blk)
        S.delete(); return allm
    res=S.solve()
    model=None
    if res and want_model:
        m=set(l for l in S.get_model() if l>0)
        model=[]
        for i in range(n,N):
            for p,(j,k) in enumerate(pairs[i]):
                if sel(i,p) in m: model.append((i,'&' if op(i) in m else '|',j,k))
    S.delete()
    return res, model
