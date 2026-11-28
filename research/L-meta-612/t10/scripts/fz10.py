import sys
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t8/scripts')
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
import graphs, t3fuzz
def cyc(n): return [(i,(i+1)%n) for i in range(n)]
def theta(a,b,c):
    # vertices 0,1 joined by paths with a,b,c edges
    E=[];nx=2
    for L in (a,b,c):
        prev=0
        for t in range(L-1): E.append((prev,nx)); prev=nx; nx+=1
        E.append((prev,1))
    return E
G10={'C5p':cyc(5)+[(0,5)],'C6p2':cyc(6)+[(0,6),(2,7)],'C7p':cyc(7)+[(0,7)],'C8p2':cyc(8)+[(0,8),(4,9)],
 'C9p':cyc(9)+[(0,9)],'C8':cyc(8),'C9':cyc(9),
 'tree-cat':[(0,1),(1,2),(2,3),(3,4),(1,5),(2,6),(3,7)],'tree-bin':[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)],
 'th233':theta(2,3,3),'th333':theta(3,3,3),'th244':theta(2,4,4),'th334':theta(3,3,4)}
t3fuzz.GR.update(G10)
import fuzz8
fuzz8.t3fuzz.GR.update(G10)
if __name__=='__main__':
    import json
    name,secs,K,seed,mode=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
    print(json.dumps(fuzz8.search(name,secs,K,seed,mode)),flush=True)
