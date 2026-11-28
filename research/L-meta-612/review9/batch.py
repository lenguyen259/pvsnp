import sys, time, itertools, json
from sat import solve
def tau(n,E):
    for k in range(n+1):
        for S in itertools.combinations(range(n),k):
            if all(u in S or v in S for u,v in E): return k
def cyc(k,o=0): return [[o+i,o+(i+1)%k] for i in range(k)]
G={
 'C3':(3,cyc(3)),'C5':(5,cyc(5)),'C6':(6,cyc(6)),'C7':(7,cyc(7)),'2C3':(6,cyc(3)+cyc(3,3)),
 'P4':(4,[[0,1],[1,2],[2,3]]),'P5':(5,[[0,1],[1,2],[2,3],[3,4]]),'P6':(6,[[0,1],[1,2],[2,3],[3,4],[4,5]]),
 'spider':(7,[[0,1],[1,2],[0,3],[3,4],[0,5],[5,6]]),
 'C3+pend':(4,cyc(3)+[[0,3]]),'bull':(5,cyc(3)+[[0,3],[1,4]]),'net':(6,cyc(3)+[[0,3],[1,4],[2,5]]),
 'C5+pend':(6,cyc(5)+[[0,5]]),'C5+2pend':(7,cyc(5)+[[0,5],[2,6]]),'C5+2pendadj':(7,cyc(5)+[[0,5],[1,6]]),
 'C6+2pend':(8,cyc(6)+[[0,6],[3,7]]),'C3+P2':(5,cyc(3)+[[3,4]]),'C3pendpath':(5,cyc(3)+[[0,3],[3,4]]),
 'C8':(8,cyc(8)),'C3+C5':(8,cyc(3)+cyc(5,3)),
}
if __name__=="__main__":
  slack=int(sys.argv[1]); names=sys.argv[2:] or list(G)
  for nm in names:
      n,E=G[nm]; t=tau(n,E); m=len(E)
      lo=m-1+(t-1)  # fewest gates possible if OR>=m-1 (we also try below to be safe)
      res=[]
      for s in range(max(1,t-1), m-1+t-1+slack+1):
          t0=time.time(); r=solve(n,E,s,t-1); res.append((s,'SAT' if r else 'UNSAT',round(time.time()-t0,1)))
          if r: print('COUNTEREXAMPLE',nm,s,r,flush=True); break
      print(nm,'tau',t,'|E|',m,res,flush=True)
