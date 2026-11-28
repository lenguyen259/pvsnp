import sys,itertools,json
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from graphs import G
from mkopts import opts
E=G(sys.argv[1]); maxneed=int(sys.argv[2])
g,o=opts(E,extra=False)
_,o2=opts(E,extra=True)
leaves=[v for v in g.sup if len(g.N[v])==1]
for r in range(1,len(leaves)+1):
    for S1 in itertools.combinations(leaves,r):
        nd=gneed(g,[],S1)
        if nd: o[((),tuple(S1))]=nd
for k,nd in o2.items():
    if nd<=maxneed: o[k]=nd
OFF=int(sys.argv[3]) if len(sys.argv)>3 else 0
L=[[list(a),list(b),nd-1+OFF] for (a,b),nd in o.items()]
print(json.dumps(L))
