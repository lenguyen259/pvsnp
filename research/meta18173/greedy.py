import sys,random,json
from collections import Counter
from base import *
class C:
    def __init__(s): s.g=[];s.memo={}
    def gate(s,op,a,b=None):
        k=(op,)+((min(a,b),max(a,b)) if b is not None and op!='N' else (a,))
        if op!='N' and a==b: return a
        if k in s.memo:return s.memo[k]
        s.g.append((op,a,b));w=N+len(s.g)-1;s.memo[k]=w;return w
def build(seed,extract=True):
    rnd=random.Random(seed)
    c=C()
    T=[set(t) for t in terms]
    sig={}  # new signal -> wire
    for i in range(N):sig[i]=i
    nxt=N
    # AND pair extraction
    while extract:
        cnt=Counter()
        for t in T:
            l=sorted(t)
            for i in range(len(l)):
                for j in range(i+1,len(l)):cnt[(l[i],l[j])]+=1
        if not cnt:break
        m=max(cnt.values())
        if m<2:break
        cands=[p for p,v in cnt.items() if v==m]
        a,b=rnd.choice(cands)
        w=c.gate('A',sig[a],sig[b]);sig[nxt]=w
        for t in T:
            if a in t and b in t:t-= {a,b};t.add(nxt)
        nxt+=1
    memo={}
    def F(ts):
        ts=[frozenset(t) for t in ts]
        key=frozenset(ts)
        if key in memo:return memo[key]
        if any(len(t)==0 for t in ts):raise
        if len(ts)==1:
            l=sorted(ts[0]);w=sig[l[0]]
            for x in l[1:]:w=c.gate('A',w,sig[x])
            memo[key]=w;return w
        cnt=Counter(x for t in ts for x in t)
        x,m=max(cnt.items(),key=lambda kv:(kv[1],rnd.random()))
        if m>=2:
            with_=[t-{x} for t in ts if x in t];rest=[t for t in ts if x not in t]
            if any(len(t)==0 for t in with_):
                w=sig[x]
                if rest: w=c.gate('O',w,F(rest))  # absorption
                # actually terms w/o x remain: x covers all with-x terms
            else:
                w=c.gate('A',sig[x],F(with_))
                if rest:w=c.gate('O',w,F(rest))
        else:
            ws=[F([t]) for t in ts];w=ws[0]
            for y in ws[1:]:w=c.gate('O',w,y)
        memo[key]=w;return w
    out=c.gate('N',F(T))
    return c,out
def ev(c,out):
    v=list(X)
    for op,a,b in c.g:
        v.append(v[a]&v[b] if op=='A' else v[a]|v[b] if op=='O' else FULL^v[a])
    return v[out]
if __name__=="__main__":
    Tg=target();best=None
    for s in range(int(sys.argv[1])):
        c,o=build(s)
        if best is None or len(c.g)<len(best[0].g):
            assert ev(c,o)==Tg;best=(c,o);print(s,len(c.g),flush=True)
    json.dump({'gates':best[0].g,'out':best[1]},open('best_greedy.json','w'))
