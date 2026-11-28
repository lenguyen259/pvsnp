import sys,json,collections,itertools
from lib6 import *
POOL='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t3/locpool.jsonl'
GS={}
def setup(name):
    _,n,S=name.split(':'); n=int(n); S=[int(x) for x in S.split(',')]
    E,L=psun(n,S); g=Graph(E); P=list(L); R=runs(n,S); rv=[w for r in R for w in r]
    fam={}
    # P u B
    for r in range(len(rv)+1):
        for B in itertools.combinations(rv,r):
            sub={x:('c',1) for x in P+list(B)}
            nd=need_sub(g,sub)
            if nd is None or nd=='bad': continue
            fam[('PB',B)]=(sub,nd)
    # shortening
    for w in range(n):
        w2=(w+1)%n
        if w in S or w2 in S: continue
        a=(w-1)%n; b=(w2+1)%n
        sub={w:('v',b),w2:('v',a)}
        nd=need_sub(g,sub); fam[('SH',(w,w2))]=(sub,nd)
    # single identifications x_w:=x_y
    for w in range(g.n):
        for y in range(g.n):
            if y==w: continue
            sub={w:('v',y)}; nd=need_sub(g,sub)
            if nd is None or nd=='bad': continue
            fam[('ID',(w,y))]=(sub,nd)
    return g,P,L,fam
st=collections.Counter(); ex={}
lim=int(sys.argv[1]) if len(sys.argv)>1 else 10**9
cnt=0
for l in open(POOL):
    D=json.loads(l); name=D['g']
    if not name.startswith('psun'): continue
    if name not in GS: GS[name]=setup(name); print(name,{k:v[1] for k,v in GS[name][3].items() if k[0]!='ID'})
    g,P,L,fam=GS[name]; c=parse(D['c'])
    if struct(g,c,P,L)!=3: continue
    cnt+=1
    if cnt>lim: break
    best=collections.defaultdict(lambda:-99)
    for k,(sub,nd) in fam.items():
        if nd=='bad': continue
        d=elim_sub(g,c,sub)-nd
        best[k[0]]=max(best[k[0]],d)
        if k[0]=='SH': st[(name,'SH',k[1],d)]+=1
    for f in ('PB','SH','ID'):
        st[(name,f,'good' if best[f]>=0 else 'bad')]+=1
        if best[f]<0 and (name,f) not in ex: ex[(name,f)]=(D['c'],D['s'])
    st[(name,'any','good' if max(best.values())>=0 else 'bad')]+=1
print(cnt)
for k in sorted(st,key=str): print(k,st[k])
for k in ex: print(k,ex[k])
