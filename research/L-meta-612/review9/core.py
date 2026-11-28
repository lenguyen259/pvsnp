import itertools, random, sys
# circuit: n inputs, gates list of (op, a, b) with a,b node ids; op in AND/OR; node ids < own id; output last
# constants represented as nodes 'T'/'F' during restriction
def tt_var(n,i): return sum(1<<r for r in range(1<<n) if r>>i&1)
def evalc(n,C):
    M=(1<<(1<<n))-1; V=[tt_var(n,i) for i in range(n)]
    for op,a,b in C: V.append(V[a]&V[b] if op=='AND' else V[a]|V[b])
    return V
def fG(n,E): return sum(1<<r for r in range(1<<n) if any(r>>u&1 and r>>v&1 for u,v in E))
def restrict(n,C,assign):
    """assign: dict var->0/1. returns reduced circuit (n same, unused vars stay) or ('const',c)"""
    # node map: id -> ('c',0/1) or ('n',newid)
    mp={}; out=[]
    for i in range(n): mp[i]=('c',assign[i]) if i in assign else ('n',i)
    for g,(op,a,b) in enumerate(C, start=n):
        A,B=mp[a],mp[b]
        if A[0]=='c' or B[0]=='c':
            if A[0]=='c' and B[0]=='c':
                mp[g]=('c', (A[1]&B[1]) if op=='AND' else (A[1]|B[1])); continue
            c,o=(A,B) if A[0]=='c' else (B,A)
            if op=='AND': mp[g]= o if c[1]==1 else ('c',0)
            else: mp[g]= o if c[1]==0 else ('c',1)
            continue
        if A==B: mp[g]=A; continue
        out.append((op,A[1],B[1])); mp[g]=('n',n+len(out)-1)
    o=mp[n+len(C)-1]
    if o[0]=='c': return ('const',o[1])
    return dedead(n,out,o[1])
def dedead(n,C,outid):
    live=set([outid]); 
    for g in range(n+len(C)-1,n-1,-1):
        if g in live: op,a,b=C[g-n]; live|={a,b}
    newid={i:i for i in range(n)}; R=[]
    for g in range(n,n+len(C)):
        if g in live and g<=outid:
            op,a,b=C[g-n]; R.append((op,newid[a],newid[b])); newid[g]=n+len(R)-1
    return ('circ',R,newid[outid])
def func(n,R):
    if R[0]=='const': return ((1<<(1<<n))-1) if R[1] else 0
    return evalc(n,R[1])[R[2]]
def nand(C):
    if isinstance(C,tuple): C=C[1] if C[0]=='circ' else []
    return sum(op=='AND' for op,_,_ in C)
def analyze(n,C,E,stats):
    """C reduced, computes f_G. checks."""
    V=evalc(n,C); N=n+len(C)
    adj={i:set() for i in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    ev=lambda node,r: V[node]>>r&1
    Q={};Ex={};andread={}
    for v in range(n):
        q=set()
        for g,(op,a,b) in enumerate(C,start=n):
            ina=lambda x: x==v or x in q
            if (op=='OR' and (ina(a) or ina(b))) or (op=='AND' and ina(a) and ina(b)): q.add(g)
        sem={g for g in range(n,N) if ev(g,1<<v)}
        if q!=sem: stats['Qmismatch']+=1
        Q[v]=q
        Ex[v]=[g for g,(op,a,b) in enumerate(C,start=n) if op=='AND' and g not in q and (a in q or b in q or a==v or b==v)]
        andread[v]=any(op=='AND' and v in (a,b) for op,a,b in C)
        # removal by x_v:=1
        R=restrict(n,C,{v:1})
        drop=nand(C)-nand(R)
        need=len(Ex[v])+sum(1 for g in q if C[g-n][0]=='AND')
        if drop<need: stats['exitdropfail']+=1
        if adj[v] and drop<1: stats['X1fail']+=1
    nonis=[v for v in range(n) if adj[v]]
    for v in nonis:
        if not andread[v] and len(Ex[v])==1:
            stats['uniq']+=1
            e=Ex[v][0]; op,a,b=C[e-n]
            s_,t_=(a,b) if (a in Q[v]) else (b,a)
            for x in adj[v]:
                if not ev(t_,1<<x): stats['t_notin_Qa']+=1
                if e not in Ex[x]: stats['E_not_exit_a']+=1
    leafless=all(len(adj[v])>=2 for v in nonis)
    if leafless and nonis:
        stats['leafless']+=1
        good=[v for v in nonis if andread[v] or len(Ex[v])>=2]
        if not good: stats['ANDcorefail']+=1; print('ANDCORE FAIL',n,E,C)
        # PF step
        for v in good:
            if andread[v]:
                R=restrict(n,C,{v:0})
                if nand(C)-nand(R)<1: stats['PFa_fail']+=1
                if func(n,R)!=fG(n,[e for e in E if v not in e]): stats['PFa_func']+=1
            if len(Ex[v])>=2:
                asg={v:1}; asg.update({u:0 for u in adj[v]})
                R=restrict(n,C,asg)
                Gr=[e for e in E if not set(e)&({v}|adj[v])]
                if nand(C)-nand(R)<2: stats['PFb_fail']+=1; print('PFb',C,v)
                if func(n,R)!=fG(n,Gr): stats['PFb_func']+=1
            stats['PFok']+=1
