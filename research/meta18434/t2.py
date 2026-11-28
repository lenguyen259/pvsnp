# promise-T2 on n z-variables: weight-1 inputs -> 0, weight-2 -> 1; min monotone gates by SAT
import sys, itertools
sys.setrecursionlimit(10000)
import lns
lns.BUDGET=int(sys.argv[3]) if len(sys.argv)>3 else 2000000
n=int(sys.argv[1]); k=int(sys.argv[2])
rows=[]
for i in range(n):
    p=[0]*n; p[i]=1; rows.append((tuple(p),[(1,)]))
for i,j in itertools.combinations(range(n),2):
    p=[0]*n; p[i]=1; p[j]=1; rows.append((tuple(p),[(0,)]))
import time; t=time.time()
r=lns.synth(rows,n,1,k,False)
print(n,k,'SAT' if r else 'none/unknown',round(time.time()-t,1),r,flush=True)
