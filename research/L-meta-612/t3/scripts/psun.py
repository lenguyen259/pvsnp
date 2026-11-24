import sys,itertools
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import tau,phi
def psun(n,S):
    E=[(i,(i+1)%n) for i in range(n)]; m=n
    L={}
    for s in S: E.append((s,m)); L[m]=s; m+=1
    return [tuple(sorted(e)) for e in E],L
def bad(n,S):
    E,L=psun(n,S); t=tau(tuple(sorted(E)))
    for v,u in L.items():
        Ev=tuple(sorted(e for e in E if v not in e))
        if t-tau(Ev)!=1: return False
    return True
if __name__=='__main__':
  seen=set()
  for n in [3,5,6,7,8,9]:
    for k in range(1,n+1):
        for S in itertools.combinations(range(n),k):
            forms=[tuple(sorted((sg*s+r)%n for s in S)) for r in range(n) for sg in (1,-1)]
            c=min(forms)
            if (n,c) in seen: continue
            seen.add((n,c))
            if bad(n,c): print(n,c,'Phi',phi(psun(n,c)[0]),'nv',n+len(c))
