import json,sys
from star import analyze
def run(n,E,c):
    ch,nor,s,s0=analyze(n,c,E)
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    print('E',E,'#OR',nor,'reduced size',s,'of',s0)
    print(' circ',' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c))
    print(' deg',deg,'\n ch ',ch,'\n good',[v for v in range(n) if ch[v]>=deg[v]],'V2 good',[v for v in range(n) if deg[v]==2 and ch[v]>=2])
# two triangles 012, 345 + bridge 03; V2 = 1,2,4,5
E=[(0,1),(0,2),(0,3),(1,2),(3,4),(3,5),(4,5)]
c=[(6,'&',0,3),(7,'|',1,6),(8,'|',2,6),(9,'|',4,6),(10,'|',5,6),
   (11,'&',7,8),(12,'|',7,8),(13,'&',0,12),(14,'|',11,13),
   (15,'&',9,10),(16,'|',9,10),(17,'&',3,16),(18,'|',15,17),(19,'|',14,18)]
run(6,E,c)
