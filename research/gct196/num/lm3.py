import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num')
from lm2 import *
def subspace_basis(p,q,kind):
    # orthonormal (real) basis of ambient subspace
    I=np.eye(p*q)
    cons=[]
    if kind in ('row','dc'):
        for r in range(p):
            v=np.zeros((p,q)); v[r,:]=1; cons.append(v.ravel())
    if kind in ('col','dc'):
        for j in range(q):
            v=np.zeros((p,q)); v[:,j]=1; cons.append(v.ravel())
    if kind=='all':
        v=np.ones((p,q)); cons.append(v.ravel())
    A=np.array(cons); u,s,vh=np.linalg.svd(A); k=(s>1e-9).sum()
    return vh[k:]   # rows: basis of nullspace
def search_sub(p,q,n,seed,Pb,iters=600,tol=1e-24):
    rng=np.random.default_rng(seed); st=setup(p)
    S=int(1.3*math.comb(n+p-1,p))+60
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n)); C/=np.linalg.norm(C,axis=1,keepdims=True)
    d=Pb.shape[0]
    Y=rng.normal(size=(n,d))+1j*rng.normal(size=(n,d))
    Y=orth(Y)
    def RJ(Y,wj=True):
        r,J=res_jac(Y@Pb,C,p,q,st,wj)
        if wj: J=(J.reshape(-1,n,p*q)@Pb.T).reshape(J.shape[0],n*d)
        return r,J
    r,J=RJ(Y); cost=np.vdot(r,r).real; mu=1e-2
    for it in range(iters):
        A=J.conj().T@J; g=J.conj().T@r; ok=False
        while mu<1e10:
            dlt=np.linalg.solve(A+mu*np.eye(A.shape[0]),-g)
            Y2=orth(Y+dlt.reshape(n,d)); r2,_=RJ(Y2,False); c2=np.vdot(r2,r2).real
            if c2<cost: Y=Y2; mu=max(mu/3,1e-14); ok=True; break
            mu*=4
        if not ok: break
        r,J=RJ(Y); cost=np.vdot(r,r).real
        if cost<tol: break
    return cost,Y@Pb
if __name__=='__main__':
    p,q,n,s0,s1=map(int,sys.argv[1:6]); kind=sys.argv[6]
    Pb=subspace_basis(p,q,kind)
    for s in range(s0,s1):
        t=time.time(); cost,B=search_sub(p,q,n,s,Pb)
        ch=check(B,p,q)
        print(kind,p,q,n,'seed',s,'cost %.3g'%cost,'check %.3g'%ch,'time',round(time.time()-t,1),flush=True)
        if ch<1e-9: np.save(f'/home/user/pvsnp/research/gct196/num/sol_{kind}_{p}x{q}_{n}_{s}.npy',B)
