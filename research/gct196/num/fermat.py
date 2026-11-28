import numpy as np, itertools
p,q=4,7
def M(x,k):
    tot=0
    for R in itertools.combinations(range(p),k):
        for Cc in itertools.combinations(range(q),k):
            for perm in itertools.permutations(Cc):
                pr=1
                for r,c in zip(R,perm): pr*=x[r,c]
                tot+=pr
    return tot
rng=np.random.default_rng(0)
def decomp(x):
    S=x.sum(); a=x.sum(1)/q - S/(p*q); b=x.sum(0)/p - S/(p*q)
    d=x-a[:,None]-b[None,:]-S/(p*q)
    return d,a,b,S/(p*q)
x=rng.normal(size=(p,q))+1j*rng.normal(size=(p,q)); x-=x.mean()
d,a,b,c=decomp(x)
for sa in [1,-1]:
  for sb in [1,-1]:
    al=sa*1j*np.sqrt(q-1); be=sb*1j*np.sqrt(p-1)
    y=d+al*a[:,None]+be*b[None,:]
    print(sa,sb,'M2',M(x,2),0.5*(y**2).sum(),'M3',M(x,3),(2/3)*(y**3).sum())
