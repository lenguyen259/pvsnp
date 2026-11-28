import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
exec(open('run2.py').read().split('for name,Bs in srcs.items():')[0])
def nullspace(A,tol=1e-9):
    u,s,vh=np.linalg.svd(A); r=(s>tol*max(1,s[0])).sum(); return vh[r:].conj().T
def lam(X): # X (k,28) -> (k,11)
    M=X.reshape(-1,p,q); return np.hstack([M.sum(2),M.sum(1)])
def analyze(Bs):
    n=rank(Bs); Lm=lam(Bs)
    N=nullspace(Lm.T)   # coefficients c with c@Lm=0 -> D = c@Bs
    Dm=(N.T@Bs) if N.shape[1] else np.zeros((0,28))
    d=Dm.shape[0]; K=rank(Lm)
    if d==0: return dict(n=n,D=0,lam=K)
    prods=np.array([Dm[i]*Dm[j] for i in range(d) for j in range(i,d)])
    perpDD=abs(prods@Bs.T).max()
    lDD=rank(lam(prods))
    trip=np.array([Dm[i]*Dm[j]*Dm[k] for i in range(d) for j in range(i,d) for k in range(j,d)])
    lDDD=rank(np.vstack([lam(prods),lam(trip)]))
    # functionals in K^perp from D∘D: check orthogonality to lam(L)
    orthK=abs(lam(prods)@Lm.T).max()
    return dict(n=n,D=d,lam=K,slack=9-K-d,DDperpL='%.1e'%perpDD,lamDD=lDD,lamDD_orthK='%.1e'%orthK,lamDD_DDD=lDDD)
for name,Bs in list(srcs.items())[:6]:
    print(name,analyze(Bs))
