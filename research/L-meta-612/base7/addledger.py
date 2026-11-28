# addledger.py NAME 'EDGES' PHI M_CUBED : record a graph closed by sizes<Phi-1 (run7) + cubes at Phi-1
import sys,json,itertools
name,edges,phi,mc=sys.argv[1],json.loads(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
n=max(max(e) for e in edges)+1
tau=min(k for k in range(n+1) if any(all(a in S or b in S for a,b in edges) for S in itertools.combinations(range(n),k)))
assert len(edges)+tau-1==phi,(len(edges),tau,phi)
lg=[json.loads(l) for l in open('base7/logs/%s_cubes_%d.jsonl'%(name,mc))]
assert all(x['result']=='UNSAT' and x['drat'].startswith('VERIFIED') for x in lg) and len(lg)==2*(mc+1)
d=json.load(open('ledger/proven_subcubic.json'))
e=dict(d[-1]);e.update(name=name,edges=edges,n=n,m=len(edges),tau=tau,phi=phi,L=phi,
 flags='sizes 1..%d: run7.py; size %d: cubes7.py (%d cubes, all UNSAT, all DRAT VERIFIED), log base7/logs/%s_cubes_%d.jsonl'%(mc-1,mc,len(lg),name,mc),date='2026-11-27')
e['per_size']={str(mc):{'result':'UNSAT','method':'%d cubes (cubes7.py)'%len(lg),'drat':'all VERIFIED'}}
d.append(e);json.dump(d,open('ledger/proven_subcubic.json','w'),indent=0);print(name,'recorded; total',len(d))
