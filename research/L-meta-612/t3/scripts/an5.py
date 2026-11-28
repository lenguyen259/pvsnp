import json,sys,collections,random
from gen import *
st=collections.Counter(); G={}; ex={}
rnd=random.Random(1)
pools=sys.argv[2:]; frac=float(sys.argv[1])
for pool in pools:
  for l in open(pool):
    if rnd.random()>frac: continue
    D=json.loads(l)
    key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]; c=parse(D['c'])
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        W=sorted(g.N[u]-{v})
        bat={'Nv':({u,v},()),"N'v":({u},{v}),'Bu':((),{u}),'Nu':(g.N[u]|{u},()),"N'u":((g.N[u]|{u})-{v},{v}),
             'v1W0':(set(W),{v}),'Bv':((),{v})}
        for i,w in enumerate(W):
            bat['Aw%d'%i]=({w},()); bat['Bw%d'%i]=((),{w}); bat['Nw%d'%i]=(g.N[w]|{w},())
            bat['v1w%d0'%i]=({w},{v})
        R={}
        for k,(S0,S1) in bat.items():
            r=gopt(g,c,S0,S1); R[k]=r is not None and r[2]
        st[(D['g'],'inst')]+=1
        for k in R:
            if R[k]: st[(D['g'],k)]+=1
        def fails(keys): return not any(R[k] for k in keys)
        for name,keys in [('Nv|Bu|Nu',['Nv','Bu','Nu']),("N'v|Bu|N'u",["N'v",'Bu',"N'u"]),("N'v|N'u",["N'v","N'u"]),('all',list(R)),
                          ("N'v|Bu|N'u|v1W0",["N'v",'Bu',"N'u",'v1W0'])]:
            if fails(keys):
                st[(D['g'],'FAIL '+name)]+=1; ex.setdefault((D['g'],name),(D['s'],D['c'],v,R))
for k,v in sorted(st.items()): print(k,v)
for k,v in ex.items(): print(k,v)
