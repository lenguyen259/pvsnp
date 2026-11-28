import sys, itertools
from pysat.solvers import Cadical153
mask=int(sys.argv[2]) if len(sys.argv)>2 else 3242; n,m=int(sys.argv[3]) if len(sys.argv)>3 else 3,int(sys.argv[4]) if len(sys.argv)>4 else 5; S=int(sys.argv[1])
rows=[(u,v) for u in range(n) for v in range(m)]
I=n+m
def inp(r,w):
    u,v=r
    return (w==u) if w<n else (w-n==v)
cnt=[0]
def nv(): cnt[0]+=1; return cnt[0]
sel={}; op={}; val={}
cl=[]
for g in range(S):
    ws=I+g
    pairs=[(a,b) for a in range(ws) for b in range(a+1,ws)]
    for p in pairs: sel[g,p]=nv()
    cl.append([sel[g,p] for p in pairs])
    for p,q in itertools.combinations(pairs,2): cl.append([-sel[g,p],-sel[g,q]])
    op[g]=nv()  # true=AND
    for r in rows: val[g,r]=nv()
def v_of(r,w):
    if w<I: return inp(r,w)
    return val[w-I,r]
for g in range(S):
    ws=I+g
    for a in range(ws):
        for b in range(a+1,ws):
            s=sel[g,(a,b)]
            for r in rows:
                x,y,z=v_of(r,a),v_of(r,b),val[g,r]
                def lit(t): return t
                # build clauses with constants
                def add(c,extra):
                    c=[l for l in c]
                    cl.append(extra+c)
                for xv in ([True,False] if not isinstance(x,bool) else [x]):
                    for yv in ([True,False] if not isinstance(y,bool) else [y]):
                        base=[-s]
                        if not isinstance(x,bool): base.append(-x if xv else x)
                        if not isinstance(y,bool): base.append(-y if yv else y)
                        # AND
                        cl.append(base+[-op[g], z if (xv and yv) else -z])
                        cl.append(base+[op[g], z if (xv or yv) else -z])
out=nv()  # output selector among gates: pick last-or-any
osel=[nv() for g in range(S)]
cl.append([osel[S-1]])
# symmetry: every gate g<S-1 is read by a later gate; second input nondecreasing
for g in range(S-1):
    w=I+g
    cl.append([sel[h,p] for h in range(g+1,S) for p in [(a,b) for a in range(I+h) for b in range(a+1,I+h)] if w in p])
for g in range(S-1):
    for p in [(a,b) for a in range(I+g) for b in range(a+1,I+g)]:
        for q in [(a,b) for a in range(I+g+1) for b in range(a+1,I+g+1)]:
            if q[1]<p[1]: cl.append([-sel[g,p],-sel[g+1,q]])
for r in rows:
    t=bool((mask>>(m*r[0]+r[1]))&1)
    for g in range(S): cl.append([-osel[g], val[g,r] if t else -val[g,r]])
s=Cadical153(bootstrap_with=cl)
if s.solve():
    M=set(l for l in s.get_model() if l>0)
    gs=[]
    for g in range(S):
        p=[p for (gg,p),v in sel.items() if gg==g and v in M][0]
        gs.append(('and' if op[g] in M else 'or',p))
    o=[g for g in range(S) if osel[g] in M][0]
    print('SAT',gs,'out gate',o)
else: print('UNSAT',S)
