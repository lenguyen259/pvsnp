from cl import *
cnt=collections.Counter(); shown=collections.Counter()
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        st=stars(n,E,c,G,rd); mins=minimal_ands(n,c)
        cats=collections.Counter(S['cat'] for S in st)
        if cats['A1'] or cats['A2']: cnt['Acov']+=1; continue
        typ=tuple(sorted(('ovl' if A&B else 'star' if min(len(A),len(B))==1 else 'rect') for g,A,B in mins))
        key=(fn,typ,tuple(sorted(cats.items())))
        cnt[key]+=1
        if shown[key]<int(sys.argv[1]):
            shown[key]+=1; good={vb for vb in need if len(dead[vb])>=need[vb]}
            print(key,fmt(c),[(S['g'],S['a'],S['B'],S['F'],S['deg'],S['T'],S['priv']) for S in st],sorted(good))
for k,v in sorted(cnt.items(),key=str): print(k,v)
