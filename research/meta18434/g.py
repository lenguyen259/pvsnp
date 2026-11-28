import re,subprocess
n=20
ALL=(1<<100)-1
X=[]
for w in range(20):
    m=0
    for u in range(10):
        for v in range(10):
            if (u==w if w<10 else v==w-10): m|=1<<(u*10+v)
    X.append(m)
F=0
for u in range(10):
    for v in range(10):
        if u!=v: F|=1<<(u*10+v)
def ev(C):
    w=list(X)
    for g in C:
        if g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w
def ok(C):
    for i,g in enumerate(C):
        for a in g[1:]:
            if a>=n+i: return False
    return ev(C)[-1]==F
def from_lean(path):
    s=open(path).read()
    gs=re.findall(r'GateOp\.(and|or), \[(\d+), (\d+)\]',s)
    return [(a,int(b),int(c)) for a,b,c in gs]
