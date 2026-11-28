# bottom-up prover: python3 rec4.py CLASS --fam A2,N,B,B1,BB --sizes 9,10 [--extra "..."] [--check] --timeout T
import sys, json, subprocess, time, argparse, os
import networkx as nx
from lib import *
ap=argparse.ArgumentParser(); ap.add_argument('c',type=int); ap.add_argument('--fam',default='A2,N,B,B1,BB')
ap.add_argument('--sizes'); ap.add_argument('--extra',default=''); ap.add_argument('--check',action='store_true')
ap.add_argument('--timeout',type=float,default=600); ap.add_argument('--tag',default='')
ap.add_argument('--noviol',action='store_true'); ap.add_argument('--assume',action='store_true'); ap.add_argument('--dry',action='store_true')
A=ap.parse_args()
PROVED=json.load(open('proved.json')) if os.path.exists('proved.json') else {}
if '--assume' in sys.argv: PROVED=json.load(open('proved_assume.json'))
def L(c):
    if c is None: return 0
    I=info(c)
    if nx.is_forest(classes[c][0]) or I['maxdeg']<=2: return I['phi']   # Theorems F1, F2
    if str(c) in PROVED: return PROVED[str(c)]
    raise Exception('class %d not proved'%c)
I=info(A.c); E=I['E']; phi=I['phi']
R=restrictions(E,A.fam.split(','))
def LB(F,Hc):
    if Hc is None: return F-1
    return F+L(Hc)
sizes=[int(x) for x in A.sizes.split(',')] if A.sizes else list(range(1,phi))
for s in sizes:
    rest=[[S0,S1,s-LB(F,Hc)] for S0,S1,F,Hc in R]
    rest=[r for r in rest if r[2]<s]
    if any(r[2]<0 for r in rest) and not A.check: print('CLASS',A.c,'s',s,'TRIV-UNSAT',flush=True); continue
    cmd=['python3','enc4.py',str(s),'--graph',json.dumps(E),'--chain','--factc','--rest',json.dumps(rest),'--timeout',str(A.timeout)]
    if not (A.check or A.noviol): cmd.append('--viol')
    if A.c==0 and '--orb' not in A.extra: cmd.append('--symb')
    if A.extra: cmd+=A.extra.split()
    if A.dry: open("lastcmd.json","w").write(json.dumps(cmd)); print(' '.join(cmd[:3]),len(rest)); continue
    t0=time.time(); open("lastcmd.json","w").write(json.dumps(cmd))
    try: out=subprocess.run(cmd,capture_output=True,text=True,timeout=A.timeout+30).stdout
    except subprocess.TimeoutExpired: out='RESULT TIMEOUT %.0fs'%(time.time()-t0)
    line=[l for l in out.splitlines() if l.startswith('RESULT') or 'VERIF' in l]
    print('CLASS',A.c,'phi',phi,'s',s,A.tag,'nrest',len(rest),' | '.join(line) if line else out[-500:],flush=True)
