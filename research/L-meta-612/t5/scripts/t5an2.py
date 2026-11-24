import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
def allopts(g,c):
    out=[]
    V=g.sup
    cand=set()
    for v in V:
        cand.add((frozenset([v]),frozenset())); cand.add((frozenset(),frozenset([v])))
        cand.add((frozenset(g.N[v]|{v}),frozenset()))
        cand.add((frozenset(g.N[v]),frozenset([v])))
        for u in V:
            if u!=v: cand.add((frozenset([u,v]),frozenset()))
            if u!=v and u not in g.N[v]: cand.add((frozenset([u]),frozenset([v])))
    for S0,S1 in cand:
        nd=gneed(g,S0,S1)
        if nd is None: continue
        rho={x:0 for x in S0}; rho.update({x:1 for x in S1})
        e=elim(g,c,rho); eR=len(c)-len(ruleR(g,c,rho))
        out.append((tuple(sorted(S0)),tuple(sorted(S1)),e,eR,nd))
    return out
if __name__=='__main__':
    files=sys.argv[1:]
    for d in load(files):
        g=Graph(d['E']); c=parse(d['c'])
        o=allopts(g,c)
        good=[x for x in o if x[2]>=x[4]]; goodR=[x for x in o if x[3]>=x[4]]
        a,b=d['rec'][0][1:3]
        print(d['g'],'s=+%d'%d['s'],'ab=',a,b,'#good',len(good),'#goodR',len(goodR))
        print('   goodR:',sorted(goodR,key=lambda x:(len(x[0])+len(x[1]),x))[:12])
