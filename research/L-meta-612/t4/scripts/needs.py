import sys,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
# guaranteed gadget elims (min over star/ORp), keyed (state_v,state_u); states: f(ree),0,1
GU={('1','f'):2,('1','0'):3,('0','f'):1,('0','0'):2,('f','0'):1,('f','f'):0}
def best(n,S):
    E,L=psun(n,S); g=Graph(E); P=list(L); res=[]
    cyc=list(range(n))
    for S1 in itertools.chain.from_iterable(itertools.combinations(P,r) for r in range(len(P)+1)):
        for S0c in itertools.chain.from_iterable(itertools.combinations(cyc,r) for r in range(n+1)):
            for S0p in itertools.chain.from_iterable(itertools.combinations([p for p in P if p not in S1],r) for r in range(len(P)+1)):
                S0=set(S0c)|set(S0p)
                nd=gneed(g,S0,S1)
                if nd is None: continue
                gu=0
                for v,u in L.items():
                    sv='1' if v in S1 else ('0' if v in S0 else 'f')
                    su='0' if u in S0 else 'f'
                    gu+=GU[(sv,su)]
                res.append((nd-gu,nd,sorted(S0),list(S1)))
    res.sort(); return res[:3]
for n,S in [(3,(0,1,2)),(5,(0,1,2)),(6,(0,1)),(6,(0,3)),(5,(0,1,2,3,4)),(6,(0,1,2,3)),(7,(0,1,2)),(7,(0,1,4)),(6,tuple(range(6))),(7,(0,1,2,3,4))]:
    print(n,S,best(n,S))
