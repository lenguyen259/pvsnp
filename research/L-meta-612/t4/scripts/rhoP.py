import sys
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *
from psun import psun
for line in open('psun.out'):
    a=line.split(); n=int(a[0]); S=eval(line[line.index('('):line.index(')')+1])
    E,L=psun(n,S); g=Graph(E); P=list(L)
    nd=gneed(g,[],P); print(n,S,'Phi',g.P,'|P|',len(P),'need',nd,'deficit',nd-2*len(P))
