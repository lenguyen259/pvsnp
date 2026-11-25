# CEGAR driver for enc2. run2.py G|H s seed [--mono] [--rand=K] [--tl=sec] [--maxnot=j] [--cadical]
import sys,time,random,json,subprocess
import enc2
from enc2 import Enc2
which=sys.argv[1]; s=int(sys.argv[2]); seed=int(sys.argv[3])
opt={a.split('=')[0]:(a.split('=')[1] if '=' in a else True) for a in sys.argv[4:]}
if which=='H':
    enc2.n=8; enc2.E[:]=[(0,4),(0,5),(1,5),(2,5),(1,6),(3,6),(2,7),(3,7),(4,7),(6,7)]
random.seed(seed); n=enc2.n; N=1<<n; f=enc2.f
mono='--mono' in opt
e=Enc2(s,mono=mono)
if '--maxnot' in opt:
    from pysat.card import CardEnc
    cnf=CardEnc.atmost(lits=e.isnot,bound=int(opt['--maxnot']),top_id=e.cnt)
    for c in cnf.clauses: e.addc(c)
    e.cnt=max(e.cnt,cnf.nv)
rows={0}
for a,b in enc2.E: rows.add((1<<a)|(1<<b))
Fs=[r for r in range(N) if not f(r)]
rows|={r for r in Fs if not any(q!=r and q&r==r for q in Fs)}
if not mono: rows|=set(random.sample(range(N),int(opt.get('--rand',0))))
if '--all' in opt: rows=set(range(N))
for t in sorted(rows): e.addrow(t)
def ev(G,t):
    w=[(t>>j)&1 for j in range(n)]
    for g in G:
        if g[0]=='not': w.append(1-w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w[-1]
KIS='/home/user/pvsnp/research/L-meta-612/petersen19/kissat'
tag='%s%d_%d%s_%s'%(which,s,seed,'m' if mono else '',opt.get('--maxnot','x'))
fn='/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/m10531/%s.cnf'%tag
t0=time.time(); it=0
if '--cadical' in opt:
    from pysat.solvers import Solver
    S=Solver(name='cadical195'); 
    for c in e.CL: S.add_clause(c)
    e.addc=S.add_clause
while True:
    it+=1
    if '--cadical' in opt:
        ok=S.solve()
        if not ok:
            print('UNSAT',which,'s=%d'%s,'rows=%d'%len(e.X),'t=%.1f'%(time.time()-t0)); print('rows',sorted(e.X)); break
        mod=S.get_model()
    else:
        with open(fn,'w') as fh:
            fh.write('p cnf %d %d\n'%(e.cnt,len(e.CL)))
            for c in e.CL: fh.write(' '.join(map(str,c))+' 0\n')
        cmd=[KIS,'-q']+(['--time='+opt['--tl']] if '--tl' in opt else [])+[fn]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if 's UNSATISFIABLE' in r.stdout:
            print('UNSAT',which,'s=%d'%s,'rows=%d'%len(e.X),'t=%.1f'%(time.time()-t0)); print('rows',sorted(e.X)); break
        if 's SATISFIABLE' not in r.stdout:
            print('UNKNOWN t=%.1f'%(time.time()-t0),'rows',len(e.X)); break
        mod=[int(v) for l in r.stdout.splitlines() if l.startswith('v') for v in l.split()[1:]]
    G=e.decode(mod); bad=[t for t in range(N) if ev(G,t)!=f(t)]
    print('iter',it,'rows',len(e.X),'bad',len(bad),'t=%.1f'%(time.time()-t0),flush=True)
    if not bad: print('FOUND',json.dumps(G)); break
    for t in random.sample(bad,min(4,len(bad))): e.addrow(t)
