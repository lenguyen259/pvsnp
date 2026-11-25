# refine.py JOBS RESULTS OUT [nbits]: every TIMEOUT cube is split into a complete prefix tree over the
# next nbits unfixed lexbot bits (b1=1 | b1=0,b2=1 | ... | all 0). Children cover the parent exactly.
import json, sys, shlex
jobs={l.split('\t')[0]:l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()}
nb=int(sys.argv[4]) if len(sys.argv)>4 else 4
n=10 if '--graph' not in open(sys.argv[1]).readline() else None
out=[]
for l in open(sys.argv[2]):
    r=json.loads(l)
    if 'TIMEOUT' not in r['res']: continue
    nm,s,args=jobs[r['name']]; a=shlex.split(args)
    gi=a.index('--graph') if '--graph' in a else None
    nv=max(max(e) for e in json.loads(a[gi+1]))+1 if gi is not None else 10
    ci=a.index('--cube'); cube=json.loads(a[ci+1])
    fixed={(c[1],c[2],c[3]) for c in cube if c[0]=='b'}
    BITS=[(j,k,o) for j in range(nv) for k in range(j+1,nv) for o in (1,0)]
    free=[b for b in BITS if b not in fixed][:nb]
    for d in range(len(free)+1):
        c=cube+[['b',*free[t],0] for t in range(d)]
        if d<len(free): c.append(['b',*free[d],1])
        a2=list(a); a2[ci+1]=json.dumps(c)
        out.append('%s_r%d\t%s\t%s'%(nm,d,s,' '.join(shlex.quote(x) for x in a2)))
open(sys.argv[3],'w').write('\n'.join(out)+'\n'); print(len(out))
