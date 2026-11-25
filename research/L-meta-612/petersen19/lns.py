# Large-neighbourhood SAT search: keep a downward-closed set K of gates of a known circuit, ask SAT for a
# circuit of total size s whose first |K| gates are K (any topological order; no canonical order).
# usage: lns.py circuits.json s keep_count n_samples timeout seed
import json, sys, random, subprocess, time
from plib import verify, canon
circs=json.load(open(sys.argv[1])); s=int(sys.argv[2]); kc=int(sys.argv[3]); ns=int(sys.argv[4]); to=float(sys.argv[5])
random.seed(int(sys.argv[6])); n=10
def closed_subset(c,k):
    # random downward-closed subset of size k (gates only)
    avail=lambda S: [g for g in range(len(c)) if g not in S and all(x<n or (x-n) in S for x in c[g][1:])]
    S=[]
    while len(S)<k:
        a=avail(S)
        if not a: return None
        S.append(random.choice(a))
    return S
seen=set()
for it in range(ns):
    c=random.choice(circs); S=closed_subset(c,kc)
    if S is None: continue
    # renumber kept gates in order
    pos={i:i for i in range(n)}; pre=[]
    for g in S:
        o,j,k=c[g]; a,b=sorted((pos[j],pos[k])); pos[n+g]=n+len(pre); pre.append([o,a,b])
    key=json.dumps(sorted(map(tuple,pre)))
    if key in seen: continue
    seen.add(key)
    part=[[n+i,o,a,b] for i,(o,a,b) in enumerate(pre)]
    cmd=['python3','enc5.py',str(s),'--nocanon','--factc','--partial',json.dumps(part),'--solve','--timeout',str(to)]
    out=subprocess.run(cmd,capture_output=True,text=True).stdout
    res=[l for l in out.splitlines() if 'RESULT' in l or 'VERIF' in l]
    print(it,len(pre),' '.join(res),flush=True)
    if any('VERIFIED' in l for l in res): print('FOUND',res,flush=True); break
