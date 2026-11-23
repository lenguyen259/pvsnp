from cl import *
import itertools
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        for a in range(n):
            if not [e for e in E if a not in e]: continue
            Na=nbrs(E,a); e=len(dead[(a,0)])
            live={i for i,_,_,_ in c}-dead[(a,0)]
            orf={sum(1<<r for r in range(1<<n) if r & sum(1<<u for u in S)) : S for S in [set(x) for k in range(1,len(Na)+1) for x in itertools.combinations(sorted(Na),k)]} if Na else {}
            best=0
            for i in live:
                # function of i in restricted circuit = T[i] with x_a=0: compare on rows with bit a = 0
                mask=sum(1<<r for r in range(1<<n) if not (r>>a)&1)
                for f,S in orf.items():
                    if (T[i]&mask)==(f&mask): best=max(best,len(S))
            if best:
                cnt['checked']+=1
                assert e<=2+len(Na)-best,(fn,fmt(c),a,e,best)
                if e<need[(a,0)] and 2+len(Na)-best<need[(a,0)]: cnt['L5 explains failure']+=1
print(dict(cnt))
