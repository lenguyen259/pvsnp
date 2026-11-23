from cl import *
cnt=collections.Counter(); 
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        for S in stars(n,E,c,G,rd):
            cat=S['cat']; cnt[cat]+=1
            V=[S['a']]+S['B']; gs=sorted(vb for vb in good if vb[0] in V)
            ag=(S['a'],0) in good
            cnt[cat+'_a0good']+=ag; cnt[cat+'_Sgood']+=bool(gs)
            if cat in('S1','S2') and (not ag or '-v' in sys.argv):
                print(fn,cat,fmt(c),'g=%d a=%d B=%s F=%d deg=%d T=%s priv=%s'%(S['g'],S['a'],S['B'],S['F'],S['deg'],S['T'],S['priv']),'good',gs,
                  'a0 dead',sorted(dead[(S['a'],0)]),'need',need[(S['a'],0)])
print(dict(cnt))
