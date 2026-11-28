import sys,pickle,time,collections
from t2lib import *
G={}; stats=collections.Counter(); fails=collections.defaultdict(list); seen=set()
t0=time.time(); out=[]
for fn,n,E,c in load_cached():
    key=(tuple(sorted(E)),)
    if key not in G: G[key]=(Graph(E,n),)
    g=G[key][0]
    if g.t==1: continue  # stars
    c=renum(n,red(g,c)); k2=(g.E,tuple(c))
    if k2 in seen: continue
    seen.add(k2)
    r=evaluate(g,c)
    good=collections.defaultdict(set)
    for a,v,e,nd,ok_ in r:
        if ok_: good[a].add(v)
    st=len(c)-g.P
    stats['circ']+=1
    deg={v:len(g.N[v]) for v in g.sup}
    T2=bool(good['A']|good['N']); T2F=T2 or bool(good['B'])
    for nm,val in [('T2',T2),('T2F',T2F),('AorB',bool(good['A']|good['B'])),('Aonly',bool(good['A'])),('Nonly',bool(good['N'])),('Bonly',bool(good['B'])),
                   ('every_v_any',all(v in good['A']|good['N']|good['B'] for v in g.sup)),
                   ('every_leaf_AN',all(v in good['A']|good['N'] for v in g.sup if deg[v]==1)),
                   ('every_leaf_ANB',all(v in good['A']|good['N']|good['B'] for v in g.sup if deg[v]==1)),
                   ('every_leaf_A_or_Nb_or_Bnb',all(v in good['A']|good['N'] or (list(g.N[v])[0] in good['B']) for v in g.sup if deg[v]==1)),
                   ('every_deg2_any',all(v in good['A']|good['N']|good['B'] for v in g.sup if deg[v]==2)),
                   ('minAND_supp_AN', any(support(g,c,i)&(good['A']|good['N']) for i in minimal_ands(c))),
                   ('everyminAND_supp_ANB', all(support(g,c,i)&(good['A']|good['N']|good['B']) for i in minimal_ands(c))),
                   ]:
        if val: stats[nm]+=1
        else:
            stats['F_'+nm]+=1
            if len(fails[nm])<5 or st<min(x[0] for x in fails[nm]): fails[nm].append((st,g.E,fmt(c)))
    if stats['circ']%5000==0: print(stats['circ'],time.time()-t0,flush=True)
print(dict(stats))
for k in fails:
    best=min(fails[k]); print(k,best)
pickle.dump((stats,dict(fails)),open('scan.pkl','wb'))
