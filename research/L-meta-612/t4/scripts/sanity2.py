import sys,json,subprocess
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
from canon import canon
from dataP import struct
name=sys.argv[1]; _,n,S=name.split(':'); E,L=psun(int(n),[int(x) for x in S.split(',')]); g=Graph(E)
cnt=0
for l in open('../t3/locpool.jsonl'):
    D=json.loads(l)
    if D['g']!=name: continue
    c=parse(D['c'])
    if struct(g,c,list(L),L)!=3: continue
    cc=canon([(o,j,k) for i,o,j,k in c],g.n)
    r=subprocess.run(['python3','enc5.py',str(len(cc)),'--graph',json.dumps(E),'--fix',json.dumps(cc),'--mincex','--timeout','60'],capture_output=True,text=True).stdout
    print(D['s'],r.strip().split('\n')[-1]); cnt+=1
    if cnt>=4: break
