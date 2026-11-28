from cl import *
def tts(n,c):
    T={}
    for u in range(n): T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
cnt=collections.Counter(); shown=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        ev=lambda t,S: (t>>sum(1<<u for u in S))&1
        for S in stars(n,E,c,G,rd):
            if S['cat']!='S1': continue
            a=S['a']; B=set(S['B'])
            for cc in sorted(nbrs(E,a)-B):
                # first gate creating a,cc
                for i,o,j,k in c:
                    if ev(T[i],[a,cc]) and not ev(T[i],[a]) and not ev(T[i],[cc]): break
                assert o=='&'
                h1,h2=(j,k) if ev(T[j],[a]) else (k,j)
                desc=('x_a' if h1==a else ('reader:'+G[h1][0]+('inp' if min(G[h1][1:])<n else 'gate') if a in G[h1][1:] else 'deep'))
                key=(desc, 'h1sing=%s'%sorted(u for u in range(n) if ev(T[h1],[u])), 'deadh=%d'%(i in dead[(a,0)]))
                cnt[desc]+=1
                if shown[desc]<3: shown[desc]+=1; print(fn,fmt(c),'a=%d B=%s c=%d gate %d=%d%s%d'%(a,sorted(B),cc,i,j,o,k),key)
print(cnt)
