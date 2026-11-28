import random,time,collections
from fz import *
from run import margins
g=G([[0,2],[0,5],[1,2],[1,3],[2,3],[3,4],[4,5]]); rnd=random.Random(3)
c=star_circuit(g,rnd); print(len(c),g.P,g.ok(c))
c=renum(g.n,redc(g.n,c,g.X)[2]); print(len(c),g.ok(c))
ok=0;none=0;sizes=collections.Counter()
for t in range(300):
    c2=mutate(g,c,rnd,g.P+5)
    if c2 is None: none+=1; continue
    ok+=1; sizes[len(c2)]+=1
    if len(c2)<=g.P+5: c=c2
print(ok,none,sizes, margins(g,c))
