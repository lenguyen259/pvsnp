exec(open('/home/user/pvsnp/research/gct196/num/gam.py').read())
from lm3 import search_sub
import sys
p,q=4,7
def T1orth(B):
    T=T1basis(B,p,q)
    Q,_=np.linalg.qr(T.T); return Q.T  # orthonormal rows (complex)
def Gtype():
    z=np.exp(2j*np.pi/6); v=np.array([0]+[z**k for k in range(6)]); B=[]
    for r in range(1,4):
        M=np.zeros((p,q),complex); M[0,0]=1; M[r,0]=-1; B.append(M.ravel())
    for r in range(4):
        M=np.zeros((p,q),complex); M[r,:]=v; B.append(M.ravel())
    return np.array(B)
def C4v7():
    z7=np.exp(2j*np.pi/7); v7=np.array([z7**k for k in range(7)]); B=[]
    for r in range(4):
        M=np.zeros((p,q),complex); M[r,:]=v7; B.append(M.ravel())
    return np.array(B)
which=sys.argv[1]; B0=Gtype() if which=='G' else C4v7()
Pb=T1orth(B0); print(which,'T1 dim',Pb.shape[0],flush=True)
for n in range(B0.shape[0]+1,min(Pb.shape[0],11)+1):
    best=None
    for s in range(12):
        c,B=search_sub(p,q,n,s,Pb,iters=400)
        ch=check(B,p,q)
        best=ch if best is None else min(best,ch)
        if ch<1e-9:
            print(which,'FOUND level dim',n,'seed',s,'T1',T1(B,p,q),flush=True); np.save(f'ext_{which}_{n}.npy',B); break
    print(which,'n',n,'best check',best,flush=True)
