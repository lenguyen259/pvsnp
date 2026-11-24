import sys,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
for line in open('psun.out'):
    a=line.split(); n=int(a[0]); S=eval(line[line.index('('):line.index(')')+1])
    E,L=psun(n,S); g=Graph(E); P=list(L); bare=[w for w in range(n) if w not in S]
    res=[]
    for r in range(len(bare)+1):
        for B in itertools.combinations(bare,r):
            S1=P+list(B); nd=gneed(g,[],S1)
            if nd is None: continue
            res.append((nd-len(S1)-len(P), nd-len(S1)-len(P)-len(B), B))
    res.sort(key=lambda x:(x[1],x[0]))
    print(n,S,'(def with r1>=k+|B|, def with r1>=k, B)',res[:2])
