import sys; sys.path.insert(0,'.')
from lm2 import *
def T1(B,p,q,seed=0):
    n=B.shape[0]; rng=np.random.default_rng(seed); st=setup(p)
    S=int(1.5*math.comb(n+p-2,p-1))+80
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n))
    X=(C@B).reshape(S,p,q)
    # gradient rows: use res_jac with n=1 basis trick: B1 = X_s itself
    rows=[]
    for s in range(S):
        r,J=res_jac(X[s].reshape(1,-1),np.ones((1,1)),p,q,st)
        rows.append(J)
    A=np.vstack(rows)
    sv=np.linalg.svd(A,compute_uv=False)
    return (sv<1e-8*sv[0]).sum()+max(0,p*q-len(sv))
def T1basis(B,p,q,seed=0):
    n=B.shape[0]; rng=np.random.default_rng(seed); st=setup(p)
    S=int(1.5*math.comb(n+p-2,p-1))+80
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n))
    X=(C@B).reshape(S,p,q)
    A=np.vstack([res_jac(X[s].reshape(1,-1),np.ones((1,1)),p,q,st)[1] for s in range(S)])
    u,sv,vh=np.linalg.svd(A)
    k=(sv<1e-8*sv[0]).sum()+max(0,p*q-len(sv))
    return vh[-k:].conj()
def known(p,q):
    w=np.exp(2j*np.pi/3)
    def E(r,j): M=np.zeros((p,q),complex); M[r,j]=1; return M
    B=[];a=np.zeros((p,q),complex); al=[1,w,w*w]; be=[1,w*w,w]
    for k in range(3): a[k+1,0]=al[k]; a[k+1,1]=-al[k]
    B.append(a.ravel()); b=np.zeros((p,q),complex)
    for k in range(3): b[k+1,2]=be[k]; b[k+1,3]=-be[k]
    B.append(b.ravel())
    for j in range(1,q): B.append((E(0,0)-E(0,j)).ravel())
    F=np.array(B)
    H=np.array([(E(0,0)-E(0,j)).ravel() for j in range(1,q)]+[(E(1,0)-E(r,0)).ravel() for r in (2,3)])
    return F,H
