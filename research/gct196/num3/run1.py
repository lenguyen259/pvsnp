import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
from gam import *
import glob
z=np.exp(2j*np.pi/6); v=np.array([0]+[z**k for k in range(6)]); B=[]
for r in range(1,4):
    M=np.zeros((p,q),complex); M[0,0]=1; M[r,0]=-1; B.append(M.ravel())
for r in range(4):
    M=np.zeros((p,q),complex); M[r,:]=v; B.append(M.ravel())
G7=np.array(B)
F,H=known(p,q)
srcs={'F7':F,'hook':H,'N8':np.load('/home/user/pvsnp/research/gct196/num/ext_G_8.npy'),'G7':G7}
for f in sorted(glob.glob('/home/user/pvsnp/research/gct196/num/walk_*_8.npy'))[:6]: srcs[f.split('/')[-1]]=np.load(f)
rng=np.random.default_rng(1)
worst={}
for name,Bs in srcs.items():
    print(name,invariants(Bs,rng),flush=True)
    n=Bs.shape[0]
    for k in range(1,n):
        for trial in range(int(sys.argv[1])):
            A=rng.normal(size=(k,n))+1j*rng.normal(size=(k,n))
            if trial%2: # coordinate subspace
                A=np.zeros((k,n),complex); A[np.arange(k),rng.permutation(n)[:k]]=1
            iv=invariants(A@Bs,rng)
            key=(iv['n'])
            val=iv['Gam']-2*iv['n']
            if key not in worst or val<worst[key][0]: worst[key]=(val,name,iv)
for k in sorted(worst): print(k,worst[k])
