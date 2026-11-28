import sys, os
os.environ['OMP_NUM_THREADS']='1'
sys.path.insert(0,'/home/user/pvsnp/research/gct196/num')
import numpy as np, torch
torch.set_num_threads(1)
from lev import Ms
from ext import known
p,q=4,7
def grads(X):
    # X (S,p,q) numpy complex -> (S,p, p*q) gradients of e_1..e_p
    S=X.shape[0]
    Xt=torch.as_tensor(X)
    A=Xt.unsqueeze(1).repeat(1,p*q,1,1).clone(); B=A.clone()
    for k in range(p*q):
        r,j=divmod(k,q); A[:,k,r,j]=1; B[:,k,r,j]=0
    MA=Ms(A.reshape(-1,p,q),p).reshape(S,p*q,p); MB=Ms(B.reshape(-1,p,q),p).reshape(S,p*q,p)
    return (MA-MB).permute(0,2,1).numpy()
def rank(M,tol=1e-8):
    if len(M)==0: return 0
    s=np.linalg.svd(M,compute_uv=False); return int((s>tol*s[0]).sum())
def invariants(Bs,rng):
    n=rank(Bs); 
    S=60+3*n*n
    C=rng.normal(size=(S,Bs.shape[0]))+1j*rng.normal(size=(S,Bs.shape[0]))
    X=(C@Bs).reshape(S,p,q)
    G=grads(X)
    J=np.ones((1,p*q))
    g2=G[:,1,:]; g3=G[:,2,:]; g4=G[:,3,:]
    d1=rank(np.vstack([J,g2])); d2=rank(np.vstack([J,g2,g3])); d3=rank(np.vstack([J,g2,g3,g4]))
    # orth check
    orth=max(abs(G[:,k,:]@Bs.T).max() for k in range(p))
    M=Bs.reshape(-1,p,q); R=M.sum(2); Cc=M.sum(1)
    lr=rank(R); lc=rank(Cc); lam=rank(np.hstack([R,Cc])); D=n-lam
    return dict(n=n,lR=lr,lC=lc,lam=lam,D=D,G2=d1,G23=d2,Gam=d3,orth=orth)
if __name__=='__main__':
    pass
