import sys,json,random,subprocess
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from mkopts import opts
from canon import canon
name,gname,K,mode=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
from graphs import G
E=G(gname); g,O=opts(E)
L=[json.loads(l) for l in open('../t3/locpool.jsonl') if json.loads(l)['g']==name]
random.Random(1).shuffle(L)
for D in L[:K]:
    c=parse(D['c']); n=g.n
    cc=canon([(o,j,k) for i,o,j,k in c],n)
    # rebuild list circuit from canon to compute elim on same circuit
    c2=[(n+i,o,j,k) for i,(o,j,k) in enumerate(cc)]
    ops=[]
    for (S0,S1),nd in O.items():
        rho={x:0 for x in S0}; rho.update({x:1 for x in S1})
        e=elim(g,c2,rho); ops.append([list(S0),list(S1),e-(1 if mode=='tight' else 0)])
    r=subprocess.run(['python3','enc5.py',str(len(c2)),'--graph',json.dumps(E),'--fix',json.dumps(cc),'--opts',json.dumps(ops),'--timeout','60'],capture_output=True,text=True).stdout
    print(D['s'],r.strip().split('\n')[-1])
