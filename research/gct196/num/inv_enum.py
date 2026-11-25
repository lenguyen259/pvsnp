import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
mode=sys.argv[1]; n=int(sys.argv[2]); seeds=int(sys.argv[3])
exec(open('/home/user/pvsnp/research/gct196/num/inv_search.py').read().split("if __name__=='__main__':")[0])
if mode=='c7': P=permmat([0,1,2,3],[(j+1)%7 for j in range(7)])
else: P=permmat([0,1,2,3],[0]+[1+(j%6) for j in range(1,7)])
blocks=eig_blocks(P)
# order blocks by eigenvalue angle
ang=[np.angle(w)%(2*np.pi) for w,b in blocks]; order=np.argsort(ang); blocks=[blocks[i] for i in order]
sizes=[b.shape[0] for w,b in blocks]; m=len(blocks)
print(mode,'sizes',sizes,flush=True)
def canon(d):
    # symmetry: k -> u*k mod m for units u
    from math import gcd
    best=None
    for u in range(1,m):
        if gcd(u,m)!=1: continue
        e=[0]*m
        for k in range(m): e[(u*k)%m]=d[k]
        t=tuple(e); best=t if best is None or t<best else best
    return best
profs=set()
import itertools
for d in itertools.product(*[range(s+1) for s in sizes]):
    if sum(d)==n: profs.add(canon(d))
profs=sorted(profs); print('profiles',len(profs),flush=True)
found=0
for i,d in enumerate(profs):
    bestc=9
    for s in range(seeds):
        cost,B=search_blocks(blocks,list(d),s,iters=250)
        ch=check(B,p,q); bestc=min(bestc,ch)
        if ch<1e-8:
            found+=1; print(mode,n,'FOUND',d,'T1',T1(B,p,q),flush=True); np.save(f'enum_{mode}_{n}_{i}.npy',B); break
    if i%20==0: print(mode,n,i,d,'best %.2g'%bestc,flush=True)
print(mode,n,'DONE found',found,flush=True)
