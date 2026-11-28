# cube runner: cubes.py JOBFILE RESULTFILE PAR TIMEOUT
# JOBFILE: lines "name<TAB>s<TAB>enc5 args (shell-split)". Each job: enc5 -> CNF -> kissat (time limit) -> decode.
# Results appended as JSON lines; jobs already in RESULTFILE are skipped.
import sys, json, subprocess, shlex, os, time
from concurrent.futures import ThreadPoolExecutor
jf, rf, par, to = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
SCR='/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/cubes'
os.makedirs(SCR,exist_ok=True)
done=set()
if os.path.exists(rf):
    for l in open(rf):
        try: done.add(json.loads(l)['name'])
        except Exception: pass
jobs=[l.rstrip('\n').split('\t') for l in open(jf) if l.strip()]
jobs=[j for j in jobs if j[0] not in done]
def run(j):
    name,s,args=j; cnf=f'{SCR}/{name}.cnf'; meta=f'{SCR}/{name}.meta'
    t0=time.time()
    subprocess.run(['python3','enc5.py',s]+shlex.split(args)+['--dimacs',cnf,'--meta',meta],capture_output=True)
    out=subprocess.run(['python3','runk.py',cnf,meta,str(to)],capture_output=True,text=True).stdout
    res=[l for l in out.splitlines() if l.startswith('RESULT') or l.startswith('VERIF')]
    rec={'name':name,'s':int(s),'args':args,'res':' | '.join(res),'wall':round(time.time()-t0,1)}
    with open(rf,'a') as fh: fh.write(json.dumps(rec)+'\n')
    for p in (cnf,meta):
        try: os.remove(p)
        except OSError: pass
    print(name,rec['res'],flush=True)
with ThreadPoolExecutor(par) as ex: list(ex.map(run,jobs))
