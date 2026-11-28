def minimal_ors(d):
    R=d['R']; n=d['n']; hasor={}
    for i in sorted(R):
        op,j,k=R[i]
        hasor[i]=any((q>=n and (R[q][0]=='|' or hasor[q])) for q in (j,k))
    return [i for i in d['ors'] if not hasor[i]]
