# simulated annealing over monotone circuits evaluated on key rows (exact by monotonicity)
# usage: sa.py EDGES mode S iters seed [init_circuit_json]
#  mode: size | or | and | lemd   ; S = number of gate slots
import sys, json, random, math
from rows import key_rows
E=[tuple(e) for e in json.loads(sys.argv[1])]; mode=sys.argv[2]; S=int(sys.argv[3]); IT=int(sys.argv[4]); random.seed(int(sys.argv[5]))
n=max(max(e) for e in E)+1
T,F,D=key_rows(n,E); rows=sorted(set(T+F+D)); Rn=len(rows)
f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
TGT=sum(1<<t for t,r in enumerate(rows) if f(r)); MASK=(1<<Rn)-1
X=[sum(1<<t for t,r in enumerate(rows) if (r>>v)&1) for v in range(n)]
DB=[1<<rows.index(((1<<n)-1)^(1<<v)) for v in range(n)]
deg=[sum(1 for e in E if v in e) for v in range(n)]
def rand_gate(i):
    j=random.randrange(i); k=random.randrange(i)
    while k==j: k=random.randrange(i)
    return [random.choice('&|'),min(j,k),max(j,k)]
if len(sys.argv)>6:
    init=json.loads(sys.argv[6]); C=[]
    # renumber to slots: pad at front with random gates? place given gates at the end
    pad=S-len(init); assert pad>=0
    C=[rand_gate(n+i) for i in range(pad)]
    m={}
    for idx,(i,o,j,k) in enumerate(init):
        jj=m.get(j,j); kk=m.get(k,k); m[i]=n+pad+idx; C.append([o,min(jj,kk),max(jj,kk)])
else:
    C=[rand_gate(n+i) for i in range(S)]
def evaluate(C):
    V=X[:]
    for o,j,k in C: V.append(V[j]&V[k] if o=='&' else V[j]|V[k])
    out=n+S-1; err=bin((V[out]^TGT)&MASK).count('1')
    live=set(); st=[out]
    while st:
        x=st.pop()
        if x>=n and x not in live: live.add(x); g=C[x-n]; st+= [g[1],g[2]]
    # function-duplicates among live gates are not merged here (upper bound on size)
    nor=sum(1 for x in live if C[x-n][0]=='|'); nand=len(live)-nor
    ex=0
    if mode=='lemd':
        ch=[0]*n
        for x in live:
            o,j,k=C[x-n]
            if o=='|':
                for v in range(n):
                    if (V[j]&DB[v])==0 or (V[k]&DB[v])==0: ch[v]+=1
        ex=sum(max(0,ch[v]-deg[v]+1) for v in range(n) if deg[v]>0)
    return err,len(live),nor,nand,ex
def cost(ev):
    err,sz,nor,nand,ex=ev
    base={'size':sz,'or':nor+0.05*sz,'and':nand+0.05*sz,'lemd':sz+3*ex}[mode]
    return 4*err+base
cur=evaluate(C); cc=cost(cur); best=None
import os; Tmp=float(os.environ.get("T0","2.0"))
for it in range(IT):
    Tt=Tmp*(1-it/IT)+0.05
    i=random.randrange(S); old=C[i]
    r=random.random()
    if r<0.2: new=[('&' if old[0]=='|' else '|'),old[1],old[2]]
    else:
        new=list(old); pos=random.choice([1,2]); new[pos]=random.randrange(n+i)
        if new[1]==new[2]: continue
        new=[new[0],min(new[1],new[2]),max(new[1],new[2])]
    C[i]=new; ev=evaluate(C); c2=cost(ev)
    if c2<=cc or random.random()<math.exp((cc-c2)/Tt):
        cur,cc=ev,c2
        if ev[0]==0 and (mode!='lemd' or ev[4]==0):
            key=(ev[1] if mode in('size','lemd') else ev[2] if mode=='or' else ev[3])
            if best is None or key<best[0]:
                best=(key,ev,[(n+t,g[0],g[1],g[2]) for t,g in enumerate(C)])
                print('BEST',key,ev,json.dumps(best[2]),flush=True)
    else: C[i]=old
print('final',best[:2] if best else None)
