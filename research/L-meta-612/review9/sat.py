# SAT: exists monotone fan-in-2 circuit for f_G with s gates, #AND <= amax ?
import sys, itertools, json
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
def fG(n,E,x): return int(any(x[u] and x[v] for u,v in E))
def build(n,E,s,amax):
    P=IDPool(); cl=[]
    adj={i:set() for i in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    rows=[]
    for u,v in E: rows.append(tuple(int(i in (u,v)) for i in range(n)))
    for r in itertools.product([0,1],repeat=n):
        I=[i for i in range(n) if r[i]]
        if fG(n,E,r): continue
        if all(fG(n,E,tuple(1 if i==j else r[i] for i in range(n))) for j in range(n) if not r[j]): rows.append(r)
    N=n+s
    val=lambda i,r: P.id(('v',i,r))
    isand=lambda g: P.id(('a',g))
    sel=lambda g,j,k: P.id(('s',g,j,k))  # inputs j<=k
    for g in range(n,N):
        S=[sel(g,j,k) for j in range(g) for k in range(j+1,g)]
        cl.append(S)
        cl+= CardEnc.atmost(S,1,vpool=P,encoding=EncType.seqcounter).clauses
    for ri,r in enumerate(rows):
        for i in range(n):
            cl.append([val(i,ri)] if r[i] else [-val(i,ri)])
        for g in range(n,N):
            o=val(g,ri); a=isand(g)
            for j in range(g):
                for k in range(j+1,g):
                    t=sel(g,j,k); vj=val(j,ri); vk=val(k,ri)
                    # AND
                    cl.append([-t,-a,-o,vj]); cl.append([-t,-a,-o,vk]); cl.append([-t,-a,o,-vj,-vk])
                    # OR
                    cl.append([-t,a,o,-vj]); cl.append([-t,a,o,-vk]); cl.append([-t,a,-o,vj,vk])
        cl.append([val(N-1,ri)] if fG(n,E,r) else [-val(N-1,ri)])
    for g in range(n,N-1):
        cl.append([sel(h,j,k) for h in range(g+1,N) for j in range(h) for k in range(j+1,h) if g in (j,k)])
    cl+=CardEnc.atmost([isand(g) for g in range(n,N)],amax,vpool=P,encoding=EncType.seqcounter).clauses
    return P,cl,rows
def solve(n,E,s,amax,limit=1):
    P,cl,rows=build(n,E,s,amax)
    sols=[]
    with Cadical153(bootstrap_with=cl) as S:
        while len(sols)<limit and S.solve():
            m=set(l for l in S.get_model() if l>0)
            C=[]
            for g in range(n,n+s):
                for j in range(g):
                    for k in range(j+1,g):
                        if P.id(('s',g,j,k)) in m: C.append(('AND' if P.id(('a',g)) in m else 'OR',j,k))
            sols.append(C)
            S.add_clause([-P.id(('s',g,j,k)) for g,(t,j,k) in zip(range(n,n+s),C)]+[(-1 if t=='AND' else 1)*P.id(('a',g)) for g,(t,j,k) in zip(range(n,n+s),C)])
    return sols
if __name__=='__main__':
    n=int(sys.argv[1]); E=json.loads(sys.argv[2]); s=int(sys.argv[3]); amax=int(sys.argv[4])
    r=solve(n,E,s,amax)
    print('SAT' if r else 'UNSAT', r)
