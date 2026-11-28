# refine.py C LEVELS_JSON -> child cases (one more level): lines name<TAB>levels
import sys, json
from lib import *
C=int(sys.argv[1]); LV=json.loads(sys.argv[2]); E=info(C)['E']
reps=[orbs[k][0] for orbs,k,op in LV if k>=0]
forb=set(); andforb=set()
for orbs,k,op in LV:
    for o in (orbs if k<0 else orbs[:k]):
        forb|=set(map(tuple,o))
    if k>=0 and op=='|': andforb|=set(map(tuple,orbs[k]))
so,_=stab_orbits(E,reps,reps)
out=[]
for k2,o in enumerate(so):
    if all(tuple(p) in forb for p in o): continue
    for op2 in '&|':
        if op2=='&' and all(tuple(p) in andforb for p in o): continue
        out.append(('%d%s'%(k2,'a' if op2=='&' else 'o'),LV+[[so,k2,op2]]))
out.append(('none',LV+[[so,-1,'&']]))
for nm,lv in out: print(nm+'\t'+json.dumps(lv,separators=(',',':')))
