from cl import *
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        sing=lambda p: {u for u in range(n) if (T[p]>>(1<<u))&1}
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        st=stars(n,E,c,G,rd)
        for S in st:
            if S['cat']!='S1' or len(S['B'])<2: continue
            a=S['a']; B=set(S['B'])
            orr=[r for r in rd[a] if G[r][0]=='|']
            zs={p:sing(G[p][1] if G[p][2]==a else G[p][2]) for p in orr}
            att=all(any(zs[p] and zs[p]<=nbrs(E,cc) for p in orr) for cc in nbrs(E,a)-B)
            if att: continue
            key=(fn,(a,0) in good, any(v in [a]+S['B'] for v,b in good)); cnt[key]+=1
            if cnt[key]<=2: print(key,fmt(c),S,{p:sorted(z) for p,z in zs.items()},'N(a)',sorted(nbrs(E,a)),'need',need[(a,0)],'dead',sorted(dead[(a,0)]),'good',sorted(good))
print(cnt)
