from t4 import *
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    d=stats(n,E,c)
    T=tts(n,c); S=sing(n,T)
    a2=sum(1 for i,op,j,k in c if op=='&' and not S[j] and not S[k])
    tests={'A*':d['m']-d['m0c']+d['m0']-d['lnkA']-d['t'], 'm-a2>=t':d['m']-a2-d['t'],'a2':-a2}
    for t,v in tests.items():
        cnt[(t,X,min(v,3))]+=1
        if v<0: ex.setdefault(t,(fn.split('/')[-1],fmt(c)))
for k,v in sorted(cnt.items()): print(k,v)
for k,v in ex.items(): print(k,v)
