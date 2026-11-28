import sys
exec(open('run4.py').read().split('maxn=int')[0])
def minimal_ands(n,circ):
    sets={i:frozenset([i]) for i in range(n)}; isor={i:True for i in range(n)}
    res=[]
    for (i,o,j,k) in circ:
        if o=='|' and isor[j] and isor[k]: sets[i]=sets[j]|sets[k]; isor[i]=True
        else:
            isor[i]=False
            if o=='&' and isor[j] and isor[k]: res.append((sets[j],sets[k]))
    return res
maxn=int(sys.argv[1]); lim=int(sys.argv[2]); X=int(sys.argv[3])
for G in nx.graph_atlas_g():
    n=G.number_of_nodes()
    if n<2 or n>maxn or G.number_of_edges()==0 or any(d==0 for _,d in G.degree()) or has_c4(G): continue
    E=list(G.edges()); P=phiG(E)
    circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
    stats=collections.Counter()
    for c in circs:
        good={(v,b) for v in range(n) for b in (0,1) if restrict(n,c,v,b)-X<=(phi0(E,v) if b==0 else phi1(E,v))}
        mins=minimal_ands(n,c)
        anyA=any(v in A|B for (v,b) in good for (A,B) in mins)
        everyA=all(any(v in A|B for (v,b) in good) for (A,B) in mins)
        # stronger: v from the smaller side of every minimal AND
        small=all(any(v in (A if len(A)<=len(B) else B) for (v,b) in good) for (A,B) in mins)
        allsmall=all(all(any((v,b) in good for b in (0,1)) for v in (A if len(A)<=len(B) else B)) for (A,B) in mins)
        stats['every_v_of_every_smallside']+=allsmall
        if not small: print('   FAIL small', c, mins, sorted(good))
        stats['any_minAND']+=anyA; stats['every_minAND']+=everyA; stats['every_minAND_smallside']+=small
    print(n,len(E),'#circ',len(circs),dict(stats),E,flush=True)
