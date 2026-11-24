import sys,collections
sys.path.insert(0,'../orb')
from tr import load,DIRS
c=collections.Counter(); g=collections.Counter()
for fn,n,E,X,cc in load(DIRS):
    d=collections.Counter(x for e in E for x in e)
    md=max(d.values())
    c[md]+=1
    if md<=3: g[tuple(E)]+=1
print(c); print(len(g))
for E,k in sorted(g.items(),key=lambda t:(len(t[0]),t[0])): print(E,k)
