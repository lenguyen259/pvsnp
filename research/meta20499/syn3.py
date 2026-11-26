import sys, itertools
from pysat.solvers import Cadical153
S=int(sys.argv[1]); mask=int(sys.argv[2]) if len(sys.argv)>2 else 279104447; N=6
rows=sorted(set((min(i,j),max(i,j)) for i in range(N) for j in range(N)))
def inp(r,w): return w==r[0] or w==r[1]
tgt={r:bool((mask>>(6*r[0]+r[1]))&1) for r in rows}
cnt=[0]
def nv(): cnt[0]+=1; return cnt[0]
cl=[]; val={}; typ={}  # gate: type var AND / OR / NOT via two bits
A={};O={};NT={}
sel={}
for g in range(S):
    ws=N+g
    pr=[(a,b) for a in range(ws) for b in range(a+1,ws)]
    nt=[(a,) for a in range(ws)]
    for p in pr+nt: sel[g,p]=nv()
    allp=pr+nt
    cl.append([sel[g,p] for p in allp])
    for p,q in itertools.combinations(allp,2): cl.append([-sel[g,p],-sel[g,q]])
    A[g]=nv()
    for r in rows: val[g,r]=nv()
def v(r,w): return inp(r,w) if w<N else val[w-N,r]
for g in range(S):
    ws=N+g
    for a in range(ws):
        for r in rows:
            x=v(r,a); z=val[g,r]; s=sel[g,(a,)]
            for xv in ([True,False] if not isinstance(x,bool) else [x]):
                base=[-s]
                if not isinstance(x,bool): base.append(-x if xv else x)
                cl.append(base+[z if not xv else -z])
        for b in range(a+1,ws):
            s=sel[g,(a,b)]
            for r in rows:
                x,y,z=v(r,a),v(r,b),val[g,r]
                for xv in ([True,False] if not isinstance(x,bool) else [x]):
                    for yv in ([True,False] if not isinstance(y,bool) else [y]):
                        base=[-s]
                        if not isinstance(x,bool): base.append(-x if xv else x)
                        if not isinstance(y,bool): base.append(-y if yv else y)
                        cl.append(base+[-A[g], z if (xv and yv) else -z])
                        cl.append(base+[A[g], z if (xv or yv) else -z])
for r in rows: cl.append([val[S-1,r] if tgt[r] else -val[S-1,r]])
# every earlier gate read later
for g in range(S-1):
    w=N+g
    cl.append([sel[h,p] for h in range(g+1,S) for p in [k for k in sel if k[0]==h and w in k[1]] ] if False else [vv for (h,p),vv in sel.items() if h>g and w in p])
s=Cadical153(bootstrap_with=cl)
if s.solve():
    M=set(l for l in s.get_model() if l>0)
    gs=[]
    for g in range(S):
        p=[p for (gg,p),vv in sel.items() if gg==g and vv in M][0]
        gs.append((('not' if len(p)==1 else ('and' if A[g] in M else 'or')),p))
    print('SAT',gs)
else: print('UNSAT',S)
