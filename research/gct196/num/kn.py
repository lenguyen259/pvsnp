import os; os.environ['OMP_NUM_THREADS']='1'
exec(open('/home/user/pvsnp/research/gct196/num/ext_search.py').read().split('which=sys.argv')[0])
def rk(A,tol=1e-8):
    if len(A)==0: return 0
    s=np.linalg.svd(np.atleast_2d(A),compute_uv=False); return int((s>tol*max(1,s[0])).sum())
def Nprime(p,q):
    out=[]
    for r in range(p):
        M=np.zeros((p,q)); M[r,:]=1; out.append(M.ravel())
    for j in range(q):
        M=np.zeros((p,q)); M[:,j]=1; out.append(M.ravel())
    A=np.array(out); u,s,vh=np.linalg.svd(A); return vh[:(s>1e-9).sum()]
def phi(x,p,q):
    X=x.reshape(p,q); S=X.mean(); a=X.mean(1)-S; b=X.mean(0)-S
    d=X-a[:,None]-b[None,:]-S
    al=(2-q)/2; be=(2-p)/2
    return (d+al*a[:,None]+be*b[None,:]+S).ravel()
def G3(x,p,q,st):
    r,J=res_jac(x.reshape(1,-1),np.ones((1,1)),p,q,st); return J.reshape(p,p*q)[2]
def analyze(B,p,q,name):
    st=setup(p); n=B.shape[0]; Np=Nprime(p,q)
    rng=np.random.default_rng(0)
    # identity check: G3(x) - 2 phi(x)^2 in N'
    x=(rng.normal(size=n)+1j*rng.normal(size=n))@B
    g=G3(x,p,q,st); h=2*phi(x,p,q)**2
    res=(g-h)-((g-h)@Np.conj().T)@Np
    print(name,'identity residual',np.abs(res).max())
    Wb=np.vstack([np.array([phi(b,p,q) for b in B]),np.ones(p*q)])
    prods=np.array([Wb[i]*Wb[j] for i in range(len(Wb)) for j in range(i,len(Wb))])
    u,s,vh=np.linalg.svd(prods); k=(s>1e-8*s[0]).sum(); WW=vh[:k]
    e=k+len(Np)-rk(np.vstack([WW,Np]))
    # stabilizer: x with x*WW ⊆ WW : solve linear system
    m=p*q; P_perp=np.eye(m)-WW.T@WW.conj()  # projector onto complement (WW orthonormal rows conj)
    # x -> (x*w_i) projected off WW for each i must vanish
    A=np.vstack([P_perp@np.diag(w) for w in WW])
    sv=np.linalg.svd(A,compute_uv=False); s_dim=(sv<1e-8*sv[0]).sum()+max(0,m-len(sv))
    print(name,'n',n,'dim WoW',k,'e=dim(WoW∩N\')',e,'stab dim',s_dim,'Kneser bound 2n+2-s',2*n+2-s_dim, gamma_dims(B,p,q))
if __name__=='__main__':
    p,q=4,7
    F,H=known(p,q)
    analyze(F,p,q,'F7'); analyze(H,p,q,'hook'); analyze(np.load('ext_G_8.npy'),p,q,'N8'); analyze(Gtype(),p,q,'G7')
