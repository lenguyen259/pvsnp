# Compact (Kojevnikov-Kulikov-Yaroslavtsev style) exact-synthesis encoding, HasCircuitSize model:
# gate i: left selector L (one-hot), right selector R (one-hot); binary AND/OR need L<R, NOT needs L=R.
# Every gate counts; output = last gate; every other gate read; NOT(NOT) and op(g, NOT g) forbidden;
# adjacent gates in colex (R,L) order unless i+1 reads i (exchange argument); equal (R,L): only AND<OR.
import random
n=9
E=[(0,5),(0,6),(1,6),(2,6),(1,7),(3,7),(4,7),(2,8),(3,8),(5,8),(7,8)]
def f(t): return int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
class Enc2:
    def __init__(s_, s, mono=False, add=None):
        s_.s=s; s_.cnt=0; s_.CL=[]; add=s_.addc=add or s_.CL.append; nv=s_.nv
        s_.L=[[nv() for j in range(n+i)] for i in range(s)]
        s_.R=[[nv() for j in range(n+i)] for i in range(s)]
        s_.isnot=[nv() for i in range(s)]; s_.op=[nv() for i in range(s)]
        L,R,isnot,op=s_.L,s_.R,s_.isnot,s_.op
        for i in range(s):
            m=n+i
            for S in (L[i],R[i]):
                add(list(S))
                for a in range(m):
                    for b in range(a+1,m): add([-S[a],-S[b]])
            add([-isnot[i],op[i]])
            if mono: add([-isnot[i]])
            for j in range(m):
                # binary: L<R ; NOT: L==R
                for k in range(j+1): add([isnot[i],-L[i][j],-R[i][k]])
                add([-isnot[i],-L[i][j],R[i][j]])
                if j>=n: add([-isnot[i],-L[i][j],-isnot[j-n]])  # no NOT(NOT)
            # op(g, NOT g) forbidden: L=j, R=k, gate k is NOT reading j
            for k in range(n,m):
                for j in range(k):
                    add([isnot[i],-L[i][j],-R[i][k],-isnot[k-n],-L[k-n][j]])
            # op(a, op(a,b)) with same op forbidden (copy)
            for k in range(n,m):
                g=k-n
                for j in range(k):
                    for side in (L,R):
                        # gate i = op(j,k) ; gate g reads j (on either side) and is binary with same op
                        for c in ([isnot[i],-L[i][j],-R[i][k],isnot[g],-side[g][j],op[i],op[g]],
                                  [isnot[i],-L[i][j],-R[i][k],isnot[g],-side[g][j],-op[i],-op[g]]):
                            add(c)
        for g in range(s-1):
            add([v for i in range(g+1,s) for v in (L[i][n+g],R[i][n+g])])
        for i in range(s-1):
            m=n+i
            for a in range(m):
                for b in range(a):
                    add([-R[i+1][b],-R[i][a]])
            for b in range(m):
                for d in range(b+1):
                    for c in range(d):
                        add([-R[i+1][b],-R[i][b],-L[i+1][c],-L[i][d]])
                # equal (R,L): identical inputs -> types must be AND then OR (NOT equal NOT forbidden)
                for c in range(b+1):
                    add([-R[i+1][b],-R[i][b],-L[i+1][c],-L[i][c],-isnot[i]])
                    add([-R[i+1][b],-R[i][b],-L[i+1][c],-L[i][c],-op[i]])
                    add([-R[i+1][b],-R[i][b],-L[i+1][c],-L[i][c],op[i+1]])
        s_.X={}
    def nv(s_): s_.cnt+=1; return s_.cnt
    def addrow(s_,t):
        add=s_.addc; s=s_.s; nv=s_.nv
        x=[nv() for i in range(s)]; a=[nv() for i in range(s)]; b=[nv() for i in range(s)]
        s_.X[t]=x
        for i in range(s):
            for S,V in ((s_.L[i],a[i]),(s_.R[i],b[i])):
                for j in range(n+i):
                    if j<n: add([-S[j], V if (t>>j)&1 else -V])
                    else: add([-S[j],-V,x[j-n]]); add([-S[j],V,-x[j-n]])
            X,A,B,nt,o=x[i],a[i],b[i],s_.isnot[i],s_.op[i]
            add([-nt,X,A]); add([-nt,-X,-A])
            add([nt,o,-X,A]); add([nt,o,-X,B]); add([nt,o,X,-A,-B])
            add([nt,-o,X,-A]); add([nt,-o,X,-B]); add([nt,-o,-X,A,B])
        add([x[s-1] if f(t) else -x[s-1]])
    def decode(s_,model):
        M=set(v for v in model if v>0); G=[]
        for i in range(s_.s):
            l=[j for j in range(n+i) if s_.L[i][j] in M][0]; r=[j for j in range(n+i) if s_.R[i][j] in M][0]
            G.append(('not',l) if s_.isnot[i] in M else (('or' if s_.op[i] in M else 'and'),l,r))
        return G
    def assume(s_,G):
        A=[]
        for i,g in enumerate(G):
            if g[0]=='not': A+=[s_.L[i][g[1]],s_.R[i][g[1]],s_.isnot[i]]
            else: A+=[s_.L[i][min(g[1:])],s_.R[i][max(g[1:])],-s_.isnot[i],(s_.op[i] if g[0]=='or' else -s_.op[i])]
        return A
