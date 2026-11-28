import sys, json, time
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from lib import *
E=[tuple(e) for e in json.loads(sys.argv[1])]; X=int(sys.argv[2]); which=sys.argv[3]
n=max(max(e) for e in E)+1; s=phiE(E)+X; t0=time.time()
kw={'max_or':len(E)-2} if which=='or' else {'max_and':tauE(E)-1}
r=exists_circuit(n,target_tt(n,E),s,want_model=True,**kw)
print(sys.argv[1],X,which,r if not isinstance(r,tuple) else r,'%.0fs'%(time.time()-t0),flush=True)
