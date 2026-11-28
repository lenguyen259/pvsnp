import sys, json, glob, collections
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from lib import phiE, phi0, phi1, nbrs, minimal_ands, fmt
def live_after(n,circ,v,b):
    rep={i:('n',i) for i in range(n)}; rep[v]=('c',b); live={}
    for (i,o,j,k) in circ:
        A,B=rep[j],rep[k]
        if A[0]=='c' or B[0]=='c':
            c,other=(A,B) if A[0]=='c' else (B,A)
            if o=='&': rep[i]= other if c[1]==1 else ('c',0)
            else: rep[i]= other if c[1]==0 else ('c',1)
        elif A==B: rep[i]=A
        else: rep[i]=('n',i); live[i]=(A[1],B[1])
    out=rep[circ[-1][0]]
    if out[0]=='c': return set()
    seen=set(); st=[out[1]]
    while st:
        x=st.pop()
        if x in live and x not in seen: seen.add(x); st.extend(live[x])
    return seen
def info(n,E,c):
    G={i:(o,j,k) for i,o,j,k in c}; rd=collections.defaultdict(list)
    for i,o,j,k in c: rd[j].append(i); rd[k].append(i)
    P=phiE(E); s=len(c); allg={i for i,_,_,_ in c}
    need={(v,b):P-(phi0(E,v) if b==0 else phi1(E,v)) for v in range(n) for b in (0,1)}
    dead={vb:allg-live_after(n,c,*vb) for vb in need}
    return G,rd,need,dead
def stars(n,E,c,G,rd):
    out=[]
    for g,A,B in minimal_ands(n,c):
        if A&B: continue
        o,j,k=G[g]
        for X,Y,yy in ((A,B,k),(B,A,j)):
            if len(X)!=1: continue
            (a,)=X
            if (j if yy==k else k)!=a: continue
            T=set(); st=[yy]
            while st:
                x=st.pop()
                if x>=n and x not in T: T.add(x); st+= [G[x][1],G[x][2]]
            priv=set(); ch=True
            while ch:
                ch=False
                for x in T-priv:
                    if all(r==g or r in priv for r in rd[x]): priv.add(x); ch=True
            d=len(nbrs(E,a)); F=len(rd[a])
            if F>=d: cat='A1'
            elif F==1 and priv==T: cat='A2'
            elif F==1: cat='S2'
            else: cat='S1'
            out.append(dict(g=g,a=a,B=sorted(Y),y=yy,T=sorted(T),priv=sorted(priv),F=F,deg=d,cat=cat))
    return out
def tts(n,c):
    T={}
    for u in range(n): T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
