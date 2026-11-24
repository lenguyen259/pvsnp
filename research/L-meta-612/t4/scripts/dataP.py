import sys,json,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
GS={}
def struct(g,c,P,L):
    """min over pendants: 0 none; 1 single OR reader; 2 +reader has single AND reader; 3 +F_u=1"""
    lv=3
    for v in P:
        u=L[v]; rd=[x for x in c if v in x[2:]]
        if len(rd)!=1 or rd[0][1]!='|': return 0
        rg=[x for x in c if rd[0][0] in x[2:]]
        if len(rg)!=1 or rg[0][1]!='&': lv=min(lv,1); continue
        if sum(1 for x in c if u in x[2:])!=1: lv=min(lv,2)
    return lv
st=collections.Counter(); mins={}
files=sys.argv[1:] if __name__=="__main__" else []
for fn in files:
  for l in open(fn):
    D=json.loads(l); name=D['g']
    if not name.startswith('psun'): continue
    if name not in GS:
        _,n,S=name.split(':'); E,L=psun(int(n),[int(x) for x in S.split(',')]); g=Graph(E); GS[name]=(g,list(L),L,gneed(g,[],list(L)))
    g,P,L,nd=GS[name]; c=parse(D['c'])
    lev=struct(g,c,P,L)
    e=elim(g,c,{v:1 for v in P})
    key=(name,lev); d=e-nd
    st[(name,lev,d,D['s'])]+=1
for k in sorted(st): print(k,st[k])
