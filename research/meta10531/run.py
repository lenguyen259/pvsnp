# CEGAR driver. run.py G|H s seed [--mono] [--rand=K] [--solver=kissat|cadical] [--tl=sec] [--maxnot=j]
import sys,time,random,json,subprocess
import enc
from enc import Enc
which=sys.argv[1]; s=int(sys.argv[2]); seed=int(sys.argv[3])
opt={a.split('=')[0]:(a.split('=')[1] if '=' in a else True) for a in sys.argv[4:]}
if which=='H':
    enc.n=8; enc.E[:]=[(0,4),(0,5),(1,5),(2,5),(1,6),(3,6),(2,7),(3,7),(4,7),(6,7)]
random.seed(seed)
N=1<<enc.n
mono='--mono' in opt
e=Enc(s,mono=mono)
if '--maxnot' in opt:
    # at most j NOT gates: sequential counter
    from pysat.card import CardEnc
    cnf=CardEnc.atmost(lits=e.isnot,bound=int(opt['--maxnot']),top_id=e.cnt)
    for c in cnf.clauses: e.addc(c)
    e.cnt=max(e.cnt,cnf.nv)
rows=enc.initial_rows() if enc.n==9 else None
if rows is None:
    rows={0}
    for a,b in enc.E: rows.add((1<<a)|(1<<b))
    Fs=[r for r in range(N) if not enc.f(r)]
    rows|={r for r in Fs if not any(q!=r and q&r==r for q in Fs)}
    rows=sorted(rows)
if not mono:
    rows=sorted(set(rows)|set(random.sample(range(N),int(opt.get('--rand',0)))))
for t in rows: e.addrow(t)
def ev(G,t):
    w=[(t>>j)&1 for j in range(enc.n)]
    for g in G:
        if g[0]=='not': w.append(1-w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w[-1]
KIS='/home/user/pvsnp/research/L-meta-612/petersen19/kissat'
tag='%s%d_%d%s_%s'%(which,s,seed,'m' if mono else '',opt.get('--maxnot','x'))
fn='/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/%s.cnf'%tag
t0=time.time(); it=0
while True:
    it+=1
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
    G=e.decode(mod); bad=[t for t in range(N) if ev(G,t)!=enc.f(t)]
    print('iter',it,'rows',len(e.X),'bad',len(bad),'t=%.1f'%(time.time()-t0),flush=True)
    if not bad: print('FOUND',json.dumps(G)); break
    for t in random.sample(bad,min(4,len(bad))): e.addrow(t)
