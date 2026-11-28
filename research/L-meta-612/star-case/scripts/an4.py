from cl import *
cnt=collections.Counter(); shown=0
for fn in sorted(glob.glob('circs/*.json')):
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c)
        for S in stars(n,E,c,G,rd):
            if S['cat'] not in ('S1',): continue
            a=S['a']; g=S['g']; B=set(S['B'])
            rg=len(rd[g]); P=len(S['priv']); F=S['F']; d=S['deg']; dl=need[(a,0)]-d
            Na=nbrs(E,a); extra=len(dead[(a,0)])-F-rg-P
            simple = F+rg+P >= d+dl
            key=(F,rg,P,len(B),d,dl,len(Na-B),len(B-Na),simple)
            cnt[key]+=1
            if not simple and shown<int(sys.argv[1]):
                shown+=1; print(fn,fmt(c),S,'dead',sorted(dead[(a,0)]),'need',need[(a,0)])
for k,v in sorted(cnt.items()): print('F rg P |B| deg delta |N-B| |B-N| simpleOK',k,v)
