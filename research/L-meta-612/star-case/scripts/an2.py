from cl import *
cnt=collections.Counter(); seen=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        byg=collections.defaultdict(list)
        for S in stars(n,E,c,G,rd): byg[S['g']].append(S)
        for g,L in byg.items():
            cats={S['cat'] for S in L}
            if cats&{'A1','A2'}: cnt['covered']+=1; continue
            cat='/'.join(sorted(cats)); cnt[cat]+=1
            V=set().union(*[{S['a']}|set(S['B']) for S in L])
            gs=sorted(vb for vb in good if vb[0] in V); cnt[cat+'_good']+=bool(gs)
            key=(fn,cat)
            if seen[key]<int(sys.argv[1]):
                seen[key]+=1
                for S in L:
                  print(fn,cat,fmt(c),'| g=%d a=%d B=%s F=%d deg=%d T=%s priv=%s'%(S['g'],S['a'],S['B'],S['F'],S['deg'],S['T'],S['priv']),'good',gs)
                  for v in [S['a']]+S['B']:
                    for b in (0,1): print('    ',(v,b),'need',need[(v,b)],'dead',sorted(dead[(v,b)]))
print(dict(cnt))
print(sorted(seen.items()))
