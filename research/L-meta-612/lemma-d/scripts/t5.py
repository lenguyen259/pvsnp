import base,collections
L=base.get(); H=collections.Counter()
for d in L:
    if len(d['E'])!=7: continue
    chv=tuple(base.ch(d,v) for v in d['sup'])
    H[chv,d['X']]+=1
for k in sorted(H): print(k,H[k])
