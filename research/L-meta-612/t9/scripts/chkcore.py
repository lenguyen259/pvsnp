"""DATA check of Lemma AND-core: in a reduced monotone circuit for f_G, G C4-free with min degree >= 2 on its
support, some non-isolated v has an AND reader or >= 2 exits (AND gates outside Q_v with an input in Q_v).
Circuits: cached pseudoforest circuits with every leaf (repeatedly) set to 0, then reduced."""
import sys,json,collections
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t9/scripts')
from chkX1 import parse,tabs
def reduce(n,c,sub):
    T,full=tabs(n,c,sub); first={}; real={}; canon={}
    for u in range(n):
        canon[u]='K' if T[u] in (0,full) else first.setdefault(T[u],u)
    for i,o,j,k in c:
        if T[i] in (0,full): canon[i]='K'; continue
        if T[i] in first: canon[i]=first[T[i]]; continue
        first[T[i]]=i; canon[i]=i; real[i]=(o,canon[j],canon[k])
    out=canon[c[-1][0]]; seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(y for y in real[x][1:] if y!='K')
    return [(i,)+real[i] for i in sorted(seen)]
st=collections.Counter(); bad=[]
for fn in sys.argv[1:-1]:
  for li,line in enumerate(open(fn)):
    if li>=int(sys.argv[-1]): break
    d=json.loads(line); E=[tuple(e) for e in d['E']]; c=parse(d['c']); n=min(i for i,_,_,_ in c)
    Ed=set(E); zero=set()
    while True:
        deg=collections.Counter(x for e in Ed for x in e); lv=[v for v in deg if deg[v]==1]
        if not lv: break
        zero.add(lv[0]); Ed={e for e in Ed if lv[0] not in e}
    if not Ed: continue
    c2=reduce(n,c,{v:0 for v in zero})
    if any('K' in g[2:] for g in c2): st['constinput']+=1; continue
    V=sorted({x for e in Ed for x in e}); ok=False
    for v in V:
        if any(o=='&' and v in (j,k) for i,o,j,k in c2): ok=True; break
        Q=set()
        for i,o,j,k in c2:
            ins=[x==v or x in Q for x in (j,k)]
            if (o=='|' and any(ins)) or (o=='&' and all(ins)): Q.add(i)
        ex=[i for i,o,j,k in c2 if o=='&' and i not in Q and (j in Q or k in Q)]
        if len(ex)>=2: ok=True; break
    st['tested']+=1; st['ok']+=ok
    if not ok: bad.append(line[:300])
    noand=all(not(o=='&' and (j<n or k<n)) for i,o,j,k in c2)
    st['no_AND_reader_at_all']+=noand
print(dict(st),'fail',len(bad)); [print(b) for b in bad[:3]]
