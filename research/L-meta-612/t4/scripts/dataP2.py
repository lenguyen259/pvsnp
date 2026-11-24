import sys,json,collections,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
from dataP import struct
GS={}; st=collections.Counter(); ex={}
for fn in sys.argv[1:]:
  for l in open(fn):
    D=json.loads(l); name=D['g']
    if not name.startswith('psun'): continue
    if name not in GS:
        _,n,S=name.split(':'); S=[int(x) for x in S.split(',')]; E,L=psun(int(n),S); g=Graph(E); P=list(L)
        cand={'rhoP':([],P),'rho*':(S,P)}
        # all (S0 subset U, S1=P), and (S0 = U + one bare, S1=P)
        for r in range(len(S)+1):
            for S0 in itertools.combinations(S,r): cand['U%s'%(''.join(map(str,S0)))]=(list(S0),P)
        GS[name]=(g,P,L,{k:(a,b,gneed(g,a,b)) for k,(a,b) in cand.items()})
    g,P,L,cand=GS[name]; c=parse(D['c'])
    if struct(g,c,P,L)!=3: continue
    best=-99
    for k,(a,b,nd) in cand.items():
        if nd is None: continue
        rho={x:0 for x in a}; rho.update({x:1 for x in b})
        d=elim(g,c,rho)-nd; st[(name,k,d)]+=1; best=max(best,d)
        if (name,k) not in ex or d<ex[(name,k)][0]: ex[(name,k)]=(d,D['c'],D['s'])
    st[(name,'BEST',best)]+=1
for k in sorted(st): print(k,st[k])
for k in sorted(ex): print(k,ex[k])
