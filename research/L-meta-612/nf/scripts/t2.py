from base import *
cnt=collections.Counter(); ex={}
for fn,n,E,X,g5,c in load(DIRS+sys.argv[1:]):
    T=tts(n,c); S=sing(n,T); ES={frozenset(e) for e in E}
    f=set()
    for i,o,j,k in c:
        if o=='&':
            A,B=S[j],S[k]
            if A&B: f.add('N1')
            if not A or not B: f.add('N2')
            elif not (A-B) or not (B-A): f.add('deg')
            if any(frozenset((u,v)) not in ES for u in A-B for v in B-A): f.add('N3')
    key=(X,tuple(sorted(f))); cnt[key]+=1; ex.setdefault(key,[]).append((fn.split('/')[-1],fmt(c)))
for k,v in sorted(cnt.items()):
    print(k,v)
    for e in ex[k][:3]: print('   ',e)
