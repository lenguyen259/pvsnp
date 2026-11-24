"""sanity checks: Lemma N' (elim(x_u:=0,x_v:=1) >= F_u+2) and structure facts, on cache + pools."""
import json,sys,collections,random
from gen import *
st=collections.Counter(); G={}
def check(g,c):
    T=tables(g,c,{})
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        if not g.Eminus({u,v}): continue
        ors=[x for x in c if v in x[2:] and x[1]=='|' and u not in x[2:]]
        if not ors: continue
        Fu=sum(1 for x in c if u in x[2:])
        e=elim(g,c,{u:0,v:1}); st['N_inst']+=1
        if e<Fu+2: st['N_VIOL']+=1; print('VIOL',g.E,fmt(c),v)
        rv=[x for x in c if v in x[2:]]
        if len(rv)==1 and rv[0][1]=='|':
            gg=rv[0][0]; z=rv[0][2] if rv[0][3]==v else rv[0][3]
            rg=[x for x in c if gg in x[2:]]
            if len(rg)==1 and rg[0][1]=='&':
                q=rg[0]; y=q[2] if q[3]==gg else q[3]
                st['i_inst']+=1
                if not (T[y]>>(1<<u))&1: st['i_VIOL_y']+=1
                if (T[z]>>(1<<u))&1: st['i_VIOL_z']+=1
                if Fu==1:
                    p=[x for x in c if u in x[2:]][0]
                    if p[0]==q[0]:
                        # star: sing(z) = N(u)-v
                        S=sing(g,T,z)
                        st['star']+=1
                        if S!=frozenset(g.N[u]-{v}): st['star_VIOL_sing']+=1
                    elif p[1]=='|':
                        t=p[2] if p[3]==u else p[3]
                        fGu=0
                        for a,b in g.Eminus({u}): fGu|=g.X[a]&g.X[b]
                        st['ORp']+=1
                        if T[t]&~fGu: st['ORp_VIOL_t']+=1
                    else: st['ANDp_nonstar']+=1
seen=set(); n=0
for fn,nn,E,c in load_cached():
    g=Graph(E,nn)
    if g.t==1: continue
    c=renum(nn,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k); check(g,c); n+=1
print('cache',n,dict(st))
rnd=random.Random(5)
for pool in sys.argv[1:]:
    for l in open(pool):
        if rnd.random()>0.05: continue
        D=json.loads(l); key=tuple(map(tuple,D['E']))
        if key not in G: G[key]=Graph(key)
        check(G[key],parse(D['c']))
print('all',dict(st))
