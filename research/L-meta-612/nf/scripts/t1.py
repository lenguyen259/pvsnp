from base import *
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+sys.argv[1:]):
    T=tts(n,c); S=sing(n,T)
    m=sum(1 for x in c if x[1]=='&')
    B2=sum(1 for i,o,j,k in c if o=='|' and S[j] and S[k] and len(S[i])>=2)
    B1=sum(1 for i,o,j,k in c if o=='|' and S[j] and S[k] and len(S[i])==1)
    Z=sum(1 for i,o,j,k in c if o=='|' and (not S[j] or not S[k]))
    t=tauE(E)
    key=(X,m-t,B2-(len(E)-m),Z-(m-1),B1)
    cnt[key]+=1; ex.setdefault(key,(fn,fmt(c)))
for k,v in sorted(cnt.items()): print(k,v, ex[k] if min(k[1:4])<0 else '')
