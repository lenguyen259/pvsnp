import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
from gam import *
import glob
rng=np.random.default_rng(3)
for f in sorted(glob.glob('solD_*.npy')):
    iv=invariants(np.load(f),rng); print(f,iv['n'],'D',iv['D'],'G2',iv['G2'],'G23',iv['G23'],'Gam',iv['Gam'],'Gam-2n',iv['Gam']-2*iv['n'])
