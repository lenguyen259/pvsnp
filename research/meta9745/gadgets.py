# rectangle gadgets (OR A) & (OR B), A in left, B in right: cost |A|+|B|-1 gates, covers e(A,B) edges,
# junk |A||B|-e(A,B) non-edges. excess = e - (|A|+|B|-1) is the gain over stars if junk were free.
import itertools
from g import E
ES=set(E); best={}
for a in range(1,8):
    for A in itertools.combinations(range(7),a):
        for b in range(1,8):
            for B in itertools.combinations(range(7,14),b):
                e=sum((u,v) in ES for u in A for v in B)
                ex=e-(a+b-1); key=(a,b)
                if key not in best or ex>best[key][0]: best[key]=(ex,e,a*b-e,A,B)
for k in sorted(best):
    if best[k][0]>=0: print(k,'excess',best[k][0],'edges',best[k][1],'junk',best[k][2],best[k][3],best[k][4])
