import json,sys
from canon import canon
def rechain(c,n=10):
    N=n+len(c); users={g:[] for g in range(N)}
    for idx,(o,j,k) in enumerate(c): users[j].append(n+idx); users[k].append(n+idx)
    op=lambda g: c[g-n][0]
    isint=lambda g: g>=n and len(users[g])==1 and op(users[g][0])==op(g)
    roots=[g for g in range(n,N) if not isint(g)]
    newc={}  # build node list as expressions
    def leaves(g,o):
        if g>=n and (g==r or isint(g)) and op(g)==o:
            _,j,k=c[g-n]; return leaves(j,o)+leaves(k,o)
        return [g]
    expr={}
    for r in roots:
        o=op(r); ls=sorted(set(leaves(r,o))); expr[r]=(o,ls)
    # emit in topological order: build new circuit
    out=[]; pos={i:i for i in range(n)}
    def emit(r):
        if r in pos: return pos[r]
        o,ls=expr[r]; ps=[emit(l) for l in ls]
        x=ps[0]
        for p in ps[1:]:
            out.append([o,min(x,p),max(x,p)]); x=n+len(out)-1
        pos[r]=x; return x
    for r in sorted(roots): emit(r)
    return out
def normal(c):
    for _ in range(50):
        c2=canon(rechain(c))
        # canon may change leaf order; rechain sorts leaves by current positions
        if c2==c: return c
        c=c2
    raise Exception('no fixpoint')
if __name__=='__main__': print(json.dumps(normal(json.loads(sys.argv[1]))))
