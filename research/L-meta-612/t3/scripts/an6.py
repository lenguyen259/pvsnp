import json,sys,collections,random
from gen import *
rnd=random.Random(2); st=collections.Counter(); ex={}; G={}
frac=float(sys.argv[1])
for pool in sys.argv[2:]:
  for l in open(pool):
    if rnd.random()>frac: continue
    D=json.loads(l); key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]; c=parse(D['c']); s=len(c)-g.P
    T=tables(g,c,{})
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v])); d=len(g.N[u])
        if d<3: continue
        rv=[x for x in c if v in x[2:]]
        if len(rv)!=1 or rv[0][1]!='|': continue
        gg=rv[0][0]; z=rv[0][2] if rv[0][3]==v else rv[0][3]
        rg=[x for x in c if gg in x[2:]]
        struct = 'i' if (len(rg)==1 and rg[0][1]=='&') else 'other'
        Fu=[x for x in c if u in x[2:]]; kand=sum(1 for x in Fu if x[1]=='&')
        e,nd,okk=gopt(g,c,{u},{v})
        key2=(struct,s,len(Fu),kand)
        if struct=='i':
            q=rg[0]; y=q[2] if q[3]==gg else q[3]
            key2+=('y=xu' if y==u else 'y!=xu',)
        st[key2+(e-d,)]+=1
        ex.setdefault(key2+(e-d,),(D['g'],D['c'],v))
for k,v in sorted(st.items(),key=lambda kv:str(kv[0])): print(k,v)
import pickle; pickle.dump(ex,open('an6ex.pkl','wb'))
