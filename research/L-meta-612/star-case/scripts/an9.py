from cl import *
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        st=stars(n,E,c,G,rd)
        for S in st:
            if S['cat'] not in ('S2',) and not (S['cat']=='S1' and S['priv']!=S['T']): continue
            g=S['g']; a=S['a']
            shared=[t for t in S['T'] if any(r!=g and r not in S['T'] for r in rd[t])]
            def supp(t):
                if t<n: return {t}
                return supp(G[t][1])|supp(G[t][2])
            Ssup=set().union(*[supp(t) for t in shared])
            ok1=all((v,1) in good for v in Ssup)
            key=(fn,S['cat'],'B=N' if set(S['B'])==nbrs(E,a) else 'B!=N','allS1good' if ok1 else 'notallS1', 'a0' if (a,0) in good else 'a0bad','Sgood' if any(v in [a]+S['B'] for v,b in good) else 'RULESFAIL')
            cnt[key]+=1
            if not ok1 and cnt[key]<3: print(key,fmt(c),S,shared,Ssup,sorted(good))
for k,v in sorted(cnt.items()): print(k,v)
