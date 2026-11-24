import sys,itertools
sys.path.insert(0,'../core')
from h1 import red, parse
from lib import tau,phi
def run(E,n,c):
    R,T=red(n,c); A0=sum(1 for g in R.values() if g[0]=='&'); S0=len(R)
    N={v:{b for a,b in E if a==v}|{a for a,b in E if b==v} for v in range(n)}
    t=tau(E); P=phi(E)
    def rest(rho):
        R1,_=red(n,c,rho); return A0-sum(1 for g in R1.values() if g[0]=='&'), S0-len(R1)
    out=[]
    for k in (1,2):
        for X in itertools.combinations(range(n),k):
            EX=[e for e in E if e[0] not in X and e[1] not in X]
            sa,st=rest({x:0 for x in X})
            out.append(('zero',X,sa,t-(tau(EX) if EX else 0),st,P-phi(EX)))
    for v in range(n):
        EX=[e for e in E if e[0] not in N[v]|{v} and e[1] not in N[v]|{v}]
        sa,st=rest({v:1,**{u:0 for u in N[v]}})
        out.append(('v1N0',v,sa,t-(tau(EX) if EX else 0),st,P-phi(EX)))
    return out
E=[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)]; n=6
c=parse('6=2|4 7=5|2 8=1|0 9=3|5 10=6&8 11=3|10 12=11&7 13=4|12 14=0|12 15=9&13 16=1|2 17=14&16 18=17|15')
for r in run(E,n,c):
    flag=('ANDok' if r[2]>=r[3] else '')+(' TOTok' if r[4]>=r[5] else '')
    print(r,flag)
