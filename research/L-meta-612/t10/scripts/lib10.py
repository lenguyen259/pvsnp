import sys,collections,itertools
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t8/scripts')
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from lib8 import *
from t2lib import load_cached, red, renum, triangle_free, fmt, parse
def c4free(g):
    for a in g.sup:
        for b in g.sup:
            if a<b and len(g.N[a]&g.N[b])>=2: return False
    return True
def girth5(g): return triangle_free(g) and c4free(g)
def isstar(g):
    return len(g.E)==max(len(g.N[v]) for v in g.sup)
def corpus(cache=True,pools_=True,only_g5=True):
    seen=set()
    if pools_:
        for s_,d in allsrc():
            g=Graph(d['E']); c=parse(d['c'])
            if only_g5 and not girth5(g): continue
            if isstar(g): continue
            k=(g.E,d['c'])
            if k in seen: continue
            seen.add(k); yield 'pool',g,c
    if cache:
        for fn,n,E,c in load_cached():
            g=Graph(E,n)
            if only_g5 and not girth5(g): continue
            if isstar(g): continue
            c=renum(n,red(g,c)); k=(g.E,fmt(c))
            if k in seen: continue
            seen.add(k); yield 'cache',g,c
def delta(g,v): return g.t-tau(g.Eminus({v}))
from t2lib import tau
