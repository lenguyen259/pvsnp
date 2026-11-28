# Simulated-annealing search for a size-s monotone circuit computing f_P (truth tables as 1024-bit ints).
# Any circuit with cost 0 is re-verified gate by gate on all 1024 inputs and printed.
import random, sys, math, time
from plib import PET, n, verify
s=int(sys.argv[1]); seed=int(sys.argv[2]); budget=float(sys.argv[3])
random.seed(seed)
M=1<<n; FULL=(1<<M)-1
X=[sum(1<<r for r in range(M) if (r>>u)&1) for u in range(n)]
FT=0
for a,b in PET: FT|=X[a]&X[b]
# weight: core rows heavier
def pc(x): return bin(x).count('1')
def rand_gate(i):
    j,k=random.sample(range(i),2); return [random.choice('&|'),min(j,k),max(j,k)]
def evalc(c):
    v=list(X)
    for o,j,k in c: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
    return v
def cost(c):
    v=evalc(c); return pc(v[-1]^FT)
t0=time.time(); best=None; restarts=0
while time.time()-t0<budget:
    c=[rand_gate(n+i) for i in range(s)]; cur=cost(c); T=3.0; restarts+=1
    for it in range(200000):
        i=random.randrange(s); old=c[i]
        r=random.random()
        if r<0.2: c[i]=['&' if old[0]=='|' else '|',old[1],old[2]]
        else: c[i]=rand_gate(n+i)
        new=cost(c)
        if new<=cur or random.random()<math.exp((cur-new)/T): cur=new
        else: c[i]=old
        T=max(0.05,T*0.99997)
        if cur==0:
            ok=verify(c); print('FOUND' if ok else 'BADVERIFY',c,flush=True)
            if ok: sys.exit(0)
    if best is None or cur<best: best=cur
print('restarts',restarts,'best',best)
