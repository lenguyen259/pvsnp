import warnings; warnings.filterwarnings('ignore')
from gen import gen
from model import solve, build
from common import analyze, fmt
hits=0
for n,E in gen():
    r=solve(n,E,40)
    if r is None: continue
    c=build(n,E,*r); a=analyze(n,c,E)
    hits+=1; print(n,E,'size',a['size'],'ok',a['ok'],'slack',a['slack'],a['ch'])
print('hits',hits)
