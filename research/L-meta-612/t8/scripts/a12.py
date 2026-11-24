from lib8 import *
st=collections.Counter(); ex=collections.defaultdict(list); unc=[]
def cert_of(r): return r['kZ']>=1 and r['pen']==0 and (len(r['rest'])==0 or (r['singok'] and r['single']))
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c'])
    rs={v:DV2(g,c,v) for v in g.sup if g.Eminus({v})}
    if any(cert_of(r) for r in rs.values()): continue
    st['unc']+=1; st[d['g']]+=1; unc.append(d)
    why=collections.Counter()
    for v,r in rs.items():
        why['kZ0']+= r['kZ']==0; why['pen']+= r['pen']>0; why['singfail']+= (not r['singok']) and len(r['rest'])>0; why['multi']+= (not r['single'])
    for k in why: st['why_'+k]+=1 if why[k] else 0
    pays=[(nm,v) for nm,v,rho,need in g.options() if LR(g,c,rho)>=need]
    st['paidA']+=any(nm=='A' for nm,v in pays); st['paidB']+=any(nm=='B' for nm,v in pays); st['paidN']+=any(nm=='N' for nm,v in pays)
    if len(ex[d['g']])<1: ex[d['g']].append((d['c'],pays))
import json
json.dump(unc,open('unc157.json','w'))
print(dict(st))
for k,v in ex.items(): print(k,v)
