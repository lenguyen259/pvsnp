from common import *
from jtrick import jt
# case-(a) graph with two disjoint hub edges: triangles a b p, c d q; paths a-r-c, b-s-d
# a0 b1 c2 d3 p4 q5 r6 s7
E=[(0,1),(0,4),(1,4),(2,3),(2,5),(3,5),(0,6),(2,6),(1,7),(3,7)]
n=8; print('C4',has_c4(n,E),'tau',tau(E))
r=analyze(n,jt(n,E,[(0,1),(2,3)],[0,1,2,3]),E)
print({k:r[k] for k in ('ok','size','nor','nand','ch','deg','slack')}); print(fmt(r['R']))
