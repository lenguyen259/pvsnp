import numpy as np, math, sys, time
def setup(p):
    N=1<<p
    pairs=[(A,B) for A in range(N) for B in range(N) if A&B==0]
    PA=np.array([a for a,b in pairs]); PB=np.array([b for a,b in pairs]); PU=PA|PB
    pc=np.array([bin(U).count('1') for U in range(N)])
    return PA,PB,PU,pc
def bmul(a,b,st):
    PA,PB,PU,pc=st
    out=np.zeros(a.shape,complex)
    prod=a[...,PA]*b[...,PB]
    for U in range(a.shape[-1]):
        pass
    np.add.at(out.T,PU,prod.T) if False else None
    # manual accumulate
    out=np.zeros(a.shape,complex)
    for idx in range(len(PU)):
        out[...,PU[idx]]+=prod[...,idx]
    return out
def colelem(X,j,p):
    S=X.shape[0]; e=np.zeros((S,1<<p),complex); e[:,0]=1
    for r in range(p): e[:,1<<r]=X[:,r,j]
    return e
def res_jac(B,C,p,q,st,want_jac=True):
    S=C.shape[0]; n=B.shape[0]
    X=(C@B).reshape(S,p,q)
    PA,PB,PU,pc=st
    els=[colelem(X,j,p) for j in range(q)]
    pre=[None]*(q+1); pre[0]=np.zeros((S,1<<p),complex); pre[0][:,0]=1
    for j in range(q): pre[j+1]=bmul(pre[j],els[j],st)
    full=pre[q]
    r=np.stack([full[:,pc==k].sum(1) for k in range(1,p+1)],1)  # S,p
    if not want_jac: return r,None
    suf=[None]*(q+1); suf[q]=np.zeros((S,1<<p),complex); suf[q][:,0]=1
    for j in range(q-1,-1,-1): suf[j]=bmul(els[j],suf[j+1],st)
    G=np.zeros((S,p,p,q),complex) # S,k,r,j
    for j in range(q):
        E=bmul(pre[j],suf[j+1],st)
        for rr in range(p):
            for k in range(1,p+1):
                mask=(pc==k-1)&((np.arange(1<<p)>>rr)&1==0)
                G[:,k-1,rr,j]=E[:,mask].sum(1)
    G=G.reshape(S,p,p*q)
    J=(G[:,:,None,:]*C[:,None,:,None]).reshape(S*p,n*p*q)
    return r.ravel(),J
def orth(B):
    Q,_=np.linalg.qr(B.T.conj()); return Q.T.conj()
def search(p,q,n,seed,iters=400,verbose=False,init=None,tol=1e-24):
    rng=np.random.default_rng(seed); st=setup(p)
    S=int(1.3*math.comb(n+p-1,p))+60
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n)); C/=np.linalg.norm(C,axis=1,keepdims=True)
    m=p*q
    B=rng.normal(size=(n,m))+1j*rng.normal(size=(n,m)) if init is None else init.copy()
    B=orth(B)
    r,J=res_jac(B,C,p,q,st); cost=np.vdot(r,r).real; mu=1e-2
    for it in range(iters):
        A=J.conj().T@J; g=J.conj().T@r
        ok=False
        while mu<1e10:
            d=np.linalg.solve(A+mu*np.eye(A.shape[0]),-g)
            B2=orth(B+d.reshape(n,m))
            r2,_=res_jac(B2,C,p,q,st,False); c2=np.vdot(r2,r2).real
            if c2<cost:
                B=B2; mu=max(mu/3,1e-14); ok=True; break
            mu*=4
        if not ok: break
        r,J=res_jac(B,C,p,q,st); cost=np.vdot(r,r).real
        if verbose and it%10==0: print(it,cost,mu,flush=True)
        if cost<tol: break
    return cost,B
def check(B,p,q,seed=12345):
    n=B.shape[0]; rng=np.random.default_rng(seed); st=setup(p)
    S=int(2*math.comb(n+p-1,p))+60
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n)); C/=np.linalg.norm(C,axis=1,keepdims=True)
    r,_=res_jac(B/np.linalg.norm(B,axis=1,keepdims=True),C,p,q,st,False); return np.abs(r).max()
if __name__=='__main__':
    p,q,n,s0,s1=map(int,sys.argv[1:6])
    for s in range(s0,s1):
        t=time.time(); cost,B=search(p,q,n,s)
        ch=check(B,p,q)
        print(p,q,n,'seed',s,'cost %.3g'%cost,'check %.3g'%ch,'time',round(time.time()-t,1),flush=True)
        if ch<1e-9: np.save(f'/home/user/pvsnp/research/gct196/num/sol_{p}x{q}_{n}_{s}.npy',B)
