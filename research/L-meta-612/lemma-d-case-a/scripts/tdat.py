# on enumerated circuits: Lemma D, T(a) (some V2 good), all-V2-single-charged count, hub good
import json,glob,sys
from star import analyze
for fn in sorted(glob.glob('circs/*.json'))+['/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/s_case/circs/02_05_12_13_23_34_45.json']:
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    st=dict(N=0,LD=0,Ta=0,allV2one=0,hubgood=0); seen=set()
    for c in D['circs']:
        c=[tuple(x) for x in c]
        ch,nor,s,s0=analyze(n,c,E); st['N']+=1
        st['LD']+=any(ch[v]>=deg[v] for v in range(n))
        st['Ta']+=any(deg[v]==2 and ch[v]>=2 for v in range(n))
        st['allV2one']+=all(ch[v]==1 for v in range(n) if deg[v]==2)
        st['hubgood']+=any(deg[v]>=3 and ch[v]>=deg[v] for v in range(n))
    print(fn.split('/')[-1],st,flush=True)
