import sys, collections, time
from lib import *
from mcsat2 import exists_circuit as ec2
nmin,nmax,X,lim=map(int,sys.argv[1:5])
for n,E in graphs(nmin,nmax):
    P=phiE(E); t0=time.time()
    circs=ec2(n,target_tt(n,E),P+X,enum_all=lim,nostar=True)
    st=collections.Counter()
    for c in circs:
        good,sl=goodset(n,E,c); mins=minimal_ands(n,c)
        assert all(min(len(A),len(B))>=2 or A&B for g,A,B in mins), (fmt(c),mins)
        ok=any(v in A|B for g,A,B in mins for v,b in good); st['E*']+=ok; st['L6']+=bool(good)
        if not ok: print('  E*FAIL',fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(good),{k:v for k,v in sl.items() if v>-2},flush=True)
    print(n,len(E),'Phi',P,'#nostar',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
