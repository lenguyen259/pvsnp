import os; os.environ['OMP_NUM_THREADS']='1'
exec(open('/home/user/pvsnp/research/gct196/num/ext.py').read())
from lm3 import search_sub
p,q=4,6
z=np.exp(2j*np.pi/5); v=np.array([0]+[z**k for k in range(5)]); B=[]
for r in range(1,4):
    M=np.zeros((p,q),complex); M[0,0]=1; M[r,0]=-1; B.append(M.ravel())
for r in range(4):
    M=np.zeros((p,q),complex); M[r,:]=v; B.append(M.ravel())
B=np.array(B); print('G4 level',check(B,p,q),'T1',T1(B,p,q),flush=True)
T=T1basis(B,p,q); Qm,_=np.linalg.qr(T.T); Pb=Qm.T
for n in range(8,Pb.shape[0]+1):
    for s in range(10):
        c,Bn=search_sub(p,q,n,s,Pb,iters=300)
        ch=check(Bn,p,q)
        if ch<1e-9: print('4x6 FOUND',n,'T1',T1(Bn,p,q),flush=True); np.save(f'g46_{n}.npy',Bn); break
    else:
        print('4x6 none at',n,flush=True); break
# F_6 row-centred (dim 7) and hook (dim 7) T1
w=np.exp(2j*np.pi/3)
def E(r,j): M=np.zeros((p,q),complex); M[r,j]=1; return M
F=[];a=np.zeros((p,q),complex); al=[1,w,w*w]; be=[1,w*w,w]
for k in range(3): a[k+1,0]=al[k]; a[k+1,1]=-al[k]
F.append(a.ravel()); b=np.zeros((p,q),complex)
for k in range(3): b[k+1,2]=be[k]; b[k+1,3]=-be[k]
F.append(b.ravel())
for j in range(1,q): F.append((E(0,0)-E(0,j)).ravel())
F=np.array(F); print('F6 level',check(F,p,q),'T1',T1(F,p,q))
