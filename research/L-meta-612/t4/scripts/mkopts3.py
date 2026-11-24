# option subsets for ablation: mode in none,P,basic,basicP,runs
import sys,json,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from graphs import G
from mkopts import opts
E=G(sys.argv[1]); mode=sys.argv[2]
g,o=opts(E,extra=False)
leaves=[v for v in g.sup if len(g.N[v])==1]
U=sorted({next(iter(g.N[v])) for v in leaves})
L=[]
if mode in ('P','basicP'): L.append([[],leaves,gneed(g,[],leaves)-1])
if mode in ('basic','basicP'): L+= [[list(a),list(b),nd-1] for (a,b),nd in o.items()]
if mode=='runs':  # options at bare vertices only plus rhoP
    L.append([[],leaves,gneed(g,[],leaves)-1])
    for (a,b),nd in o.items():
        if set(a)|set(b) <= set(g.sup)-set(leaves)-set(U) or (len(a)>1 and b==()): L.append([list(a),list(b),nd-1])
print(json.dumps(L))
