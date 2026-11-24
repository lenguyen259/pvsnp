"""(1) what is Top made of; how often Top is needed (LO fails, LT pays)."""
from lib7 import *
import time
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); ex=[]
for src,d in pools():
    if time.time()-t0>secs: break
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1
    T0=tables(g,c,{}); f=g.f; gate={x[0]:x for x in c}
    okLO=okLT=False; payers=[]
    for nm,v,rho,need in g.options():
        K,cp,Tp,T=parts(g,c,rho)
        lo=len(K|cp); lt=len(K|cp|Tp)-1
        if lo>=need: okLO=True
        if lt>=need: okLT=True; payers.append((nm,v,need,lo,lt,K,cp,Tp,T))
    st['LO']+=okLO; st['LT']+=okLT
    if okLT and not okLO:
        st['topneeded']+=1
        for nm,v,need,lo,lt,K,cp,Tp,T in payers:
            st['pay_'+nm]+=1
            new=Tp-K-cp
            fH=T[c[-1][0]]
            for q in Tp:
                st['top_tot']+=1
                st['top_le_f']+= (T0[q]&~f&g.full)==0
                st['top_OR']+= gate[q][1]=='|'
                st['top_inCp']+= q in cp
            if len(ex)<4: ex.append((src,d['g'],nm,v,need,lo,lt,sorted(Tp),sorted(cp),d['c']))
print(dict(st))
for e in ex: print(e)
