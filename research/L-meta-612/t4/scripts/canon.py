import json,sys
def canon(c,n=10):
    N=n+len(c); dep={i:0 for i in range(n)}
    for idx,(o,j,k) in enumerate(c): dep[n+idx]=1+max(dep[j],dep[k])
    pos={i:i for i in range(n)}; out=[]; nxt=n
    for d in range(1,max(dep.values())+1):
        lvl=[n+idx for idx in range(len(c)) if dep[n+idx]==d]
        keys=[]
        for g in lvl:
            o,j,k=c[g-n]; a,b=sorted((pos[j],pos[k])); keys.append(((a,b,0 if o=='&' else 1),g))
        for (a,b,oo),g in sorted(keys): pos[g]=nxt; nxt+=1; out.append(['&' if oo==0 else '|',a,b])
    return out
if __name__=='__main__':
    print(json.dumps(canon(json.loads(sys.argv[1]))))
