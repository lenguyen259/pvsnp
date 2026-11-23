import sys, json, collections, time
from lib import *
from mcsat2 import exists_circuit as ec2
E=[tuple(e) for e in json.loads(sys.argv[1])]; X=int(sys.argv[2]); lim=int(sys.argv[3]); nostar=sys.argv[4]=='1'
n=max(max(e) for e in E)+1; P=phiE(E); t0=time.time()
circs=ec2(n,target_tt(n,E),P+X,enum_all=lim,nostar=nostar)
st=collections.Counter()
for c in circs:
    good,sl=goodset(n,E,c); mins=minimal_ands(n,c)
    ok=any(v in A|B for g,A,B in mins for v,b in good); st['E*']+=ok; st['L6']+=bool(good)
    if not good: print('  L6FAIL',fmt(c),flush=True)
    for g,A,B in mins:
        if A&B or min(len(A),len(B))>1: continue
        st['star']+=1; gg=any(v in A|B for v,b in good); st['starS']+=gg
        if not gg: print('  RULE-S FAIL',fmt(c),sorted(A),sorted(B),sorted(good),flush=True)
    if not ok: print('  E*FAIL',fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(good),flush=True)
print(n,len(E),'Phi',P,'X',X,'nostar',nostar,'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
