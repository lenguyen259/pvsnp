"""Function-set distance from stuck non-STAR-ALL minimum circuits to STAR-ALL minimum circuits."""
import pickle,collections
from t2lib import *
from exch import nviol
still=pickle.load(open('exch_still.pkl','rb'))
SA=collections.defaultdict(list)
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1: continue
    c=renum(n,red(g,c))
    if len(c)!=g.P or nviol(g,c): continue
    T=tables(g,c,{}); SA[g.E].append(frozenset(T[i] for i,_,_,_ in c))
hist=collections.Counter(); ex={}
for E,s,v0,_ in still:
    g=Graph(E); c=renum(g.n,red(g,parse(s))); T=tables(g,c,{})
    F=frozenset(T[i] for i,_,_,_ in c)
    d=min(len(F-F2) for F2 in SA[g.E]) if SA[g.E] else None
    hist[d]+=1
    if d not in ex: ex[d]=(E,s)
print(dict(hist)); 
for d in sorted(ex): print(d,ex[d])
