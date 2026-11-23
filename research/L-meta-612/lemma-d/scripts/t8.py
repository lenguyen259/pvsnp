import base,collections
L=base.get(); c=0
for d in L:
    if len(d['E'])!=5: continue
    chv={v:base.ch(d,v) for v in d['sup']}
    for v in d['sup']:
        if chv[v]!=1: continue
        g=[i for i in d['ors'] if v in d['chg'][i]][0]
        j,k=d['ors'][g]
        if v in (j,k):
            print('v',v,'g',g,{i:d['R'][i] for i in sorted(d['R'])},chv); c+=1
            break
    if c>6: break
