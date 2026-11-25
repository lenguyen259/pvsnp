# run kissat on a CNF with timeout; decode model via meta and verify on all 1024 inputs
import sys, json, subprocess, time
cnf, meta, to = sys.argv[1], sys.argv[2], int(sys.argv[3])
extra=sys.argv[4:]
t0=time.time()
p=subprocess.run(['./kissat','-q','--time=%d'%to]+extra+[cnf],capture_output=True,text=True)
out=p.stdout; dt=time.time()-t0
if 's SATISFIABLE' in out:
    lits=set()
    for l in out.splitlines():
        if l.startswith('v '): lits|={int(x) for x in l[2:].split() if int(x)>0}
    M=json.load(open(meta)); n=M['n']; s=M['s']; E=M['E']; c=[]
    for i in range(n,n+s):
        j=[int(a) for a,x in M['l'][str(i)].items() if x in lits][0]; k=[int(a) for a,x in M['r'][str(i)].items() if x in lits][0]
        c.append(['&' if M['o'][str(i)] in lits else '|',j,k])
    ok=True
    for r in range(1<<n):
        v=[(r>>u)&1 for u in range(n)]
        for o,j,k in c: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
        if v[-1]!=int(any((r>>a)&1 and (r>>b)&1 for a,b in E)): ok=False; break
    print('VERIFIED' if ok else 'VERIFY-FAIL',json.dumps(c))
    print('RESULT SAT %.1fs'%dt)
elif 's UNSATISFIABLE' in out: print('RESULT UNSAT %.1fs'%dt)
else: print('RESULT TIMEOUT %.1fs'%dt)
