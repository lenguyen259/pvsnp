import sys,json,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
from dataP import struct
GS={}; st=collections.Counter()
for l in open(sys.argv[1]):
    D=json.loads(l); name=D['g']
    if not name.startswith('psun'): continue
    if name not in GS:
        _,n,S=name.split(':'); E,L=psun(int(n),[int(x) for x in S.split(',')]); g=Graph(E); GS[name]=(g,list(L),L)
    g,P,L=GS[name]; c=parse(D['c'])
    if struct(g,c,P,L)<1: continue
    T=tables(g,c,{}); eP=sum(1<<v for v in P)
    zs=[]
    for v in P:
        r=[x for x in c if v in x[2:]][0]; z=r[2] if r[3]==v else r[3]; zs.append((T[z]>>eP)&1)
    e=elim(g,c,{v:1 for v in P})
    # first-order |R|+|dR|
    TP=tables(g,c,{v:1 for v in P}); R=[x[0] for x in c if (T[x[0]]>>eP)&1]
    Rs=set(R)|set(P); dR=[x[0] for x in c if x[1]=='&' and x[0] not in Rs and (x[2] in Rs or x[3] in Rs)]
    st[(name,'z(eP)=1' if any(zs) else 'z0', 'e>=2k' if e>=2*len(P) else 'VIOL', 'R+dR>=2k' if len(R)+len(dR)>=2*len(P) else 'RVIOL')]+=1
    if not any(zs) and e<2*len(P): print('VIOL',name,D['c'],e)
for k in sorted(st): print(k,st[k])
