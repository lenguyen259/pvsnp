# SA for "sav" counterexamples: correct circuit (all 2^n rows) where every v has ORsav(v) < deg(v),
# ORsav(v) = #OR(reduce(C)) - #OR(reduce(C | x_v:=0)).  Also modes: lemd (charge-based).
# usage: sa2.py EDGES S iters seed T0 [init "i=a|b ..."]
import sys, json, random, math, re
E=[tuple(e) for e in json.loads(sys.argv[1])]; S=int(sys.argv[2]); IT=int(sys.argv[3]); random.seed(int(sys.argv[4])); T0=float(sys.argv[5])
n=max(max(e) for e in E)+1; NR=1<<n; M=(1<<NR)-1
X=[sum(1<<r for r in range(NR) if (r>>v)&1) for v in range(n)]
TGT=sum(1<<r for r in range(NR) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
deg=[sum(1 for e in E if v in e) for v in range(n)]
def rand_gate(i):
    j,k=random.sample(range(i),2); return [random.choice('&|'),min(j,k),max(j,k)]
if len(sys.argv)>6:
    init=[]
    for t in sys.argv[6].split():
        m=re.match(r'(\d+)=(\d+)([&|])(\d+)$',t); init.append((int(m[1]),m[3],int(m[2]),int(m[4])))
    pad=S-len(init); C=[rand_gate(n+i) for i in range(pad)]; mp={}
    for idx,(i,o,j,k) in enumerate(init):
        jj=mp.get(j,j); kk=mp.get(k,k); mp[i]=n+pad+idx; C.append([o,min(jj,kk),max(jj,kk)])
else: C=[rand_gate(n+i) for i in range(S)]
def nor_reduced(C,dead=-1):
    V=[0 if v==dead else X[v] for v in range(n)]
    for o,j,k in C: V.append(V[j]&V[k] if o=='&' else V[j]|V[k])
    canon=list(range(n)); first={}
    for v in range(n):
        if V[v]: first.setdefault(V[v],v)
    real={}
    for idx,(o,j,k) in enumerate(C):
        i=n+idx; t=V[i]
        if t==0: canon.append(None); continue
        if t in first: canon.append(first[t]); continue
        first[t]=i; canon.append(i); real[i]=(o,canon[j],canon[k])
    out=canon[n+S-1]; seen=set(); st=[out] if out is not None else []
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st+=[real[x][1],real[x][2]]
    return V, sum(1 for x in seen if real[x][0]=='|'), len(seen)
def evaluate(C):
    V,no,sz=nor_reduced(C)
    err=bin(V[-1]^TGT).count('1')
    if err: return err,sz,99
    ex=0
    for v in range(n):
        _,nv,_=nor_reduced(C,v); ex+=max(0,(no-nv)-deg[v]+1)
    return 0,sz,ex
def cost(e): return 0.02*e[0]+e[2]*1.0+0.001*e[1] if e[0] else e[2]+0.001*e[1]
cur=evaluate(C); cc=cost(cur)+ (5 if cur[0] else 0); best=None
for it in range(IT):
    Tt=T0*(1-it/IT)+0.01
    i=random.randrange(S); old=C[i]
    if random.random()<0.2: new=[('&' if old[0]=='|' else '|'),old[1],old[2]]
    else:
        new=list(old); new[random.choice([1,2])]=random.randrange(n+i)
        if new[1]==new[2]: continue
        new=[new[0],min(new[1],new[2]),max(new[1],new[2])]
    C[i]=new; ev=evaluate(C); c2=cost(ev)+(5 if ev[0] else 0)
    if c2<=cc or random.random()<math.exp((cc-c2)/Tt):
        cur,cc=ev,c2
        if ev[0]==0 and (best is None or ev[2]<best[0]):
            best=(ev[2],ev[1]); print('BEST ex',ev[2],'size',ev[1],' '.join('%d=%d%s%d'%(n+t,g[1],g[0],g[2]) for t,g in enumerate(C)),flush=True)
            if ev[2]==0: break
    else: C[i]=old
print('final',best)
