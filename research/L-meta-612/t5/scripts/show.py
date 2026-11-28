import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
def dnf(g,t):
    # minimal monomials
    n=g.n; ms=[]
    for r in range(1<<n):
        if (t>>r)&1 and not any((r&m)==m for m in ms):
            # check minimal: r is true; minimal if no proper submask true
            if all(not (t>>(r&~(1<<u)))&1 for u in range(n) if (r>>u)&1):
                ms.append(r)
    ms=[m for m in ms if not any(m2!=m and (m2&m)==m2 for m2 in ms)]
    return '|'.join(''.join(str(u) for u in range(n) if (m>>u)&1) for m in sorted(ms,key=lambda m:(bin(m).count('1'),m))) or '0'
def show(E,cs,a):
    g=Graph(E); c=parse(cs); X=g.N[a]|{a}; rho={x:0 for x in X}
    T=tables(g,c,{}); T2=tables(g,c,rho); D,dD=Dsets(g,c,X)
    r=red(g,c,rho); keep={x[0] for x in r}
    print('X=',sorted(X),'need',g.P-phi(g.Eminus(X)),'elim',elim(g,c,rho))
    for i,o,j,k in c:
        tag='D ' if i in D else ('dD' if i in dD else ('  '))
        print('%3d=%2d%s%-3d %s %-28s -> %-14s %s'%(i,j,o,k,tag,dnf(g,T[i]),dnf(g,T2[i]),'SURV' if i in keep else ''))
if __name__=='__main__':
    show(eval(sys.argv[1]),sys.argv[2],int(sys.argv[3]))
