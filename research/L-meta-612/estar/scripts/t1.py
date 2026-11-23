import sys, collections, time
from lib import *
nmin,nmax,X,lim=map(int,sys.argv[1:5])
for n,E in graphs(nmin,nmax):
    P=phiE(E); t0=time.time()
    circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
    st=collections.Counter()
    for c in circs:
        good,sl=goodset(n,E,c); mins=minimal_ands(n,c)
        gv=lambda A,B:[(v,b) for (v,b) in good if v in A|B]
        est=any(gv(A,B) for _,A,B in mins); st['L6']+=bool(good); st['E*']+=est
        st['E*b0']+=any(b==0 for _,A,B in mins for v,b in gv(A,B))
        for g,A,B in mins:
            typ='ovl' if A&B else ('star' if min(len(A),len(B))==1 else 'rect')
            st[typ]+=1; st[typ+'_good']+=bool(gv(A,B))
            if typ=='star':
                ctr=A if len(A)==1 else B
                if len(A)==1 and len(B)==1: st['star11']+=1; st['star11_good']+=bool(gv(A,B))
                else:
                    (a,)=ctr; st['ctr_good']+=any((a,b) in good for b in (0,1))
                    st['ctr_good_b0']+=((a,0) in good)
        if not est: print('  E*FAIL',fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(good),flush=True)
    print(n,len(E),'Phi',P,'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
