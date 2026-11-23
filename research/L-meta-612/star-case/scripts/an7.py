from cl import *
from an5 import tts
cnt=collections.Counter(); shown=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]; Es={frozenset(e) for e in E}
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        ev=lambda t,S: (t>>sum(1<<u for u in S))&1
        geq=lambda p,q: (T[p]|T[q])==T[p]
        sing=lambda p: {u for u in range(n) if ev(T[p],[u])}
        for S in stars(n,E,c,G,rd):
            if S['cat']!='S1': continue
            a=S['a']; B=set(S['B']); g=S['g']
            others=[r for r in rd[a] if r!=g]
            orr=[r for r in others if G[r][0]=='|']
            key=['B1' if len(B)==1 else 'Bbig', 'priv' if S['priv']==S['T'] else 'shared']
            if len(orr)<len(others): key.append('ANDreader')
            ok=True; att={}
            for cc in sorted(nbrs(E,a)-B):
                wit=[]
                for i,o,j,k in c:
                    if o!='&': continue
                    for h1,h2 in ((j,k),(k,j)):
                        if ev(T[h2],[cc]) and not ev(T[h2],[a]) and not ev(T[h1],[cc]) and ev(T[h1],[a]):
                            for p in orr:
                                z=G[p][1] if G[p][2]==a else G[p][2]
                                if geq(h1,p) and any(frozenset((u,cc)) in Es for u in sing(z)): wit.append(p)
                if not wit: ok=False
                att[cc]=wit
            key.append('attOK' if ok else 'attFAIL')
            # injectivity check: exists SDR
            import itertools
            inj=any(len(set(ch))==len(ch) for ch in itertools.product(*att.values())) if ok and att else ok
            key.append('inj' if inj else 'noinj')
            key.append('a0good' if (a,0) in {vb for vb in need if len(dead[vb])>=need[vb]} else 'a0bad')
            key=tuple(key); cnt[key]+=1
            if shown[key]<int(sys.argv[1]) and 'attFAIL' in key and 'Bbig' in key: shown[key]+=1; print(fn,fmt(c),S,att)
for k,v in sorted(cnt.items()): print(k,v)
