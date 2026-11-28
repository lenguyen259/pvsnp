# enumerate placements of k rectangle-killer gadgets on Petersen, complete with stars, verify exactly
import itertools, sys
from common import *
from indep import check
n=10; E=[tuple(sorted(e)) for e in PET]; Es=set(E)
N={v:{b for a,b in E if a==v}|{a for a,b in E if b==v} for v in range(n)}
cn=lambda u,v: (N[u]&N[v]).pop()
adj=lambda u,v: tuple(sorted((u,v))) in Es
# gadget: edges (a,b),(c,d), no edges between {a,b} and {c,d}; cross centers: (a,c),(b,c),(a,d) as star pair-ORs; (b,d) killer star
gads=[]
for e1,e2 in itertools.combinations(E,2):
    if set(e1)&set(e2): continue
    if any(adj(u,v) for u in e1 for v in e2): continue
    for (a,b) in (e1,e1[::-1]):
        for (c,d) in (e2,e2[::-1]):
            gads.append((a,b,c,d))
def build(gs):
    b=B(n); g=b.g
    pairOR={}   # (center) -> (u,v) required pair
    killers={}
    cover=set()
    for (a,bb,c,d) in gs:
        for (u,v) in ((a,c),(bb,c),(a,d)):
            h=cn(u,v)
            if h in pairOR and set(pairOR[h])!={u,v}: return None
            pairOR[h]=(u,v)
        h=cn(bb,d)
        if h in pairOR or h in killers: return None
        killers[h]=(bb,d)
        cover|={tuple(sorted((a,bb))),tuple(sorted((c,d))),tuple(sorted((h,bb))),tuple(sorted((h,d)))}
    if set(killers)&set(pairOR): return None
    ORn={}
    def por(u,v):
        k=frozenset((u,v))
        if k not in ORn: ORn[k]=g('|',u,v)
        return ORn[k]
    terms=[]
    # pair ORs first
    for h,(u,v) in pairOR.items(): por(u,v)
    for h,(u,v) in killers.items(): por(u,v)
    for (a,bb,c,d) in gs:
        t=g('&',por(a,c),por(bb,c)); t=g('&',por(a,d),t)
        h=cn(bb,d); terms.append(g('&',por(bb,d),g('|',h,t)))
    # stars at pairOR centers
    for h,(u,v) in pairOR.items():
        L=[w for w in N[h] if tuple(sorted((h,w))) not in cover and w not in (u,v)]
        cur=por(u,v)
        for w in L: cur=g('|',cur,w)
        terms.append(g('&',h,cur)); cover|={tuple(sorted((h,w))) for w in N[h]}
    rest=[e for e in E if e not in cover]
    while rest:
        cnt={}
        for p,q in rest: cnt[p]=cnt.get(p,0)+1; cnt[q]=cnt.get(q,0)+1
        h=max(cnt,key=cnt.get); L=[q if p==h else p for p,q in rest if h in (p,q)]
        terms.append(g('&',h,b.OR(L)) if True else None); rest=[e for e in rest if h not in e]
    b.OR(terms); return b.c
k=int(sys.argv[1]); best=None
for gs in itertools.combinations(gads,k):
    c=build(gs)
    if c is None: continue
    r=analyze(n,c,PET)
    if not r['ok']: continue
    key=(r['nor'],r['size'])
    if best is None or key<best[0]: best=(key,gs,fmt(r['R'])); print(key,gs,flush=True)
print(best); 
if best: print(check(n,PET,best[2]))
