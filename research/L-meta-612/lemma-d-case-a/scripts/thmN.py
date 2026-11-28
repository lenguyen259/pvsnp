# Theorem N construction: hub edge ab; z_v = x_v | x_a x_b for v in V2; then any circuit for f_G on (x_H, z)
import sys
sys.path.insert(0,'.')
from star import analyze
import graphs
def build(n,E,a,b):
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    c=[]; nxt=[n]
    def g(op,j,k):
        i=nxt[0]; nxt[0]+=1; c.append((i,op,j,k)); return i
    e=g('&',a,b); node={v:(g('|',v,e) if deg[v]==2 else v) for v in range(n)}
    rest=list(E); terms=[]
    while rest:
        cnt={}
        for p,q in rest: cnt[p]=cnt.get(p,0)+1; cnt[q]=cnt.get(q,0)+1
        h=max(cnt,key=cnt.get); L=[q if p==h else p for p,q in rest if h in (p,q)]
        cur=node[L[0]]
        for x in L[1:]: cur=g('|',cur,node[x])
        terms.append(g('&',node[h],cur)); rest=[x for x in rest if h not in x]
    cur=terms[0]
    for t in terms[1:]: cur=g('|',cur,t)
    return c
for n,E in list(graphs.casea(7)):
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    he=[(p,q) for p,q in E if deg[p]>=3 and deg[q]>=3]
    if not he: print(E,'no hub edge'); continue
    c=build(n,E,*he[0]); ch,nor,s,s0=analyze(n,c,E)
    print(E,'hubedge',he[0],'size',s,'#OR',nor,'V2 ch',[ch[v] for v in range(n) if deg[v]==2],'good',[v for v in range(n) if ch[v]>=deg[v]])
