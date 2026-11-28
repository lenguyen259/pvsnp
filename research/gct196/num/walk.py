import os; os.environ['OMP_NUM_THREADS']='1'
exec(open('/home/user/pvsnp/research/gct196/num/ext_search.py').read().split('which=sys.argv')[0])
from lm3 import search_sub
import sys
p,q=4,7
F,H=known(p,q); N8=np.load('ext_G_8.npy')
srcs={'F7':F,'hook':H,'N8':N8,'G7':Gtype()}
rng=np.random.default_rng(int(sys.argv[1]))
seen=0
for it in range(int(sys.argv[2])):
    name=list(srcs)[it%len(srcs)]; B=srcs[name]; n=B.shape[0]
    # random codim-1 or codim-2 subspace
    k=n-1-(it//len(srcs))%2
    if k<3: continue
    A=rng.normal(size=(k,n))+1j*rng.normal(size=(k,n))
    if rng.random()<0.5:  # sparse combos to keep structure
        A=np.zeros((k,n),complex)
        idx=rng.permutation(n)
        for i in range(k): A[i,idx[i]]=1
        A[:,idx[k:]]=rng.normal(size=(k,n-k))
    S=A@B
    Pb=T1orth(S); d=Pb.shape[0]
    msg=f'{it} {name} sub{k} T1={d}'
    if d>=k+3:
        for target in range(max(n+1,k+2),min(d,11)+1):
            ok=False
            for s in range(4):
                c,Bn=search_sub(p,q,target,s,Pb,iters=300)
                if check(Bn,p,q)<1e-9:
                    ok=True; t1=T1(Bn,p,q); msg+=f' found{target}(T1={t1})'
                    np.save(f'walk_{it}_{target}.npy',Bn)
                    if target>=9: msg+=' !!!!!'
                    srcs[f'w{it}_{target}']=Bn
                    break
            if not ok: msg+=f' no{target}'; break
    print(msg,flush=True)
