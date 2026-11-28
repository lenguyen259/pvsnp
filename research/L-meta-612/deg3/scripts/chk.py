import sys,itertools,collections
from lib import *
def parse(s):
    c=[]
    for t in s.split():
        i,rest=t.split('='); o='&' if '&' in rest else '|'; j,k=rest.split(o); c.append((int(i),o,int(j),int(k)))
    return c
def info(n,E,c,sets=None,show=True):
    R,T,o=red(n,c)
    full=sum(1<<r for r in range(1<<n) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
    assert T[o]==full,'wrong'
    a0,o0=cnt(R)
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    res={}
    for v in sup:
        R1,_,_=red(n,c,{v:0}); a1,o1=cnt(R1)
        Ev=[e for e in E if v not in e]
        res[v]=dict(deg=deg[v],sor=o0-o1,sand=a0-a1,needP=phi(E)-phi(Ev),dtau=tau(E)-(tau(Ev) if Ev else 0))
    out=dict(size=len(R),nor=o0,nand=a0,phi=phi(E),E=len(E),tau=tau(E))
    if sets:
        for X in sets:
            R1,_,_=red(n,c,{x:0 for x in X}); e=sum(1 for a,b in E if a in X or b in X)
            out[tuple(X)]=(o0-cnt(R1)[1], e-(1 if e==len(E) else 0))
    if show:
        print(out)
        for v in res: print(' ',v,res[v])
    return out,res
if __name__=='__main__':
    E=[(0,1),(0,5),(2,3),(3,4),(4,5),(2,6),(1,6)]
    c=parse('6=0&1 7=5|6 8=0&7 9=4|8 10=2|9 11=3&10 12=7&9 13=11|12')
    # rename gates: var 6 used; shift gates by +1
    c=[(i+1,o,j+1 if j>=6 else j,k+1 if k>=6 else k) for i,o,j,k in c]
    m=c[-1][0]
    c+= [(m+1,'|',1,2),(m+2,'&',6,m+1),(m+3,'|',m,m+2)]
    info(8 if False else 7,E,c,sets=[[4,5]])
