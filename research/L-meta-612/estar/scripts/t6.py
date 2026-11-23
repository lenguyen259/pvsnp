import sys, collections, time
from lib import *
def thmA(n,E,c):
    """gates where Theorem A applies (center a): F_a>=deg a, or F_a==1 and |T_p|>=|B|-1"""
    s=len(c); out=c[-1][0]
    readers=collections.defaultdict(list)
    for i,o,j,k in c: readers[j].append(i); readers[k].append(i)
    res=[]
    for g,A,B in minimal_ands(n,c):
        if A&B: continue
        for (X,Y) in ((A,B),(B,A)):
            if len(X)!=1: continue
            (a,)=X; d=len(nbrs(E,a)); F=len(readers[a])
            if F>=d: res.append((g,a,'fan')); continue
            if F==1:
                # T: OR gates below g's other input
                gi=[x for x in c if x[0]==g][0]; y=gi[2] if gi[3]==a else gi[3]
                T=set(); st=[y]
                while st:
                    x=st.pop()
                    if x>=n and x not in T: T.add(x); xi=[q for q in c if q[0]==x][0]; st+= [xi[2],xi[3]]
                # private: all readers in T or g (iterate)
                priv=set()
                changed=True
                while changed:
                    changed=False
                    for x in T-priv:
                        if all(r==g or r in priv for r in readers[x]): priv.add(x); changed=True
                if len(priv)>=len(Y)-1: res.append((g,a,'priv'))
    return res
nmin,nmax,X,lim=map(int,sys.argv[1:5])
for n,E in graphs(nmin,nmax):
    P=phiE(E); t0=time.time()
    circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim); st=collections.Counter()
    for c in circs:
        r=thmA(n,E,c); st['A']+=bool(r)
        good,_=goodset(n,E,c)
        for g,a,why in r: assert (a,0) in good, (fmt(c),a,why)
    print(n,len(E),'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
