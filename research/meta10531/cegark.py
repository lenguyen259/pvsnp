# CEGAR exact synthesis for the L-meta-10531 edge function over the model's basis:
# gates AND(a,b), OR(a,b) (a<b distinct wires) and NOT(a); every gate counts; output = last gate.
# Usage: cegar.py s [seed] [--sb] [--time T]
import sys, random, time, json
from pysat.solvers import Solver
n = 9
E = [(0,5),(0,6),(1,6),(2,6),(1,7),(3,7),(4,7),(2,8),(3,8),(5,8),(7,8)]
def f(t): return int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
args=[a for a in sys.argv[1:] if not a.startswith('--')]
s=int(args[0]); seed=int(args[1]) if len(args)>1 else 0
nonot='--mono' in sys.argv
solvername=[a.split('=')[1] for a in sys.argv if a.startswith('--solver=')] or ['cadical195']
solvername=solvername[0]
random.seed(seed)
cnt=[0]
def nv(): cnt[0]+=1; return cnt[0]
CL=[]
def add(c): CL.append(c)
# choices per gate: list of (kind, j, k) kind 'u' (NOT j) or 'b' (j<k)
ch=[]; sel=[]; op=[]
for i in range(s):
    m=n+i; L=[]
    for j in range(m):
        if not nonot: L.append(('u',j,None))
    for k in range(m):
        for j in range(k):
            L.append(('b',j,k))
    # colex order on (k,j) for binary, unary first
    ch.append(L); sel.append([nv() for _ in L]); op.append(nv())
    add(list(sel[i]))
    for a in range(len(L)):
        for b in range(a+1,len(L)): add([-sel[i][a],-sel[i][b]])
# NOT of a NOT gate is useless; NOT of a NOT input-free... forbid NOT(NOT)
isnot=[]
for i in range(s):
    v=nv(); isnot.append(v)
    us=[sel[i][a] for a,c in enumerate(ch[i]) if c[0]=='u']
    for u in us: add([-u,v])
    add([-v]+us)
for i in range(s):
    for a,c in enumerate(ch[i]):
        if c[0]=='u' and c[1]>=n: add([-sel[i][a],-isnot[c[1]-n]])
        if c[0]=='u': pass
    add([-isnot[i],op[i]])  # op irrelevant for NOT; fix it
# each non-output gate used
uses={}
for i in range(s):
    for a,c in enumerate(ch[i]):
        for w in (c[1],c[2]):
            if w is not None and w>=n: uses.setdefault(w-n,[]).append(sel[i][a])
for g in range(s-1): add(uses.get(g,[]))
# ordering: if gate i+1 does not read gate i, then choice index(i) <= choice index(i+1)
# choice index uses a common key on (kind,j,k)
def key(c):
    return (0,c[1],0) if c[0]=='u' else (1,c[2],c[1])
if '--sb' in sys.argv or True:
    for i in range(s-1):
        keys_i=[key(c) for c in ch[i]]
        for b,c in enumerate(ch[i+1]):
            if n+i in (c[1],c[2]): continue
            kb=key(c)
            for a,ca in enumerate(ch[i]):
                if keys_i[a]>kb: add([-sel[i+1][b],-sel[i][a]])
                elif keys_i[a]==kb and c[0]=='b':
                    # same inputs: allow only AND then OR order (op i=0 -> AND? op var: True=OR)
                    add([-sel[i+1][b],-sel[i][a],-op[i]]); add([-sel[i+1][b],-sel[i][a],op[i+1]])
                elif keys_i[a]==kb: add([-sel[i+1][b],-sel[i][a]])
rows=[]; X={}
def addrow(t):
    rows.append(t)
    val=lambda w: ((t>>w)&1) if w<n else None
    xs=[nv() for i in range(s)]; X[t]=xs
    def lit(w,v):  # literal "wire w has value v"; returns True/False constant or literal
        if w<n: return ((t>>w)&1)==v
        return xs[w-n] if v else -xs[w-n]
    for i in range(s):
        for a,c in enumerate(ch[i]):
            sv=sel[i][a]
            if c[0]=='u':
                for v in (0,1):
                    l=lit(c[1],v)
                    # wire=v -> x_i = 1-v
                    out = xs[i] if v==0 else -xs[i]
                    if l is True: add([-sv,out])
                    elif l is False: pass
                    else: add([-sv,-l,out])
            else:
                j,k=c[1],c[2]
                for a1 in (0,1):
                    for b1 in (0,1):
                        lj=lit(j,a1); lk=lit(k,b1)
                        if lj is False or lk is False: continue
                        pre=[-sv]+([-lj] if lj is not True else [])+([-lk] if lk is not True else [])
                        if a1==b1:
                            add(pre+[xs[i] if a1 else -xs[i]])
                        else:
                            add(pre+[-op[i],xs[i]]); add(pre+[op[i],-xs[i]])
    add([xs[s-1] if f(t) else -xs[s-1]])
def decode(model):
    M=set(l for l in model if l>0); gates=[]
    for i in range(s):
        a=[a for a in range(len(ch[i])) if sel[i][a] in M][0]; c=ch[i][a]
        if c[0]=='u': gates.append(('not',c[1]))
        else: gates.append(('or' if op[i] in M else 'and',c[1],c[2]))
    return gates
def ev(gates,t):
    w=[(t>>j)&1 for j in range(n)]
    for g in gates:
        if g[0]=='not': w.append(1-w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w[-1]
# initial rows: edge minterms, maximal independent sets, zero
init=set([0])
for a,b in E: init.add((1<<a)|(1<<b))
F=[r for r in range(512) if not f(r)]
for r in F:
    if not any(q!=r and q&r==r for q in F): init.add(r)
for t in sorted(init): addrow(t)
import subprocess,os
KIS='/home/user/pvsnp/research/L-meta-612/petersen19/kissat'
tag='k%d_%d%s'%(s,seed,'m' if nonot else '')
extra=[a.split('=')[1] for a in sys.argv if a.startswith('--rand=')]
for t in random.sample(range(512),int(extra[0]) if extra else 0):
    if t not in X: addrow(t)
tlim=[a.split('=')[1] for a in sys.argv if a.startswith('--tl=')]
t0=time.time(); it=0
class _S: pass
S=_S()
while True:
    it+=1
    fn='/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/%s.cnf'%tag
    with open(fn,'w') as fh:
        fh.write('p cnf %d %d\n'%(cnt[0],len(CL)))
        for c in CL: fh.write(' '.join(map(str,c))+' 0\n')
    cmd=[KIS,'-q']+(['--time='+tlim[0]] if tlim else [])+[fn]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if 'UNSATISFIABLE' in r.stdout: ok=False
    elif 's SATISFIABLE' in r.stdout:
        ok=True; mod=[int(v) for l in r.stdout.splitlines() if l.startswith('v') for v in l.split()[1:]]
        S.get_model=lambda: mod
    else:
        print('UNKNOWN', time.time()-t0); break
    if not ok:
        print('UNSAT s=%d rows=%d time=%.1f'%(s,len(rows),time.time()-t0)); print('rows',sorted(rows)); break
    g=decode(S.get_model())
    bad=[t for t in range(512) if ev(g,t)!=f(t)]
    print('iter',it,'rows',len(rows),'bad',len(bad),'t=%.1f'%(time.time()-t0),flush=True)
    if not bad:
        print('FOUND',json.dumps(g)); break
    for t in random.sample(bad,min(2,len(bad))): addrow(t)
