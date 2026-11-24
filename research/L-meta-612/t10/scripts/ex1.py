# local exchange on girth>=5 non-STAR-ALL circuits: (size,nviol) lexicographic single-gate edit
import sys,time,json
from lib10 import *
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from exch import nviol, edits
from t2lib import ok
def best(g,c):
    v0=nviol(g,c); s0=len(c)
    for c2 in edits(g,c):
        if not ok(g,c2): continue
        r=renum(g.n,red(g,c2))
        if len(r)<s0 or (len(r)==s0 and nviol(g,r)<v0): return r
    return None
st=collections.Counter(); stuck=[]; t0=time.time(); lim=float(sys.argv[1]); per=collections.Counter()
for src,g,c in corpus():
    if time.time()-t0>lim: break
    v0=nviol(g,c)
    if v0==0: continue
    key=(g.E,len(c)-g.P)
    if per[key]>=int(sys.argv[2]): continue
    per[key]+=1
    st[('nonSA',len(c)-g.P)]+=1
    r=best(g,c)
    if r is None: st[('stuck',len(c)-g.P)]+=1; stuck.append((g.E,fmt(c),len(c)-g.P,v0)); print('STUCK',stuck[-1],flush=True)
print(sorted(st.items()),time.time()-t0)
json.dump(stuck,open('ex1_stuck.json','w'))
