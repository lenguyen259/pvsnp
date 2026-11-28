from cl import *
import itertools
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]; Es={frozenset(e) for e in E}
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        sing=lambda p: {u for u in range(n) if (T[p]>>(1<<u))&1}
        for S in stars(n,E,c,G,rd):
            if S['cat']!='S2': continue
            g=S['g']
            for t in S['T']:
                for q in rd[t]:
                    if q==g or q in S['T']: continue
                    # walk OR chains (all paths) to first ANDs
                    st=[(t,q)]
                    while st:
                        prev,x=st.pop()
                        if G[x][0]=='|': st+=[(x,r) for r in rd[x]]; continue
                        w=G[x][1] if G[x][2]==prev else G[x][2]
                        sr,sw=sing(prev),sing(w)
                        junk=any(frozenset((u,v)) not in Es for u in sr-sw for v in sw-sr)
                        kind='singleton' if sr&sw else ('junkpair' if junk else ('sing(w)=0' if not sw else 'IMPOSSIBLE'))
                        cnt[kind]+=1
print(dict(cnt))
