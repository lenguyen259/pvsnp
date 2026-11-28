"""Exchange test: for each non-STAR-ALL circuit of size Phi, look for a single-gate edit
giving a correct circuit of size <= Phi with fewer violating AND gates."""
import sys,collections,time,pickle
from t2lib import *
def nviol(g,c): return len({i for i,t in starall_viol(g,c)})
def edits(g,c):
    n=g.n
    for t,(i,o,j,k) in enumerate(c):
        nodes=list(range(n))+[x[0] for x in c[:t]]
        for o2 in '&|':
            for a in range(len(nodes)):
                for b in range(a+1,len(nodes)):
                    j2,k2=nodes[a],nodes[b]
                    if (o2,j2,k2)==(o,min(j,k),max(j,k)) : continue
                    c2=list(c); c2[t]=(i,o2,j2,k2); yield c2
def best_edit(g,c,v0):
    best=None
    for c2 in edits(g,c):
        if not ok(g,c2): continue
        r=renum(g.n,red(g,c2))
        if len(r)>len(c): continue
        v=nviol(g,r)
        if v<v0 and (best is None or v<best[0]): best=(v,r)
        if best and best[0]==0: return best
    return best
if __name__=='__main__':
    maxper=int(sys.argv[1]) if len(sys.argv)>1 else 10**9
    st=collections.Counter(); per=collections.Counter(); bad=[]; seen=set(); t0=time.time()
    for fn,n,E,c in load_cached():
        g=Graph(E,n)
        if g.t==1: continue
        c=renum(n,red(g,c))
        if len(c)!=g.P: continue
        k=(g.E,tuple(c))
        if k in seen: continue
        seen.add(k)
        v0=nviol(g,c)
        if v0==0: st['starall']+=1; continue
        if per[g.E]>=maxper: continue
        per[g.E]+=1
        st['nonSA']+=1
        b=best_edit(g,c,v0)
        if b is None: st['stuck']+=1; bad.append((g.E,fmt(c),v0))
        else: st['improved']+=1; st['to0' if b[0]==0 else 'partial']+=1
    print(dict(st),time.time()-t0)
    print('graphs',dict(per))
    for x in bad[:20]: print('STUCK',x)
    pickle.dump(bad,open('exch_bad.pkl','wb'))
