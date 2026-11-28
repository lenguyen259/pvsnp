import sys,random,json,itertools
from collections import Counter
from base import *
from greedy import C,ev
pairs=[(a,b) for a in range(6) for b in range(a+1,6)]
eid={p:i for i,p in enumerate(pairs)}
def E(a,b):return eid[(min(a,b),max(a,b))]
tris=[frozenset(E(a,b) for a,b in itertools.combinations(t,2)) for t in itertools.combinations(range(6),3)]
stars=[frozenset(E(h,v) for v in range(6) if v!=h) for h in range(6)]
def build(seed,usestars=True,usetris=True):
    rnd=random.Random(seed);c=C()
    T=[set(t) for t in terms]
    sig={i:i for i in range(N)};nxt=N
    base=(tris if usetris else [])+(stars if usestars else [])
    # substitute: for each term, repeatedly pick random base set contained in term
    for t in T:
        while True:
            opts=[b for b in base if b<=t]
            if not opts:break
            # prefer popular? random
            b=rnd.choice(opts)
            if b not in sig_of: sig_of[b]=None
            t-=b;t.add(('B',b))
    return T
# simpler: separate generic implementation
def run(seed,usestars,usetris,pr):
    rnd=random.Random(seed);c=C()
    base=[]
    if usetris:base+=tris
    if usestars:base+=stars
    T=[set(t) for t in terms]
    cache={}
    def bsig(b):
        l=sorted(b);w=l[0]
        for x in l[1:]:w=c.gate('A',w,x)
        return w
    for t in T:
        while True:
            opts=[b for b in base if b<=t]
            if not opts or rnd.random()>=pr:break
            b=rnd.choice(opts)
            t-=b
            if b not in cache:cache[b]=bsig(b)
            t.add(cache[b])
    while True:
        cnt=Counter()
        for t in T:
            l=sorted(t)
            for i in range(len(l)):
                for j in range(i+1,len(l)):cnt[(l[i],l[j])]+=1
        if not cnt:break
        m=max(cnt.values())
        if m<2:break
        a,b=rnd.choice(sorted(p for p,v in cnt.items() if v==m))
        w=c.gate('A',a,b)
        for t in T:
            if a in t and b in t:t-={a,b};t.add(w)
    memo={}
    def F(ts):
        ts=[frozenset(t) for t in ts];key=frozenset(ts)
        if key in memo:return memo[key]
        if len(ts)==1:
            l=sorted(ts[0]);w=l[0]
            for x in l[1:]:w=c.gate('A',w,x)
            memo[key]=w;return w
        cnt=Counter(x for t in ts for x in t)
        x,m=max(sorted(cnt.items()),key=lambda kv:(kv[1],rnd.random()))
        if m>=2:
            wi=[t-{x} for t in ts if x in t];rest=[t for t in ts if x not in t]
            if any(len(t)==0 for t in wi):w=x
            else:w=c.gate('A',x,F(wi))
            if rest:w=c.gate('O',w,F(rest))
        else:
            ws=[F([t]) for t in ts];w=ws[0]
            for y in ws[1:]:w=c.gate('O',w,y)
        memo[key]=w;return w
    return c,c.gate('N',F(T))
if __name__=="__main__":
    Tg=target();best=None
    for s in range(int(sys.argv[1])):
        for us,ut,pr in [(1,1,1),(1,0,1),(0,1,1),(1,1,.7)]:
            c,o=run(s,us,ut,pr)
            if best is None or len(c.g)<len(best[0].g):
                assert ev(c,o)==Tg;best=(c,o);print(s,us,ut,pr,len(c.g),flush=True)
    json.dump({'gates':best[0].g,'out':best[1]},open('best_greedy2.json','w'))
