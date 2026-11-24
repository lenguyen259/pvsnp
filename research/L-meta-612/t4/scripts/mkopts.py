import sys,itertools,json
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from graphs import G
def opts(E,extra=True):
    g=Graph(E); out={}
    def put(S0,S1):
        S0=tuple(sorted(S0)); S1=tuple(sorted(S1))
        if not S0 and not S1: return
        nd=gneed(g,S0,S1)
        if nd is None: return
        out[(S0,S1)]=nd
    for w in g.sup:
        put([w],[]); put([],[w]); put(sorted(g.N[w]|{w}),[])
        if len(g.N[w])==1: put(list(g.N[w]),[w])
    if extra:
        V=g.sup
        for r0 in range(0,4):
            for S0 in itertools.combinations(V,r0):
                for r1 in range(0,4):
                    for S1 in itertools.combinations([x for x in V if x not in S0],r1):
                        put(S0,S1)
    return g,out
if __name__=='__main__':
    g,o=opts(G(sys.argv[1]), extra=(len(sys.argv)>2))
    L=[[list(a),list(b),nd-1] for (a,b),nd in o.items()]
    assert all(x[2]>=0 for x in L), [x for x in L if x[2]<0]
    print(json.dumps(L))
