import sys; sys.path.insert(0,'/home/user/pvsnp/research/gct196/num3')
exec(open('run2.py').read().split('for name,Bs in srcs.items():')[0])
for name,Bs in srcs.items():
    M=Bs.reshape(-1,p,q); R=M.sum(2); C=M.sum(1); n=rank(Bs)
    out=[]
    for u in range(p):
        a=rank(np.hstack([M[:,u,:],R,C])); b=rank(np.hstack([M[:,u,:],C]))
        out.append((a,n-a,b,n-b))
    print(name,'(rank(row u,R,C), dim D_u, rank(row u,C), ker)',out)
