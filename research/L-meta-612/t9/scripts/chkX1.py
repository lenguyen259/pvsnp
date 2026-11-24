"""DATA check of Lemma X1 (x_v:=1 removes >=1 AND gate after reduction), of (AND) #AND>=tau, and of
#OR>=|E|-1 on pseudoforests, over cached circuit pools."""
import sys,json,itertools,random,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import tau
def parse(s):
    c=[]
    for tok in s.split():
        i,r=tok.split('='); o='&' if '&' in r else '|'; j,k=r.split(o); c.append((int(i),o,int(j),int(k)))
    return c
def tabs(n,c,sub):
    M=1<<n; full=(1<<M)-1
    X=[sum(1<<m for m in range(M) if (m>>u)&1) for u in range(n)]
    T={}
    for u in range(n): T[u]=(full if sub[u] else 0) if u in sub else X[u]
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T,full
def red_and(n,c,sub):
    T,full=tabs(n,c,sub); first={}; real={}; canon={}
    for u in range(n):
        canon[u]='K' if T[u] in (0,full) else first.setdefault(T[u],u)
    for i,o,j,k in c:
        if T[i] in (0,full): canon[i]='K'; continue
        if T[i] in first: canon[i]=first[T[i]]; continue
        first[T[i]]=i; canon[i]=i; real[i]=(o,canon[j],canon[k])
    out=canon[c[-1][0]]; seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(y for y in real[x][1:] if y!='K')
    return sum(1 for i in seen if real[i][0]=='&'), T
def nverts(E): return 1+max(max(e) for e in E)
def ispf(E,n):
    par=list(range(n))
    def fd(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in E: par[fd(a)]=fd(b)
    cnt=collections.Counter(fd(v) for v in range(n)); ce=collections.Counter(fd(a) for a,b in E)
    return all(ce[r]<=cnt[r] for r in cnt)
if __name__=='__main__':
 st=collections.Counter(); viol=[]
 files=sys.argv[1:]; lim=int(files.pop()) if files[-1].isdigit() else 10**9
 for fn in files:
   for li,line in enumerate(open(fn)):
     if li>=lim: break
     d=json.loads(line); E=[tuple(e) for e in d['E']]; n=max(nverts(E),0); c=parse(d['c'])
     n=min(min(i for i,_,_,_ in c),n) if c else n
     n=min(i for i,_,_,_ in c)
     T,full=tabs(n,c,{}); f=T[c[-1][0]]
     na=sum(1 for x in c if x[1]=='&'); no=len(c)-na; t=tau(tuple(sorted(E)))
     st['circ']+=1
     if na<t: viol.append(('AND',fn,line[:200]))
     if ispf(E,n):
         st['pf']+=1
         if no<len(E)-1: viol.append(('OR',fn,line[:200]))
     a0,_=red_and(n,c,{})
     for v in range(n):
         if not any(v in e for e in E): continue
         a1,T1=red_and(n,c,{v:1})
         if T1[c[-1][0]]==full: continue
         st['X1']+=1
         if a1>a0-1: viol.append(('X1',v,fn,line[:200]))
 print(dict(st),'violations',len(viol))
 for x in viol[:5]: print(x)
