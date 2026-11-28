# Construction N2: H independent; two V2 vertices p,q with N(p),N(q) in H. B = s_p | s_q, z_v = x_v | B (v in V2 - {p,q}), z_p=z_q=B,
# then a star-cover circuit for f_G on (x_H, z).
import sys, itertools, networkx as nx
from star import analyze
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from run1h import has_c4
def build(n,E,p,q):
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    N={v:[b for a,b in E if a==v]+[a for a,b in E if b==v] for v in range(n)}
    c=[]; nxt=[n]
    def g(op,j,k):
        i=nxt[0]; nxt[0]+=1; c.append((i,op,j,k)); return i
    s=lambda v: g('&',v,g('|',N[v][0],N[v][1]))
    B=g('|',s(p),s(q))
    node={v:(B if v in (p,q) else g('|',v,B)) if deg[v]==2 else v for v in range(n)}
    rest=list(E); terms=[]
    while rest:
        cnt={}
        for a,b in rest: cnt[a]=cnt.get(a,0)+1; cnt[b]=cnt.get(b,0)+1
        h=max(cnt,key=lambda x:(cnt[x],deg[x]>=3)); L=[b if a==h else a for a,b in rest if h in (a,b)]
        L=sorted(set(node[x] for x in L)); cur=L[0]
        for x in L[1:]: cur=g('|',cur,x)
        terms.append(g('&',node[h],cur) if node[h]!=cur else cur); rest=[x for x in rest if h not in x]
    terms=sorted(set(terms)); cur=terms[0]
    for t in terms[1:]: cur=g('|',cur,t)
    return c
if __name__=="__main__":
  E=[(0,3),(1,3),(1,4),(2,4),(0,5),(2,5),(0,6),(6,7),(1,7),(2,8),(8,9),(0,9)]
  n=10; G=nx.Graph(E); print('C4-free',not has_c4(G),'deg',dict(G.degree()))
  c=build(n,E,3,4); ch,nor,s,s0=analyze(n,c,E)
  deg=dict(G.degree())
  print("size",s,'#OR',nor,'ch',ch,'V2 good',[v for v in range(n) if deg[v]==2 and ch[v]>=2],'good',[v for v in range(n) if ch[v]>=deg[v]])
