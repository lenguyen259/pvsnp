import itertools, sys, random, json
sys.argv=[sys.argv[0],sys.argv[1],sys.argv[2],'1']+sys.argv[3:]
N=int(sys.argv[4]); seed=int(sys.argv[5])
src=open('meas.py').read().split("def downsets")[0]
exec(src)
random.seed(seed)
fails=0
V=list(range(n))
for it in range(N):
    X=frozenset(e for e in E if random.random()<0.7) or frozenset([random.choice(E)])
    Ys=frozenset(u for u in V if random.random()<0.85)
    cand=[p for p in NE if p[0] in Ys and p[1] in Ys]
    pk=random.choice([1.0,0.9,0.7,0.5])
    Yn=frozenset(p for p in cand if random.random()<pk)
    m=mu(X,Ys,Yn)
    for t in range(20):
        a=random.random()
        lab={u:random.choice([1,2,3,3] if a<0.5 else [1,2,3]) for u in Ys}
        Ys1=frozenset(u for u in Ys if lab[u]&1); Ys2=frozenset(u for u in Ys if lab[u]&2)
        Yn1=set();Yn2=set();ok=True
        for p in Yn:
            o=[]
            if p[0] in Ys1 and p[1] in Ys1: o.append(1)
            if p[0] in Ys2 and p[1] in Ys2: o.append(2)
            if not o: ok=False;break
            c=random.choice(o+([3] if len(o)==2 else []))
            if c&1: Yn1.add(p)
            if c&2: Yn2.add(p)
        if not ok: continue
        Yn1=frozenset(Yn1);Yn2=frozenset(Yn2)
        m1=mu(X,Ys1,Yn1); m2=mu(X,Ys2,Yn2)
        if m>m1+m2:
            fails+=1
            if fails<=5: print('AND FAIL',sorted(X),sorted(Ys),sorted(Yn),'|',sorted(Ys1),sorted(Yn1),'|',sorted(Ys2),sorted(Yn2),m,m1,m2,flush=True)
print('fails',fails,'root',mu(frozenset(E),frozenset(range(n)),frozenset(NE)))
