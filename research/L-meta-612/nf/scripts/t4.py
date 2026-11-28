from base import *
def stats(n,E,c):
    T=tts(n,c); S=sing(n,T); ES={frozenset(e) for e in E}
    # first creators
    acc=lambda p,u,v: (T[p]>>((1<<u)|(1<<v)))&1
    creators=set()
    for (u,v) in E:
        for i,op,j,k in c:
            if acc(i,u,v) and u not in S[i] and v not in S[i]:
                creators.add(i); break
    m=sum(1 for x in c if x[1]=='&')
    m0=sum(1 for i,op,j,k in c if op=='&' and not S[i])
    m0c=sum(1 for i,op,j,k in c if op=='&' and not S[i] and i in creators)
    mc=len(creators)
    kil=sum(1 for i,op,j,k in c if op=='&' and (not S[j] or not S[k]))
    lnkA=sum((not S[j])+(not S[k]) for i,op,j,k in c if op=='&')
    B2=sum(1 for i,op,j,k in c if op=='|' and S[j] and S[k] and len(S[i])>=2)
    B1=sum(1 for i,op,j,k in c if op=='|' and S[j] and S[k] and len(S[i])==1)
    Z=sum(1 for i,op,j,k in c if op=='|' and (not S[j] or not S[k]))
    return dict(m=m,m0=m0,m0c=m0c,mc=mc,kil=kil,lnkA=lnkA,B2=B2,B1=B1,Z=Z,t=tauE(E),e=len(E))
if __name__=='__main__':
  cnt=collections.Counter(); ex={}
  for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    d=stats(n,E,c)
    tests={'B2>=E-m0c':d['B2']-(d['e']-d['m0c']),
           'B2>=E-mc':d['B2']-(d['e']-d['mc']),
           'Z>=m0-1-lnkA':d['Z']-(d['m0']-1-d['lnkA']),
           'Z+m-m0c>=t-1':d['Z']+d['m']-d['m0c']-(d['t']-1),
           'Z+m-m0>=t-1':d['Z']+d['m']-d['m0']-(d['t']-1),
           'mc>=t':d['mc']-d['t']}
    for t,v in tests.items():
        cnt[(t,X,min(v,3))]+=1
        if v<0: ex.setdefault(t,(fn.split('/')[-1],fmt(c)))
  for k,v in sorted(cnt.items()): print(k,v)
  for k,v in ex.items(): print(k,v)
