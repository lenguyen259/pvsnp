"""Plateau BFS: from each stuck non-STAR-ALL minimum circuit, explore single-gate edits that keep
size <= Phi and #violating ANDs <= v0, up to depth D / cap nodes; success if viol drops."""
import pickle,collections,time,sys
from t2lib import *
from exch import nviol,edits
D=int(sys.argv[1]); CAP=int(sys.argv[2])
bad=pickle.load(open('exch_bad.pkl','rb'))
st=collections.Counter(); still=[]; dist=collections.Counter(); t0=time.time()
for E,s,v0 in bad:
    g=Graph(E); c0=renum(g.n,red(g,parse(s)))
    seen={tuple(c0)}; front=[c0]; found=None
    for d in range(1,D+1):
        nf=[]
        for c in front:
            for c2 in edits(g,c):
                if not ok(g,c2): continue
                r=renum(g.n,red(g,c2))
                if len(r)>len(c0): continue
                k=tuple(r)
                if k in seen: continue
                seen.add(k); v=nviol(g,r)
                if v<v0: found=d; break
                if v==v0: nf.append(r)
            if found or len(seen)>CAP: break
        if found or len(seen)>CAP: break
        front=nf
    if found: st['ok']+=1; dist[found]+=1
    else: st['stuck']+=1; still.append((E,s,v0,len(seen)))
print(dict(st),dict(dist),time.time()-t0)
for x in still[:10]: print('STILL',x)
pickle.dump(still,open('exch_still.pkl','wb'))
