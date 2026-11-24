from lib10 import *
from t2lib import ok, elim, starall_viol
E=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
g=Graph(E); c=parse(open('petcex.txt').read().strip())
print('correct(all 2^n)',ok(g,c),'size',len(c),'Phi',g.P,'reduced?',len(renum(g.n,red(g,c)))==len(c))
mx=-99; best=[]
for nm,v,rho,need in g.options():
    ld=LD(g,c,rho); lr=LR(g,c,rho); e=elim(g,c,rho)
    mx=max(mx,ld-need)
    if lr>=need or e>=need: best.append((nm,v,ld,lr,e,need))
print('max LD-need',mx); print('options good by LR/elim:',best)
print('viol',sorted({t for i,t in starall_viol(g,c)}))
