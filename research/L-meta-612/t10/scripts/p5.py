# clean circuits (N3 everywhere), C4-free graphs incl. triangles: test split inequalities
from lib10 import *
from t2lib import sing, starall_viol
def counts(g,c):
    T=tables(g,c,{}); S={u:frozenset([u]) for u in range(g.n)}
    for i,o,j,k in c: S[i]=sing(g,T,i)
    m=sum(1 for x in c if x[1]=='&'); m0=sum(1 for x in c if x[1]=='&' and not S[x[0]])
    B2=sum(1 for i,o,j,k in c if o=='|' and S[j] and S[k] and len(S[i])>=2)
    B1=sum(1 for i,o,j,k in c if o=='|' and S[j] and S[k] and len(S[i])==1)
    Zc=sum(1 for i,o,j,k in c if o=='|' and (not S[j] or not S[k]))
    # creators: first AND accepting e purely with neither input accepting purely
    cre=set()
    for a,b in g.E:
        bit=(1<<a)|(1<<b)
        for i,o,j,k in c:
            if o!='&': continue
            if (T[i]>>bit)&1 and not (T[i]>>(1<<a))&1 and not (T[i]>>(1<<b))&1 and not ((T[j]>>bit)&1 and not (T[j]>>(1<<a))&1 and not (T[j]>>(1<<b))&1) and not ((T[k]>>bit)&1 and not (T[k]>>(1<<a))&1 and not (T[k]>>(1<<b))&1):
                cre.add(i); break
    mc=len(cre); m0c=sum(1 for i in cre if not S[i])
    return dict(m=m,m0=m0,B2=B2,B1=B1,Z=Zc,mc=mc,m0c=m0c)
st=collections.Counter(); ex={}
for src,g,c in corpus(only_g5=False):
    if not c4free(g): continue
    v=starall_viol(g,c)
    if any(t=='N3' for i,t in v): continue
    kind=('g5' if girth5(g) else 'tri', 'N1' if any(t=='N1' for i,t in v) else '-', 'N2' if any(t=='N2' for i,t in v) else '-')
    d=counts(g,c); E=len(g.E); t=g.t
    st[kind]+=1
    tests={'OR':d['B2']+d['Z']+d['B1']>=E-1,'AND':d['m']>=t,'B':d['B2']>=E-d['m0c'],'C':d['Z']+d['m']-d['m0c']>=t-1,
           'Bmc':d['B2']>=E-d['mc'],'Cmc':d['Z']+d['m']-d['mc']>=t-1,'size':len(c)>=g.P}
    for nm,okk in tests.items():
        if not okk:
            st[(kind,nm,'fail')]+=1
            if (kind,nm) not in ex or len(c)<len(ex[(kind,nm)][1].split()): ex[(kind,nm)]=(g.E,fmt(c),len(c)-g.P)
for k in sorted(st,key=str): print(k,st[k])
for k,v in sorted(ex.items(),key=str): print(k,v)
