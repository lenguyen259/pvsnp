from base import *
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    T=tts(n,c); S=sing(n,T)
    pure=lambda p,u,v: (T[p]>>((1<<u)|(1<<v)))&1 and u not in S[p] and v not in S[p]
    cre=set()
    for i,op,j,k in c:
        if op=='&' and not S[i]:
            if any(pure(i,u,v) and not pure(j,u,v) and not pure(k,u,v) for u,v in E): cre.add(i)
    m=sum(1 for x in c if x[1]=='&'); m0=sum(1 for i,op,j,k in c if op=='&' and not S[i])
    lnkA=sum((not S[j])+(not S[k]) for i,op,j,k in c if op=='&')
    B2=sum(1 for i,op,j,k in c if op=='|' and S[j] and S[k] and len(S[i])>=2)
    t=tauE(E); e=len(E)
    for nm,v in (('B*',B2-(e-len(cre))),('A**',m-len(cre)+m0-lnkA-t)):
        cnt[(nm,X,min(v,2))]+=1
        if v<0: ex.setdefault(nm,(fn.split('/')[-1],fmt(c)))
for k,v in sorted(cnt.items()): print(k,v)
for k,v in ex.items(): print(k,v)
