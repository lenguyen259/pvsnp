import itertools, subprocess, sys, networkx as nx
def tau(n,E):
    for k in range(n+1):
        for T in itertools.combinations(range(n),k):
            if all(a in T or b in T for a,b in E): return k
def vecs(n,E,mode):
    if mode=='full':
        pts=[r for r in range(1,1<<n)]
    else:
        w=3 if mode=='slice3' else 2
        pts=[sum(1<<i for i in c) for k in range(1,w+1) for c in itertools.combinations(range(n),k)]
    gens=[sum(1<<k for k,r in enumerate(pts) if (r>>i)&1) for i in range(n)]
    Es=set(tuple(sorted(e)) for e in E)
    def f(r): return any((r>>a)&1 and (r>>b)&1 for a,b in Es)
    T=sum(1<<k for k,r in enumerate(pts) if f(r))
    return gens,T
def run(n,E,mode,K,maxs=60000000,timeout=3000):
    g,T=vecs(n,E,mode)
    args=['./fdp',str(K),str(maxs),str(n)]+['%x'%x for x in g]+['%x'%T]
    try:
        out=subprocess.run(args,capture_output=True,text=True,timeout=timeout).stdout
    except subprocess.TimeoutExpired: return None,'TIMEOUT'
    for l in out.splitlines():
        if l.startswith('MIN'):
            return int(l.split()[1]), out.splitlines()[-1]
    return None, out.splitlines()[-1]
if __name__=='__main__':
    n=int(sys.argv[1]); E=eval(sys.argv[2]); mode=sys.argv[3]
    t=tau(n,E); print('E',len(E),'tau',t,'target leaves',len(E)+t)
    print(run(n,E,mode,len(E)+t))
