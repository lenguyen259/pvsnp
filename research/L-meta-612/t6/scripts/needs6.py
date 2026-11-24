import sys
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t4/scripts')
from gen import *
from psun import psun
for n,S in [(5,(0,1,2)),(6,(0,1)),(6,(0,3)),(6,(0,1,2,3)),(7,(0,1,2)),(7,(0,1,4)),(8,(0,1)),(8,(0,3))]:
    E,L=psun(n,S); g=Graph(E); print(n,S,'Phi',g.P)
    for w in range(n):
        if w in S: continue
        print('  run w',w,'A',gneed(g,[w],[]),'B',gneed(g,[],[w]),'N',gneed(g,sorted(g.N[w]|{w}),[]))
