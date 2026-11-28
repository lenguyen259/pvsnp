# U (star-cover) circuit of size |E|+tau-1 for a graph, in canonical form
import itertools, json, sys
from plib import canon
from grest import tau
def ucirc(E):
    n=max(max(e) for e in E)+1; t=tau(E)
    Vs=sorted({x for e in E for x in e})
    for T in itertools.combinations(Vs,t):
        if all(a in T or b in T for a,b in E): break
    c=[]; done=set(); ands=[]
    def g(o,a,b): c.append([o,a,b]); return n+len(c)-1
    for ctr in T:
        L=sorted({b if a==ctr else a for a,b in E if ctr in (a,b)}-done)
        done.add(ctr)
        if not L: continue
        x=L[0]
        for y in L[1:]: x=g('|',x,y)
        ands.append(g('&',ctr,x))
    x=ands[0]
    for y in ands[1:]: x=g('|',x,y)
    return canon(c,n)
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])]; c=ucirc(E); print(len(c)); print(json.dumps(c))
