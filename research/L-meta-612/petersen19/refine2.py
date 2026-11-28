# refine2.py JOBS RESULTS OUT : every TIMEOUT cube is split by the first gate (index n): its op and input
# pair (j,k). Gate n always reads two inputs, so the children (all n*(n-1) choices) cover the parent.
import json, sys, shlex
jobs={l.split('\t')[0]:l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()}
out=[]
for l in open(sys.argv[2]):
    r=json.loads(l)
    if 'TIMEOUT' not in r['res'] or r['name'] not in jobs: continue
    nm,s,args=jobs[r['name']]; a=shlex.split(args)
    nv=max(max(e) for e in json.loads(a[a.index('--graph')+1]))+1
    for j in range(nv):
        for k in range(j+1,nv):
            for o in '&|':
                a2=a+['--partial',json.dumps([[nv,o,j,k]])]
                out.append('%s_g%d%d%s\t%s\t%s'%(nm,j,k,'a' if o=='&' else 'o',s,' '.join(shlex.quote(x) for x in a2)))
open(sys.argv[3],'w').write('\n'.join(out)+'\n'); print(len(out))
