import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
exec(open('run2.py').read().split('for name,Bs in srcs.items():')[0])
rng=np.random.default_rng(5)
def crit(Bs):
    M=Bs.reshape(-1,p,q); R=M.sum(2); C=M.sum(1); n=rank(Bs)
    D=n-rank(np.hstack([R,C])); phi=min(rank(np.hstack([M[:,u,:],R])) for u in range(p))
    return n,D,phi
worst={}
cnt={}
for name,Bs in srcs.items():
    n0=Bs.shape[0]
    for k in range(3,n0+1):
        for trial in range(30):
            if k==n0: A=np.eye(n0)
            elif trial%3==0: A=rng.normal(size=(k,n0))+1j*rng.normal(size=(k,n0))
            else:
                A=np.zeros((k,n0),complex); idx=rng.permutation(n0); A[np.arange(k),idx[:k]]=1
                if trial%3==2: A[:,idx[k:]]=rng.normal(size=(k,n0-k))*(rng.random((k,n0-k))<0.3)
            S=A@Bs; n,D,phi=crit(S)
            if D>0:   # uncovered region analogue: bound 6+phi >= n+1 , D>0
                iv=invariants(S,rng); v=iv['Gam']-2*n
                cnt[n]=cnt.get(n,0)+1
                if n not in worst or v<worst[n][0]: worst[n]=(v,name,iv)
            if k==n0: break
print(cnt)
for n in sorted(worst): print(n,worst[n])
