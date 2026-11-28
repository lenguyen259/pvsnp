"""(i) structure lemma check for deg-3 ends; (ii) candidate: some w in N[a]uN[b] with N(w) good; some w in N(a)uN(b)-{a,b}."""
import sys,collections; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
st=collections.Counter(); ex=collections.defaultdict(list)
def Nopt(g,c,w):
    X=g.N[w]|{w}; H=g.Eminus(X)
    if not H: return None
    return elim(g,c,{x:0 for x in X})>=g.P-phi(H)
for d in load(sys.argv[1:]):
    g=Graph(d['E']); c=parse(d['c']); RD=readers(c)
    for rec in d['rec']:
        i,a,b=rec[:3]; st['inst']+=1
        for v,u in ((a,b),(b,a)):
            if len(g.N[v])==3:
                st['deg3']+=1
                rd=[x for x in c if v in x[2:]]; kand=sum(1 for x in rd if x[1]=='&')
                rg=[x for x in c if i in x[2:]]
                dv=g.t-tau(g.Eminus({v}))
                ok=(len(rd)==2 and kand==1 and len(rg)==1 and rg[0][1]=='|' and elim(g,c,{v:0})==3 and dv==1)
                st['struct_ok']+=ok
                if not ok: ex['struct'].append((d['g'],d['c'],v))
        pa=[x[0] for x in c if a in x[2:] and x[0]!=i]; pb=[x[0] for x in c if b in x[2:] and x[0]!=i]
        if set(pa)&set(pb): st['shared_p']+=1; ex['shared'].append((d['g'],d['c']))
        W1=(g.N[a]|g.N[b])-{a,b}
        r1=any(Nopt(g,c,w) for w in W1); st['N(w),w in N(a)uN(b)-ab']+=r1
        r0=any(Nopt(g,c,w) for w in (a,b)); st['N(a)orN(b)']+=r0
        if not r1: ex['W1'].append((d['g'],d['s'],d['c'],a,b))
        if not (r0 or r1): ex['W'].append((d['g'],d['s'],d['c'],a,b))
        st['N[a]uN[b] some']+= (r0 or r1)
print(dict(st))
for k,v in ex.items(): print(k,len(v),v[:2])
