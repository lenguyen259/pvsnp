# (1) local subadditivity of w(p)=|E_p|+|S_p|-1 (0 if both empty) at every gate; AND step only if rectangle edges form a forest
# (2) uncertified (full DV2) girth>=5 circuits: per-vertex failure reasons and witness types
from lib10 import *
from t2lib import sing, starall_viol
def isforest(edges):
    par={}
    def f(x):
        while par.get(x,x)!=x: x=par[x]
        return x
    for a,b in edges:
        ra,rb=f(a),f(b)
        if ra==rb: return False
        par[ra]=rb
    return True
st=collections.Counter(); ex={}
for src,g,c in corpus():
    T=tables(g,c,{}); S={u:frozenset([u]) for u in range(g.n)}; Ep={u:() for u in range(g.n)}
    for i,o,j,k in c:
        S[i]=sing(g,T,i)
        Ep[i]=tuple(e for e in g.E if e[0] not in S[i] and e[1] not in S[i] and (T[i]>>((1<<e[0])|(1<<e[1])))&1)
    w=lambda p: (len(Ep[p])+len(S[p])-1) if (Ep[p] or S[p]) else 0
    for i,o,j,k in c:
        if o=='|':
            st['or']+=1; st['or_viol']+= w(i)>w(j)+w(k)+1
        else:
            K=S[j]&S[k]; R=[e for e in g.E if (e[0] in S[j]-K and e[1] in S[k]-K) or (e[1] in S[j]-K and e[0] in S[k]-K)]
            fo=isforest(R); st['and',fo]+=1
            if w(i)>w(j)+w(k): st['and_viol',fo]+=1
    # uncertified analysis
    allr={}
    cert=False
    for v in g.sup:
        if not g.Eminus({v}): continue
        r=DV2(g,c,v); d=delta(g,v); carr=(len(r['rest'])==0 or (r['singok'] and r['single']))
        if carr and r['pen']<=r['kZ']-d: cert=True; break
        allr[v]=(r,d,carr)
    if cert: continue
    ex_=len(c)-g.P; st['unc',ex_]+=1
    reasons=collections.Counter()
    for v,(r,d,carr) in allr.items():
        if not carr: reasons['carrier']+=1
        elif r['pen']>0: reasons['pen']+=1
        else: reasons['kZ<delta']+=1
    for k_ in reasons: st['unc_has',k_]+=1
    st['unc_only_pen']+= set(reasons)=={'pen'}
    nv=starall_viol(g,c); st['unc_viol',tuple(sorted({t for i,t in nv}))]+=1
for k in sorted(st,key=str): print(k,st[k])
