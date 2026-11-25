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
for f in sorted(glob.glob('/home/user/pvsnp/research/gct196/num/walk_*_8.npy')): srcs[f.split('/')[-1]]=np.load(f)
for name,Bs in srcs.items():
    M=Bs.reshape(-1,p,q); R=M.sum(2); C=M.sum(1); n=rank(Bs)
    D=n-rank(np.hstack([R,C]))
    phi=[rank(np.hstack([M[:,u,:],R])) for u in range(p)]
    ru=[rank(M[:,u,:]) for u in range(p)]
    print(name,'n',n,'D',D,'lR',rank(R),'lC',rank(C),'r_u',ru,'rank phi_u',phi)
