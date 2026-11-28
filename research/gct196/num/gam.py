import sys; sys.path.insert(0,'.')
exec(open('ext.py').read())
def grads(X,p,q,st):
    # X: (S,p,q) -> G: (S,p, p*q) gradient of M_k at each X
    S=X.shape[0]
    _,J=res_jac(X.reshape(S,-1)[:,None,:].reshape(S,1,-1)[0:1].reshape(1,-1),np.ones((1,1)),p,q,st) if False else (None,None)
    out=[]
    for s in range(S):
        r,J=res_jac(X[s].reshape(1,-1),np.ones((1,1)),p,q,st)
        out.append(J.reshape(p,p*q))
    return np.array(out)
def gamma_dims(B,p,q,seed=0):
    n=B.shape[0]; rng=np.random.default_rng(seed); st=setup(p)
    S=n*(n+1)//2*3+20
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n))
    X=(C@B).reshape(S,p,q)
    G=grads(X,p,q,st)
    def rk(A): 
        s=np.linalg.svd(A,compute_uv=False); return (s>1e-9*s[0]).sum()
    J=np.ones((1,p*q))
    r1=rk(np.vstack([J,G[:,1,:]]))
    r2=rk(np.vstack([J,G[:,1,:],G[:,2,:]]))
    r3=rk(np.vstack([J,G[:,1,:],G[:,2,:],G[:,3,:]]))
    r3only=rk(G[:,2,:]); r4only=rk(G[:,3,:])
    return dict(n=n,JQ=r1,JQG3=r2,all=r3,G3=r3only,G4=r4only)
