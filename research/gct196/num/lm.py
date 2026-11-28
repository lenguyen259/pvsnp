import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num')
from lev import *
from torch.func import jacrev
def search(p,q,n,seed,iters=300,S=None,verbose=False,init=None):
    g=torch.Generator().manual_seed(seed)
    S=S or int(1.5*(np.math.comb(n+3,4)))+50 if hasattr(np,'math') else None
    import math
    S=S or int(1.3*math.comb(n+3,4))+50
    C=torch.complex(torch.randn(S,n,generator=g),torch.randn(S,n,generator=g))
    C=C/C.abs().pow(2).sum(1,keepdim=True).sqrt()
    m=p*q
    if init is None:
        B=torch.complex(torch.randn(n,m,generator=g),torch.randn(n,m,generator=g))
    else: B=torch.as_tensor(init,dtype=CD)
    def orth(B):
        Q,_=torch.linalg.qr(B.T.conj()); return Q.T.conj()
    B=orth(B)
    def F(v):
        Bc=torch.complex(v[:n*m],v[n*m:]).reshape(n,m)
        r=residual(Bc,C,p,q)
        return torch.cat([r.real.ravel(),r.imag.ravel()])
    v=torch.cat([B.real.ravel(),B.imag.ravel()])
    mu=1e-2
    r=F(v); cost=r.dot(r).item()
    for it in range(iters):
        J=jacrev(F)(v)
        A=J.T@J; gr=J.T@r
        while True:
            d=torch.linalg.solve(A+mu*torch.eye(A.shape[0]),-gr)
            v2=v+d
            Bc=orth(torch.complex(v2[:n*m],v2[n*m:]).reshape(n,m))
            v2=torch.cat([Bc.real.ravel(),Bc.imag.ravel()])
            r2=F(v2); c2=r2.dot(r2).item()
            if c2<cost: v,r,cost=v2,r2,c2; mu=max(mu/3,1e-12); break
            mu*=4
            if mu>1e8: break
        if verbose and it%10==0: print(it,cost,mu,flush=True)
        if cost<1e-26 or mu>1e8: break
    Bc=torch.complex(v[:n*m],v[n*m:]).reshape(n,m)
    return cost,Bc.numpy()
if __name__=='__main__':
    p,q,n,seeds=map(int,sys.argv[1:5])
    for s in range(seeds):
        t=time.time()
        cost,B=search(p,q,n,s)
        print(p,q,n,'seed',s,'cost',cost,'check',is_level(B,p,q,seed=99),'time',round(time.time()-t,1),flush=True)
        if cost<1e-20: np.save(f'/home/user/pvsnp/research/gct196/num/sol_{p}x{q}_{n}_{s}.npy',B)
