# test pen-free DV2 bound on girth>=5: LD_A(c) >= kZ+kL+|ND|
from lib10 import *
st=collections.Counter(); bad=[]
for src,g,c in corpus():
    st[src]+=1
    for v in g.sup:
        if not g.Eminus({v}): continue
        r=DV2(g,c,v)
        b0=r['kZ']+r['kL']+len(r['ND'])
        st['A']+=1; st['pen>0']+=r['pen']>0
        if r['LD']<b0:
            st['viol']+=1
            if len(bad)<5 or len(fmt(c).split())<len(bad[0][1].split()): bad.append((g.E,fmt(c),v,r['pen'],r['LD'],b0,len(c)-g.P))
print(dict(st)); bad.sort(key=lambda x:len(x[1])); [print(b) for b in bad[:6]]
