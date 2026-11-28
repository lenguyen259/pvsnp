"""ports of minimum C_n circuits: wire (h,side) of AND gate h with C'[wire:=1] = f v x_u.
Then all simultaneously valid sets of ports (distinct wires), and whether their holders lie in a min vertex cover."""
import sys,itertools,collections
def parse(line):
    c=[]
    for tok in line.split():
        i,rest=tok.split('='); o='&' if '&' in rest else '|'; j,k=rest.split(o); c.append((int(i),o,int(j),int(k)))
    return c
def setup(n):
    X=[sum(1<<m for m in range(1<<n) if (m>>u)&1) for u in range(n)]
    E=[(i,(i+1)%n) for i in range(n)]
    f=0
    for a,b in E: f|=X[a]&X[b]
    full=(1<<(1<<n))-1
    return X,E,f,full
def evalc(c,X,full,ones=()):
    T={u:X[u] for u in range(len(X))}
    for i,o,j,k in c:
        a=full if (i,0) in ones else T[j]; b=full if (i,1) in ones else T[k]
        T[i]=(a&b) if o=='&' else (a|b)
    return T
def mincovers(n):
    E=[(i,(i+1)%n) for i in range(n)]; t=(n+1)//2
    return [set(S) for S in itertools.combinations(range(n),t) if all(a in S or b in S for a,b in E)]
def analyse(n,c,X,E,f,full,MC,maxk=3):
    out=c[-1][0]; ports={}
    for i,o,j,k in c:
        if o!='&': continue
        for sd in (0,1):
            T=evalc(c,X,full,{(i,sd)})
            for u in range(n):
                if T[out]==f|X[u]: ports[(i,sd)]=u
    sim=[]
    W=list(ports)
    for r in range(2,maxk+1):
        for ws in itertools.combinations(W,r):
            us=[ports[w] for w in ws]
            if len(set(us))<r: continue
            ok=True
            for rr in range(2,r+1):
                for sub in itertools.combinations(range(r),rr):
                    T=evalc(c,X,full,{ws[q] for q in sub}); tgt=f
                    for q in sub: tgt|=X[us[q]]
                    if T[out]!=tgt: ok=False;break
                if not ok: break
            if ok: sim.append((ws,tuple(us),any(set(us)<=S for S in MC)))
    return ports,sim
if __name__=='__main__':
    n=int(sys.argv[1]); X,E,f,full=setup(n); MC=mincovers(n)
    st=collections.Counter(); bad=[]
    for line in open(sys.argv[2]):
        c=parse(line); ports,sim=analyse(n,c,X,E,f,full,MC)
        U=set(ports.values())
        st['circ']+=1; st['inMC_U']+=any(U<=S for S in MC)
        st['nports=%d'%len(ports)]+=1
        for ws,us,inc in sim:
            st['sim%d'%len(us)]+=1
            if not inc: bad.append((line.strip(),ws,us))
    print(dict(st)); print('sim-sets with holders not in a common min cover:',len(bad))
    for b in bad[:10]: print(b)
