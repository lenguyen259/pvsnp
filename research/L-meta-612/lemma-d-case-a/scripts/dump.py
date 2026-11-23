import sys, json, time
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from lib import *
E=[tuple(e) for e in json.loads(sys.argv[1])]; lim=int(sys.argv[2]); X=int(sys.argv[3])
n=max(max(e) for e in E)+1; P=phiE(E); t0=time.time()
circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
name='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemDa/circs/'+'_'.join('%d%d'%e for e in E)+('_x%d'%X)+'.json'
json.dump({'E':E,'n':n,'P':P,'X':X,'circs':circs,'complete':len(circs)<lim},open(name,'w'))
print(name,len(circs),'%.0fs'%(time.time()-t0),flush=True)
