import json
from canon import canon
L={1:[0,2,6],3:[2,4,8],4:[0,9],5:[0,7,8],6:[8,9],7:[2,9]}
c=[];n=10
def g(o,a,b): c.append([o,a,b]); return n+len(c)-1
ands=[]
for ctr,ls in L.items():
    x=ls[0]
    for y in ls[1:]: x=g('|',x,y)
    ands.append(g('&',ctr,x))
x=ands[0]
for y in ands[1:]: x=g('|',x,y)
cc=canon(c)
E=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
for r in range(1024):
    v=[(r>>u)&1 for u in range(n)]
    for o,j,k in cc: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
    assert v[-1]==any(v[a] and v[b] for a,b in E)
print(json.dumps(cc))
