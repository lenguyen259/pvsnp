# print case list: lines "name<TAB>orbs-json" for level-2 split under first-level case (k,op)
import sys, json
from lib import *
C=int(sys.argv[1]); k=int(sys.argv[2]); op=sys.argv[3]
E=info(C)['E']; o1=pair_orbits(E); p0=o1[k][0]
L1=[o1,k,op]
so,_=stab_orbits(E,[p0],[p0])
# drop stab-orbits entirely contained in forbidden first-level orbits
forb=set(tuple(p) for oo in o1[:k] for p in oo)
cases=[]
for k2,o in enumerate(so):
    if all(tuple(p) in forb for p in o): continue
    for op2 in '&|':
        if op2=='&' and op=='|' and all(tuple(p) in set(map(tuple,o1[k])) for p in o): continue  # AND forbidden there
        cases.append(('L2_%d%s'%(k2,'a' if op2=='&' else 'o'),[L1,[so,k2,op2]]))
cases.append(('L2_none',[L1,[so,-1,'&']]))
for nm,lv in cases: print(nm+'\t'+json.dumps(lv,separators=(',',':')))
