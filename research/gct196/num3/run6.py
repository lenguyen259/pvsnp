import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
from gam import *
import glob
rng=np.random.default_rng(7)
for f in sorted(glob.glob('/home/user/pvsnp/research/gct196/num/*.npy')):
    B=np.load(f)
    if B.ndim!=2 or B.shape[1]!=28: continue
    iv=invariants(B,rng); print(f.split('/')[-1],iv['n'],'D',iv['D'],'Gam',iv['Gam'],'Gam-2n',iv['Gam']-2*iv['n'],'orth %.1e'%iv['orth'])
