from t4 import *
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+[SC+'/nf/circs']):
    d=stats(n,E,c)
    tests={'B2>=E-mc':d['B2']-(d['e']-d['mc']),'Z+m-mc>=t-1':d['Z']+d['m']-d['mc']-(d['t']-1),
           'Am':d['m']-d['mc']+d['m0']-d['lnkA']-d['t']}
    for t,v in tests.items():
        cnt[(t,X,min(v,2))]+=1
        if v<0: ex.setdefault(t,[]).append((fn.split('/')[-1],fmt(c)))
for k,v in sorted(cnt.items()): print(k,v)
for k,v in ex.items(): print(k,len(v),v[:3])
