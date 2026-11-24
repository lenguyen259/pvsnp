# star circuit: every V2 vertex with both nbrs in H gets s_v = x_v & (x_u|x_w); G[H] edges by a simple per-vertex star cover
import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb')
from tr import breduce
def analyze(n,c,E):
    R,T,o=breduce(n,c)
    full=sum(1<<r for r in range(1<<n) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
    assert T[o]==full, 'wrong function'
    xv={v:sum(1<<r for r in range(1<<n) if (r>>v)&1) for v in range(n)}
    core=lambda q: {v for v in range(n) if T[q]&~xv[v]==0}
    ch={v:0 for v in range(n)}
    for i,(op,j,k) in R.items():
        if op=='|':
            for v in core(j)|core(k): ch[v]+=1
    nor=sum(1 for g in R.values() if g[0]=='|')
    return ch, nor, len(R), len(c)
def build(n,E):
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    N={v:[b for a,b in E if a==v]+[a for a,b in E if b==v] for v in range(n)}
    c=[]; nxt=[n]
    def g(op,j,k):
        i=nxt[0]; nxt[0]+=1; c.append((i,op,j,k)); return i
    def OR(L):
        cur=L[0]
        for x in L[1:]: cur=g('|',cur,x)
        return cur
    terms=[]; covered=set()
    for v in range(n):
        if deg[v]==2 and all(deg[u]>=3 for u in N[v]):
            terms.append(g('&',v,OR(N[v]))); covered|={frozenset((v,u)) for u in N[v]}
    rest=[e for e in E if frozenset(e) not in covered]
    while rest:
        # greedy star cover
        cnt={}
        for a,b in rest: cnt[a]=cnt.get(a,0)+1; cnt[b]=cnt.get(b,0)+1
        h=max(cnt,key=cnt.get); L=[b if a==h else a for a,b in rest if h in (a,b)]
        terms.append(g('&',h,OR(L))); rest=[e for e in rest if h not in e]
    OR(terms); return c
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])]; n=max(max(e) for e in E)+1
    c=build(n,E); ch,nor,s,s0=analyze(n,c,E)
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    print('E',len(E),'#OR',nor,'size',s,'circ',' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c))
    print('deg',deg); print('ch ',ch); print('good',[v for v in range(n) if ch[v]>=deg[v]], 'V2 good',[v for v in range(n) if deg[v]==2 and ch[v]>=2])
