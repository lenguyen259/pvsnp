import os
os.environ['OMP_NUM_THREADS']='1'; os.environ['OPENBLAS_NUM_THREADS']='1'
exec(open('/home/user/pvsnp/research/gct196/num/gam.py').read())
import sys, itertools
p,q=4,7
def permmat(rho,gam):
    m=p*q; P=np.zeros((m,m))
    for r in range(p):
        for j in range(q): P[rho[r]*q+gam[j], r*q+j]=1
    return P
def eig_blocks(P):
    w,V=np.linalg.eig(P)
    # group by eigenvalue
    blocks=[]; used=np.zeros(len(w),bool)
    for i in range(len(w)):
        if used[i]: continue
        idx=np.where(np.abs(w-w[i])<1e-6)[0]; used[idx]=True
        Q,_=np.linalg.qr(V[:,idx]); blocks.append((w[i],Q.T.conj().conj()))  # rows basis
    return blocks
def search_blocks(blocks,dims,seed,iters=300):
    rng=np.random.default_rng(seed); st=setup(p)
    n=sum(dims)
    S=int(1.3*math.comb(n+p-1,p))+60
    C=rng.normal(size=(S,n))+1j*rng.normal(size=(S,n)); C/=np.linalg.norm(C,axis=1,keepdims=True)
    Ys=[orth(rng.normal(size=(d,b.shape[0]))+1j*rng.normal(size=(d,b.shape[0]))) if d>0 else None for (w,b),d in zip(blocks,dims)]
    def build(Ys): return np.vstack([Y@b for Y,(w,b) in zip(Ys,blocks) if Y is not None])
    def RJ(Ys,wj=True):
        B=build(Ys); r,J=res_jac(B,C,p,q,st,wj)
        if not wj: return r,None
        J=J.reshape(J.shape[0],n,p*q); cols=[]; row=0
        for Y,(w,b) in zip(Ys,blocks):
            if Y is None: continue
            d=Y.shape[0]; cols.append((J[:,row:row+d,:]@b.T).reshape(J.shape[0],-1)); row+=d
        return r,np.hstack(cols)
    def unflat(Ys,v):
        out=[];pos=0
        for Y in Ys:
            if Y is None: out.append(None); continue
            k=Y.size; out.append(orth(Y+v[pos:pos+k].reshape(Y.shape))); pos+=k
        return out
    r,J=RJ(Ys); cost=np.vdot(r,r).real; mu=1e-2
    for it in range(iters):
        A=J.conj().T@J; g=J.conj().T@r; ok=False
        while mu<1e10:
            dl=np.linalg.solve(A+mu*np.eye(A.shape[0]),-g)
            Y2=unflat(Ys,dl); r2,_=RJ(Y2,False); c2=np.vdot(r2,r2).real
            if c2<cost: Ys=Y2; mu=max(mu/3,1e-14); ok=True; break
            mu*=4
        if not ok: break
        r,J=RJ(Ys); cost=np.vdot(r,r).real
        if cost<1e-24: break
    return cost,build(Ys)
if __name__=='__main__':
    mode=sys.argv[1]; n=int(sys.argv[2]); trials=int(sys.argv[3])
    if mode=='c7': P=permmat([0,1,2,3],[(j+1)%7 for j in range(7)])
    elif mode=='c6': P=permmat([0,1,2,3],[0]+[1+(j%6) for j in range(1,7)])
    elif mode=='c3r': P=permmat([0,2,3,1],[0]+[1+(j%6) for j in range(1,7)])  # rows 1-3 cyclic, cols 1-6 6-cycle
    elif mode=='c3b': P=permmat([0,2,3,1],[(j+1)%7 for j in range(7)])
    blocks=eig_blocks(P); sizes=[b.shape[0] for w,b in blocks]
    print(mode,'block sizes',sizes,flush=True)
    rng=np.random.default_rng(int(sys.argv[4]) if len(sys.argv)>4 else 0)
    found=0
    for t in range(trials):
        # random dims profile
        while True:
            dims=[int(rng.integers(0,s+1)) for s in sizes]
            if sum(dims)==n: break
        cost,B=search_blocks(blocks,dims,t)
        ch=check(B,p,q)
        if ch<1e-8:
            found+=1; print(mode,n,'FOUND dims',dims,'T1',T1(B,p,q),flush=True); np.save(f'inv_{mode}_{n}_{t}.npy',B)
        elif t%10==0: print(mode,n,'trial',t,'dims',dims,'check %.2g'%ch,flush=True)
    print(mode,n,'done found',found,flush=True)
