import sys, json, collections, time
from lib import *
from mcsat2 import exists_circuit as ec2
E=[tuple(e) for e in json.loads(sys.argv[1])]; X=int(sys.argv[2]); lim=int(sys.argv[3]); nostar=sys.argv[4]=='1'
n=max(max(e) for e in E)+1; P=phiE(E); t0=time.time()
need={(v,b):P-(phi0(E,v) if b==0 else phi1(E,v)) for v in range(n) for b in (0,1)}
circs=ec2(n,target_tt(n,E),P+X,enum_all=lim,nostar=nostar); st=collections.Counter()
for c in circs:
    s=len(c); mins=minimal_ands(n,c); V=set().union(*[A|B for g,A,B in mins])
    g1={vb for vb in need if s-restrict(n,c,*vb)>=need[vb]}
    st['L6']+=bool(g1); e1=any(v in V for v,b in g1); st['E*']+=e1
    if not e1:
        g2={vb for vb in need if s-restrict_plus(n,c,*vb)>=need[vb]}
        e2=any(v in V for v,b in g2); st['E*+']+=e2; st['L6+']+=bool(g2)
        if not e2: print('  E*+FAIL',fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(g2),flush=True)
print(n,len(E),'Phi',P,'X',X,'nostar',nostar,'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
