import sys, collections, time
from lib import *
nmin,nmax,X,lim=map(int,sys.argv[1:5]); only=sys.argv[5] if len(sys.argv)>5 else None
for n,E in graphs(nmin,nmax):
    if only and str(E)!=only: continue
    P=phiE(E); t0=time.time()
    circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
    st=collections.Counter()
    for c in circs:
        good,sl=goodset(n,E,c); mins=minimal_ands(n,c)
        ok=any(v in A|B for g,A,B in mins for v,b in good); st['E*']+=ok
        for g,A,B in mins:
            if A&B or min(len(A),len(B))>1: continue
            st['star']+=1; gg=any(v in A|B for v,b in good); st['starS']+=gg
            if not gg: print('  RULE-S FAIL',fmt(c),sorted(A),sorted(B),sorted(good),flush=True)
        if not ok: print('  E*FAIL',fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(good),flush=True)
    print(n,len(E),'Phi',P,'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
