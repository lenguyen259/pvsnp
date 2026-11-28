n=14
E=[(0,8),(0,10),(1,7),(1,9),(1,13),(2,8),(2,12),(2,13),(3,7),(3,11),(3,12),(4,10),(4,11),(4,13),(5,9),(5,10),(5,12),(6,8),(6,9),(6,11)]
N=1<<n
X=[sum(1<<t for t in range(N) if (t>>j)&1) for j in range(n)]
ALL=(1<<N)-1
F=0
for a,b in E: F|=X[a]&X[b]
def ev(C):
    w=list(X)
    for g in C:
        if g[0]=='not': w.append(ALL^w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w
def ok(C): return ev(C)[-1]==F
