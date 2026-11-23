from cl import *
cnt=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        byg=collections.defaultdict(list)
        for S in stars(n,E,c,G,rd): byg[S['g']].append(S)
        for g,L in byg.items():
            cats={S['cat'] for S in L}
            if cats&{'A1','A2'}: continue
            for S in L:
                a=S['a']; cat=S['cat']
                key=cat+('_B1' if len(S['B'])==1 else '_Bbig')
                cnt[key]+=1; ok=(a,0) in good; cnt[key+'_a0']+=ok
                if not ok and '-p' in sys.argv:
                    print(fn,key,fmt(c),'| g=%d a=%d B=%s F=%d deg=%d T=%s priv=%s'%(S['g'],S['a'],S['B'],S['F'],S['deg'],S['T'],S['priv']),'need',need[(a,0)],'dead',sorted(dead[(a,0)]),'good',sorted(vb for vb in good if vb[0] in [a]+S['B']))
print(dict(cnt))
