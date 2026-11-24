import sys,itertools
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
def brute(E,cs):
    n=max(max(e) for e in E)+1; c=parse(cs)
    for bits in itertools.product((0,1),repeat=n):
        v=list(bits)+[0]*(len(c)+5); val={u:bits[u] for u in range(n)}
        for i,o,j,k in c: val[i]=val[j]&val[k] if o=='&' else val[j]|val[k]
        f=int(any(bits[a] and bits[b] for a,b in E))
        if val[c[-1][0]]!=f: return False
    return True
import graphs; E=graphs.EXTRA[sys.argv[2]] if len(sys.argv)>2 else graphs.EXTRA["Pet-v"]
cs=sys.argv[1]
g=Graph(E); c=parse(cs)
print('brute ok',brute(E,cs),'size',len(c),'Phi',g.P,'tau',g.t,'reduced',len(red(g,c))==len(c))
print('minimal ANDs',[(i,support(g,c,i)) for i in minimal_ands(c)])
r=evaluate(g,c)
print('good A/N/B:',[(x[0],x[1],x[2],x[3]) for x in r if x[4]])
for v in map(int,sys.argv[3].split(",")) if len(sys.argv)>3 else (7,2):
    print('at',v,[(x[0],x[2],x[3]) for x in r if x[1]==v], 'F',sum(1 for x in c if v in x[2:]))
