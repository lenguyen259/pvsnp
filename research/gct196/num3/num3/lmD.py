import sys, os
os.environ['OMP_NUM_THREADS']='1'
sys.path.insert(0,'/home/user/pvsnp/research/gct196/num')
from lm2 import *
from lm3 import subspace_basis
def search_D(p,q,n,nd,seed,iters=500,tol=1e-26):
    # first nd basis vectors doubly centred, rest free in sum-zero space
    rng=np.random.default_rng(seed); st=setup(p)
    Pdc=subspace_basis(p,q,'dc'); Pall=subspace_basis(p,q,'all')
    S=int(1.3*math.comb(n+p-1,p))+60
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n)); C/=np.linalg.norm(C,axis=1,keepdims=True)
    dims=[Pdc.shape[0]]*nd+[Pall.shape[0]]*(n-nd)
    Ps=[Pdc]*nd+[Pall]*(n-nd)
    Y=[rng.normal(size=d)+1j*rng.normal(size=d) for d in dims]
    def build(Y):
        B=np.array([y@P for y,P in zip(Y,Ps)]); return B
    def norm(Y): return [y/np.linalg.norm(y) for y in Y]
    def RJ(Y,wj=True):
        B=build(Y); r,J=res_jac(B,C,p,q,st,wj)
        if wj:
            J=J.reshape(J.shape[0],n,p*q)
            J=np.hstack([J[:,i,:]@Ps[i].T for i in range(n)])
        return r,J
    Y=norm(Y); r,J=RJ(Y); cost=np.vdot(r,r).real; mu=1e-2
    for it in range(iters):
        A=J.conj().T@J; g=J.conj().T@r; ok=False
        while mu<1e10:
            dl=np.linalg.solve(A+mu*np.eye(A.shape[0]),-g)
            Y2=[]; k=0
            for i in range(n): Y2.append(Y[i]+dl[k:k+dims[i]]); k+=dims[i]
            Y2=norm(Y2); r2,_=RJ(Y2,False); c2=np.vdot(r2,r2).real
            if c2<cost: Y=Y2; mu=max(mu/3,1e-14); ok=True; break
            mu*=4
        if not ok: break
        r,J=RJ(Y); cost=np.vdot(r,r).real
        if cost<tol: break
    return cost,build(Y)
if __name__=='__main__':
    p,q,n,nd,s0,s1=map(int,sys.argv[1:7])
    import time
    for s in range(s0,s1):
        t=time.time(); cost,B=search_D(p,q,n,nd,s); ch=check(B,p,q)
        print(n,nd,'seed',s,'cost %.2g check %.2g'%(cost,ch),round(time.time()-t,1),flush=True)
        if ch<1e-9: np.save(f'/home/user/pvsnp/research/gct196/num3/solD_{n}_{nd}_{s}.npy',B)
