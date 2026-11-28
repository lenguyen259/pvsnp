"""T2-LT test: for every reduced C, is some A/N/B option paid by 'first-order + top' bound?
   bound(rho) = |K u Dup1 u Top| - 1 where K=const gates, Dup1 = first-order copies (dD or R-side), Top = gates = out|rho.
   Also test L1(N[v]) >= e(N[v]) for all v."""
import sys,random,collections,time; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
def firstorder_sets(g,c,rho):
    T=tables(g,c,rho); full=g.full
    K={i for i,o,j,k in c if T[i] in (0,full)}
    Kn=K|{u for u in range(g.n) if u in rho}
    cp={i for i,o,j,k in c if i not in K and (j in Kn or k in Kn)}
    return K,cp,T
def LT(g,c,rho):
    K,cp,T=firstorder_sets(g,c,rho); fo=T[c[-1][0]]
    Tp={i for i,o,j,k in c if T[i]==fo}
    return len(K|cp|Tp)-1, len(K|cp)
if __name__=='__main__':
    secs=float(sys.argv[1]); N=int(sys.argv[2]); seed=int(sys.argv[3])
    rnd=random.Random(seed); allc=list(load_cached()); rnd.shuffle(allc)
    st=collections.Counter(); t0=time.time(); fails=[]
    for fn,n,E,c in allc[:N]:
        if time.time()-t0>secs: break
        g=Graph(E,n); 
        if not any(len(g.N[v])>1 for v in g.sup) or len(g.sup)==max(len(g.N[v]) for v in g.sup)+1 and len(E)==max(len(g.N[v]) for v in g.sup): continue
        c=renum(n,red(g,c))
        st['circ']+=1; okLT=okLO=False
        for nm,v,rho,need in g.options():
            lt,lo=LT(g,c,rho)
            if lt>=need: okLT=True
            if lo>=need: okLO=True
            if nm=='N':
                X=g.N[v]|{v}; D,dD=Dsets(g,c,X); eN=sum(1 for e in g.E if e[0] in X or e[1] in X)
                st['Npairs']+=1
                if len(D|dD)>=eN: st['L1>=eN']+=1
                elif len(fails)<3: fails.append(('L1<eN',E,fmt(c),v,len(D|dD),eN))
        st['LT']+=okLT; st['LO']+=okLO
        if not okLT and len(fails)<8: fails.append(('LTfail',E,fmt(c)))
    print(dict(st)); [print(f) for f in fails]
