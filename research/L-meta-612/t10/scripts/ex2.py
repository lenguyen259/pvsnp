# stuck circuits of ex1: add distributive move (x|a)&(x|b) -> x|(a&b); greedy descent with single edits + distributive
import json,sys
from lib10 import *
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from exch import nviol, edits
from t2lib import ok
def dist_moves(g,c):
    gate={x[0]:x for x in c}
    for t,(i,o,j,k) in enumerate(c):
        if o!='&' or j<g.n or k<g.n: continue
        _,o1,a1,b1=gate[j]; _,o2,a2,b2=gate[k]
        if o1!='|' or o2!='|': continue
        for x in {a1,b1}&{a2,b2}:
            a=b1 if a1==x else a1; b=b2 if a2==x else a2
            new=max(y[0] for y in c)+1
            c2=c[:t]+[(new,'&',a,b),(i,'|',x,new)]+c[t+1:]
            yield renum(g.n,c2)
def step(g,c):
    v0=nviol(g,c); s0=len(c)
    for c2 in list(dist_moves(g,c))+list(edits(g,c)):
        if not ok(g,c2): continue
        r=renum(g.n,red(g,c2))
        if len(r)<s0 or (len(r)==s0 and nviol(g,r)<v0): return r
    return None
st=collections.Counter()
for E,s,ex_,v0 in json.load(open('ex1_stuck.json')):
    g=Graph([tuple(e) for e in E]); c=parse(s)
    d=next(dist_moves(g,c),None)
    st['has_dist_move']+= d is not None
    while True:
        r=step(g,c)
        if r is None: break
        c=r
    st[('final',len(c)-g.P,nviol(g,c))]+=1
print(dict(st))
best=None
for E,s,ex_,v0 in json.load(open('ex1_stuck.json')):
    g=Graph([tuple(e) for e in E]); c=parse(s)
    while True:
        r=step(g,c)
        if r is None: break
        c=r
    if nviol(g,c)>0 and (best is None or len(c)<len(best[1].split())): best=(g.E,fmt(c),len(c)-g.P)
print('STILLSTUCK',best)
