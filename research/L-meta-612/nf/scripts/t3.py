from base import *
# candidate inequalities over all circuits
def stats(n,E,c):
    T=tts(n,c); S=sing(n,T); ES={frozenset(e) for e in E}
    m=sum(1 for x in c if x[1]=='&'); o=len(c)-m
    m0=sum(1 for i,op,j,k in c if op=='&' and not S[i])
    B2=sum(1 for i,op,j,k in c if op=='|' and S[j] and S[k] and len(S[i])>=2)
    Z=sum(1 for i,op,j,k in c if op=='|' and (not S[j] or not S[k]))
    clean=all(frozenset((u,v)) in ES for i,op,j,k in c if op=='&' for u in S[j]-S[k] for v in S[k]-S[j])
    n1=any(S[j]&S[k] for i,op,j,k in c if op=='&')
    n2=any((not S[j]) or (not S[k]) for i,op,j,k in c if op=='&')
    return dict(m=m,o=o,m0=m0,B2=B2,Z=Z,clean=clean,n1=n1,n2=n2,t=tauE(E),e=len(E))
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    d=stats(n,E,c)
    tests={'AND>=tau':d['m']>=d['t'],'OR>=E-1':d['o']>=d['e']-1,'size':len(c)>=d['e']+d['t']-1,
     'B2>=E-m0':d['B2']>=d['e']-d['m0'], 'Z>=m0-1':d['Z']>=d['m0']-1,'B2+Z>=E-1':d['B2']+d['Z']>=d['e']-1}
    cls=('clean' if d['clean'] else 'junk')+('N1' if d['n1'] else '')+('N2' if d['n2'] else '')
    for t,v in tests.items():
        cnt[(t,cls,v)]+=1
        if not v: ex.setdefault((t,cls),(fn.split('/')[-1],fmt(c)))
for k,v in sorted(cnt.items()): print(k,v)
for k,v in ex.items(): print(k,v)
