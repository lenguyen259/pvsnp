import json,sys,subprocess
from lib6 import *
def facts(n0,Sh,cs):
    E,L=psun(n0,Sh); g=Graph(E); P=sorted(L); c=parse(cs); T=tables(g,c,{})
    NB=g.N; res={}
    rd=lambda x:[y for y in c if x in y[2:]]
    gv={}; 
    for v in P:
        gg=rd(v)[0]; z=gg[2] if gg[3]==v else gg[3]; q=rd(gg[0])[0]; y=q[2] if q[3]==gg[0] else q[3]; gv[v]=(z,y)
    res['holder']=all(len(rd(L[v]))==1 and gv[v][0]!=L[v] for v in P)
    ok=True
    for w in range(n0):
        if w in L.values(): continue
        r=rd(w); ka=sum(1 for x in r if x[1]=='&'); ko=len(r)-ka; nb=gneed(g,[],[w])
        if len(r)+min(ka,2)>2 or len(r)+min(ko,2)>nb-1: ok=False
    res['run']=ok
    res['lb']=all(not (T[gv[v][0]]>>(1<<L[v]))&1 and (T[gv[v][1]]>>(1<<L[v]))&1 for v in P)
    ok=True
    def fG(r): return any((r>>a)&1 and (r>>b)&1 for a,b in E)
    for v in P:
        u=L[v]; V=[x for x in range(g.n) if x not in NB[u] and x!=u]
        for mask in range(1<<len(V)):
            r=sum(1<<V[i] for i in range(len(V)) if (mask>>i)&1)
            if not fG(r) and (T[gv[v][0]]>>r)&1: ok=False
    res['zr']=ok
    return res
if __name__=='__main__':
    n0=int(sys.argv[1]); Sh=[int(x) for x in sys.argv[2].split(',')]; L=json.load(open(sys.argv[3]))
    import collections; st=collections.Counter()
    for s_,cs in L[:int(sys.argv[4])]:
        F=facts(n0,Sh,cs); fl=['--no'+k for k in ('holder','run','lb','zr') if not F[k]]
        E,_=psun(n0,Sh); g=Graph(E)
        out=subprocess.run(['python3','enc6.py',str(n0),sys.argv[2],'--s',str(len(parse(cs))),'--nocanon','--timeout','60','--fix',cs]+fl,capture_output=True,text=True).stdout.strip().split('\n')[-1]
        st[(tuple(sorted(k for k in F if F[k])),out.split()[1])]+=1
    print(st)
