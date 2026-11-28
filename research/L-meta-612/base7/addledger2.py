# addledger2.py NAME 'EDGES' PHI M : like addledger.py but accepts k=5 cubes replaced by 8 sub-cubes (op of gates 8,9,10 split)
import sys,json,itertools
name,edges,phi,mc=sys.argv[1],json.loads(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
n=max(max(e) for e in edges)+1
tau=min(k for k in range(n+1) if any(all(a in S or b in S for a,b in edges) for S in itertools.combinations(range(n),k)))
assert len(edges)+tau-1==phi and mc==phi-1,(len(edges),tau,phi)
ok={}
for l in open('base7/logs/%s_cubes_%d.jsonl'%(name,mc)):
    x=json.loads(l)
    if x['result']=='UNSAT' and x['drat'].startswith('VERIFIED'): ok[x['cube']]=x
need=0
for k in range(mc+1):
    for o in '&|':
        key='%s%d'%(o,k)
        if key in ok: need+=1; continue
        subs=['%s_%s'%(key,''.join(c)) for c in itertools.product('ao',repeat=3)]
        assert all(s in ok for s in subs),('missing',key,[s for s in subs if s not in ok])
        need+=8
d=json.load(open('ledger/proven_subcubic.json'))
e=dict(d[-1]);e.update(name=name,edges=edges,n=n,m=len(edges),tau=tau,phi=phi,L=phi,
 flags='sizes 1..%d: run7.py; size %d: cubes7.py (top cubes by output op x #AND; k=5 cubes split on op of gates 8,9,10 into 8 sub-cubes; %d cubes total, all UNSAT, all DRAT VERIFIED), log base7/logs/%s_cubes_%d.jsonl'%(mc-1,mc,need,name,mc),date='2026-11-28')
e['per_size']={str(mc):{'result':'UNSAT','method':'%d cubes (cubes7.py, --splitops 8,9,10 for k=5)'%need,'drat':'all VERIFIED'}}
d.append(e);json.dump(d,open('ledger/proven_subcubic.json','w'),indent=0);print(name,'recorded; total',len(d))
