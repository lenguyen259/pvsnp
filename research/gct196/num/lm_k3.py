import os; os.environ['OMP_NUM_THREADS']='1'
exec(open('/home/user/pvsnp/research/gct196/num/lm2.py').read().split('if __name__')[0])
KMAX=3
_orig=res_jac
def res_jac3(B,C,p,q,st,want_jac=True):
    r,J=_orig(B,C,p,q,st,want_jac)
    S=C.shape[0]
    r=r.reshape(S,p)[:,:KMAX].ravel()
    if J is not None: J=J.reshape(S,p,-1)[:,:KMAX,:].reshape(S*KMAX,-1)
    return r,J
res_jac=res_jac3
import sys
p,q=4,7
for n in [int(a) for a in sys.argv[1:]]:
    best=9
    for s in range(4):
        c,B=search(p,q,n,s,iters=300)
        rng=np.random.default_rng(77); st=setup(p)
        Cc=rng.normal(size=(400,n))+1j*rng.normal(size=(400,n)); Cc/=np.linalg.norm(Cc,axis=1,keepdims=True)
        r,_=res_jac(B/np.linalg.norm(B,axis=1,keepdims=True),Cc,p,q,st,False); ch=np.abs(r).max(); best=min(best,ch)
        if ch<1e-9: break
    print('k<=3 only: n',n,'best',best,flush=True)
