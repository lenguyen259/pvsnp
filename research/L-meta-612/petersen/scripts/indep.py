# independent brute-force checker: evaluates per input, computes ch(v) = #OR gates with an input q such that q(x)<=x_v for all x
import sys, re, itertools
def check(n,E,s):
    g=[]
    for t in s.split():
        m=re.match(r'(\d+)=(\d+)([&|])(\d+)$',t); g.append((int(m[1]),int(m[2]),m[3],int(m[4])))
    ids=[i for i,_,_,_ in g]; out=g[-1][0]
    tab={}  # node -> list of values over all inputs
    X=range(1<<n)
    for v in range(n): tab[v]=[(x>>v)&1 for x in X]
    for i,a,o,b in g: tab[i]=[(p&q) if o=='&' else (p|q) for p,q in zip(tab[a],tab[b])]
    f=[int(any((x>>a)&1 and (x>>b)&1 for a,b in E)) for x in X]
    ok=tab[out]==f
    # reducedness
    seen={}; red=True
    for k in list(range(n))+ids:
        t=tuple(tab[k])
        if t in seen or all(z==0 for z in t) or all(z==1 for z in t):
            if k>=n: red=False
        seen.setdefault(t,k)
    dom=lambda q,v: all(tab[q][x]<= (x>>v)&1 for x in X)
    ch=[sum(1 for i,a,o,b in g if o=='|' and (dom(a,v) or dom(b,v))) for v in range(n)]
    deg=[sum(1 for e in E if v in e) for v in range(n)]
    nor=sum(1 for x in g if x[2]=='|')
    return dict(correct=ok,reduced=red,size=len(g),nor=nor,nand=len(g)-nor,ch=ch,deg=deg,lemmaD_cex=all(ch[v]<deg[v] for v in range(n) if deg[v]))
if __name__=='__main__':
    import json
    E=[tuple(e) for e in json.loads(sys.argv[1])]; n=max(max(e) for e in E)+1
    print(check(n,E,sys.argv[2]))
