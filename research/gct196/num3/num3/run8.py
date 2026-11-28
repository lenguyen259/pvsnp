import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
exec(open('run7.py').read().split('for name,Bs in list')[0])
import glob
for f in sorted(glob.glob('solD_*.npy')):
    B=np.load(f); print(f,analyze(B))
