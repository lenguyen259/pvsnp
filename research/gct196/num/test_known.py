import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num')
from lev import *
p,q=4,7
w=np.exp(2j*np.pi/3)
def E(r,j): M=np.zeros((p,q),complex); M[r,j]=1; return M
# F_7: rows1-3: x*(1,w,w^2)^T(e1-e2)+y*(1,w^2,w)^T(e3-e4); row0 sum-zero
B=[]
a=np.zeros((p,q),complex); al=[1,w,w*w]; be=[1,w*w,w]
for k in range(3): a[k+1,0]=al[k]; a[k+1,1]=-al[k]
B.append(a.ravel())
b=np.zeros((p,q),complex)
for k in range(3): b[k+1,2]=be[k]; b[k+1,3]=-be[k]
B.append(b.ravel())
for j in range(1,q): B.append((E(0,0)-E(0,j)).ravel())
B=np.array(B); print('F7 dim',np.linalg.matrix_rank(B),'res',is_level(B,p,q))
# hook: row0 sum zero + column0 rows1-3 sum zero
H=[(E(0,0)-E(0,j)).ravel() for j in range(1,q)]+[(E(1,0)-E(r,0)).ravel() for r in (2,3)]
H=np.array(H); print('hook dim',len(H),'res',is_level(H,p,q))
# hook bigger? add E(1,0)-E(0,1)?
