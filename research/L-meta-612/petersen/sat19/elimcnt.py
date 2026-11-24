def elimcount(c,n,Z):
    N=n+len(c); r=[0 if u in Z else 1 for u in range(n)]
    for o,j,k in c: r.append(r[j]&r[k] if o=='&' else r[j]|r[k])
    users={g:[] for g in range(N)}
    for idx,(o,j,k) in enumerate(c): users[j].append(n+idx); users[k].append(n+idx)
    dead={}
    for g in range(N-1,n-1,-1):
        dead[g]= g!=N-1 and all(r[u]==0 or dead[u] for u in users[g])
    return sum(1 for idx,(o,j,k) in enumerate(c) if r[j]==0 or r[k]==0 or dead[n+idx])
