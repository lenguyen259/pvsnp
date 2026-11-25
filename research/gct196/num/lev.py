import torch, numpy as np, itertools, sys, time
torch.set_default_dtype(torch.float64)
CD=torch.complex128
def kappas(X,p):
    # X: (S,p,q) complex -> coef (S,2^p): coef[U]=sum over injections rows U -> distinct cols of prod
    S,_,q=X.shape
    c=torch.zeros(S,1<<p,dtype=CD); c[:,0]=1
    for j in range(q):
        new=c.clone()
        for r in range(p):
            bit=1<<r
            idx=[U for U in range(1<<p) if U&bit]
            src=[U^bit for U in idx]
            new[:,idx]=new[:,idx]+X[:,r,j].unsqueeze(1)*c[:,src]
        c=new
    return c
def Ms(X,p):
    c=kappas(X,p)
    out=[]
    for k in range(1,p+1):
        idx=[U for U in range(1<<p) if bin(U).count('1')==k]
        out.append(c[:,idx].sum(1))
    return torch.stack(out,1)  # (S,p)
def residual(B,C,p,q):
    X=(C@B).reshape(C.shape[0],p,q)
    return Ms(X,p)
def is_level(B,p,q,S=None,seed=0):
    B=torch.as_tensor(B,dtype=CD); n=B.shape[0]
    g=torch.Generator().manual_seed(seed)
    S=S or 3*n**4//24+200
    C=torch.complex(torch.randn(S,n,generator=g),torch.randn(S,n,generator=g))
    C=C/C.abs().pow(2).sum(1,keepdim=True).sqrt()
    Bn=B/ B.abs().pow(2).sum(1,keepdim=True).sqrt()
    return residual(Bn,C,p,q).abs().max().item()
