import sys,itertools
sys.path.insert(0,'../core')
from h1 import parse
n=int(sys.argv[1]); c=parse(open(sys.argv[2]).read().strip()); E=eval(sys.argv[3])
X=[sum(1<<r for r in range(1<<n) if (r>>u)&1) for u in range(n)]
T={u:X[u] for u in range(n)}
for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
Es={frozenset(e) for e in E}
def mins(t):
    out=[]
    for k in range(1,n+1):
        for S in itertools.combinations(range(n),k):
            r=sum(1<<u for u in S)
            if (t>>r)&1 and not any(set(m)<=set(S) for m in out): out.append(S)
        if len(out)>40: break
    return out
for i,o,j,k in c:
    m=mins(T[i])
    desc=[]
    for S in m:
        if len(S)==2: desc.append(''.join(map(str,S))+('' if frozenset(S) in Es else '!'))
        else: desc.append(''.join(map(str,S)))
    print(i,'=',j,o,k,':',' '.join(desc[:30]))
