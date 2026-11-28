# Exact synthesis CNF for the L-meta-10952 edge function (AND/OR fan-in 2, optional NOT; every gate counted).
# Usage: syn9.py s out.cnf [mono]   -> writes DIMACS + out.cnf.map (json var map)
import sys, json
n = 9
E = [(0,4),(1,5),(0,6),(2,6),(1,7),(3,7),(5,7),(2,8),(3,8),(4,8),(7,8)]
def f(t): return int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
s = int(sys.argv[1]); out = sys.argv[2]; mono = len(sys.argv)>3 and sys.argv[3]=='mono'
R = 1<<n
if mono:
    T=[r for r in range(R) if f(r)]; F=[r for r in range(R) if not f(r)]
    mint=[r for r in T if not any(q!=r and q&r==q for q in T)]
    maxf=[r for r in F if not any(q!=r and q&r==r for q in F)]
    rows = sorted(mint+maxf)
else:
    rows = list(range(R))
cnt=[0]
def nv(): cnt[0]+=1; return cnt[0]
cls=[]
sa=[[nv() for j in range(n+i)] for i in range(s)]
sb=[[nv() for j in range(n+i)] for i in range(s)]
isn=[nv() for i in range(s)]; isa=[nv() for i in range(s)]
x={(i,t):nv() for i in range(s) for t in rows}
va={(i,t):nv() for i in range(s) for t in rows}
vb={(i,t):nv() for i in range(s) for t in rows}
for i in range(s):
    m=n+i
    for S in (sa[i],sb[i]):
        cls.append(list(S))
        for a in range(m):
            for b in range(a+1,m): cls.append([-S[a],-S[b]])
    if mono: cls.append([-isn[i]])
    for j in range(m):
        for k in range(j+1): cls.append([isn[i],-sa[i][j],-sb[i][k]])
        cls.append([-isn[i],-sa[i][j],sb[i][j]])
    cls.append([-isn[i],-isa[i]])
    for t in rows:
        for S,V in ((sa[i],va),(sb[i],vb)):
            for j in range(m):
                if j<n:
                    cls.append([-S[j], V[i,t] if (t>>j)&1 else -V[i,t]])
                else:
                    X=x[j-n,t]; cls.append([-S[j],-V[i,t],X]); cls.append([-S[j],V[i,t],-X])
        X,A,B=x[i,t],va[i,t],vb[i,t]
        cls += [[-isn[i],X,A],[-isn[i],-X,-A],
                [isn[i],-isa[i],-X,A],[isn[i],-isa[i],-X,B],[isn[i],-isa[i],X,-A,-B],
                [isn[i],isa[i],X,-A],[isn[i],isa[i],X,-B],[isn[i],isa[i],-X,A,B]]
for t in rows: cls.append([x[s-1,t] if f(t) else -x[s-1,t]])
for i in range(s-1):
    w=n+i; cls.append([v for k in range(i+1,s) for v in (sa[k][w],sb[k][w])])
for i in range(s):
    for j in range(n,n+i): cls.append([-isn[i],-sa[i][j],-isn[j-n]])
# every input used (f depends on all 9 inputs)
for j in range(n): cls.append([v for k in range(s) for v in (sa[k][j],sb[k][j])])
with open(out,'w') as fo:
    fo.write('p cnf %d %d\n'%(cnt[0],len(cls)))
    for c in cls: fo.write(' '.join(map(str,c))+' 0\n')
json.dump(dict(n=n,s=s,sa=sa,sb=sb,isn=isn,isa=isa),open(out+'.map','w'))
print('vars',cnt[0],'clauses',len(cls),'rows',len(rows))
