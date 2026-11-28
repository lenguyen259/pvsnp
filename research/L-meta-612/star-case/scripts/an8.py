from cl import *
import itertools
def tts(n,c):
    T={}
    for u in range(n): T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
res=collections.defaultdict(collections.Counter)
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]; Es={frozenset(e) for e in E}
    import networkx as nx
    tri=any(len(nbrs(E,u)&nbrs(E,v))>0 for u,v in E)
    for c in D['circs']:
        c=[tuple(x) for x in c]; T=tts(n,c); G,rd,need,dead=info(n,E,c)
        ev=lambda t,S: (t>>sum(1<<u for u in S))&1
        clean=all(not(ev(T[i],[u,v]) and not ev(T[i],[u]) and not ev(T[i],[v])) for i,_,_,_ in c for u,v in itertools.combinations(range(n),2) if frozenset((u,v)) not in Es)
        cats=collections.Counter(S['cat'] for S in stars(n,E,c,G,rd))
        r=res[(fn,'tri' if tri else 'notri')]; r['n']+=1; r['clean']+=clean; r['S2']+=bool(cats['S2']); r['S2clean']+=bool(cats['S2']) and clean
for k,v in sorted(res.items()): print(k,dict(v))
