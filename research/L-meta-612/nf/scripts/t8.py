from t4 import *
cnt=collections.Counter()
for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    T=tts(n,c); S=sing(n,T); ES={frozenset(e) for e in E}
    clean=all(frozenset((u,v)) in ES for i,op,j,k in c if op=='&' for u in S[j]-S[k] for v in S[k]-S[j])
    n1=not any(S[j]&S[k] for i,op,j,k in c if op=='&')
    d=stats(n,E,c)
    if clean:
        cnt[('clean: mc>=tau',d['mc']>=d['t'])]+=1
        cnt[('clean: B2+Z>=E-1',d['B2']+d['Z']>=d['e']-1)]+=1
    if clean and n1:
        cnt[('S2: B2>=E-mc',d['B2']>=d['e']-d['mc'])]+=1
        cnt[('S2: Z>=m-1-lnkA',d['Z']>=d['m']-1-d['lnkA'])]+=1
        cnt[('S2 class',X)]+=1
for k,v in sorted(cnt.items(),key=str): print(k,v)
