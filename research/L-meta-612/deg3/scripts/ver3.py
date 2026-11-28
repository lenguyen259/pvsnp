import sys,itertools,json
from chk import parse
from lib import red,cnt,tau,phi
for line in open('found.txt'):
    nm,tg,rest=line.split(' ',2); Es,cs=rest.split(' | ',1); E=[tuple(e) for e in json.loads(Es)]; c=parse(cs.strip())
    n=max(max(e) for e in E)+1
    R,T,o=red(n,c); full=sum(1<<r for r in range(1<<n) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
    a0,o0=cnt(R); t=tau(E)
    N={v:{b for a,b in E if a==v}|{a for a,b in E if b==v} for v in range(n)}
    def s(X):
        R1,_,_=red(n,c,{x:0 for x in X}); a1,o1=cnt(R1); return o0-o1,a0-a1
    def need(X):
        EX=[e for e in E if e[0] not in X and e[1] not in X]; e=len(E)-len(EX)
        return e-(0 if EX else 1), t-(tau(EX) if EX else 0), bool(EX)
    sing=[(v,s([v]),need([v])) for v in range(n)]
    print(nm,tg,'correct',T[o]==full,'size',len(R),'#AND',a0,'tau',t,'#OR',o0,'|E|',len(E),'Phi',phi(E))
    if tg=='OR':
        print('  single OR-good:',[v for v,sv,nd in sing if sv[0]>=nd[0]])
        pr=[X for X in itertools.combinations(range(n),2) if s(X)[0]>=need(X)[0] and need(X)[2]]
        print('  OR-good pairs:',len(pr),pr[:8])
        print('  OR-good N(v):',[v for v in range(n) if s(N[v])[0]>=need(N[v])[0] and need(N[v])[2]])
    else:
        print('  single AND-good:',[v for v,sv,nd in sing if sv[1]>=nd[1]])
        pr=[X for X in itertools.combinations(range(n),2) if s(X)[1]>=need(X)[1] and need(X)[2]]
        print('  AND-good pairs:',pr[:10])
        print('  AND-good N(v) (G-N(v) has edge):',[v for v in range(n) if s(N[v])[1]>=need(N[v])[1] and need(N[v])[2]])
