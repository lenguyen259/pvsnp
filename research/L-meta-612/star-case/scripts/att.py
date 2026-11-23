from cl import *
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        sing=lambda p: {u for u in range(n) if (T[p]>>(1<<u))&1}
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        st=stars(n,E,c,G,rd); covered={S['g'] for S in st if S['cat'] in ('A1','A2')}
        for S in st:
            a=S['a']; B=set(S['B']); g=S['g']; priv=S['priv']==S['T']
            orr=[r for r in rd[a] if G[r][0]=='|']
            zs={p:sing(G[p][1] if G[p][2]==a else G[p][2]) for p in orr}
            att=all(any(zs[p] and zs[p]<=nbrs(E,cc) for p in orr) for cc in nbrs(E,a)-B)
            thmB= priv and att
            if thmB: assert (a,0) in good, (fn,fmt(c),S)
            key=(S['cat'],'|B|=1' if len(B)==1 else '|B|>=2','priv' if priv else 'shared','ATT' if att else 'noATT','gatecovered' if g in covered else 'gateUNcov')
            cnt[key]+=1
for k,v in sorted(cnt.items()): print(k,v)
