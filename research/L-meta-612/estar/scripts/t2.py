import sys, collections, time
from lib import *
nmin,nmax,X,lim=map(int,sys.argv[1:5]); shown=collections.Counter()
for n,E in graphs(nmin,nmax):
    P=phiE(E); t0=time.time()
    circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
    st=collections.Counter()
    for c in circs:
        good,sl=goodset(n,E,c); mins=minimal_ands(n,c)
        stars=[(g,A,B) if len(A)==1 else (g,B,A) for g,A,B in mins if not A&B and min(len(A),len(B))==1]
        if not stars:
            st['nostar']+=1; ok=any(v in A|B for g,A,B in mins for v,b in good); st['nostar_E*']+=ok
            if shown['ns']<3: shown['ns']+=1; print('  NOSTAR',ok,fmt(c),[(g,sorted(A),sorted(B)) for g,A,B in mins],sorted(good))
        for g,A,B in stars:
            (a,)=A
            if len(B)==1: continue
            if not any((a,b) in good for b in (0,1)):
                st['ctrfail']+=1
                lg=[(v,b) for v,b in good if v in B]
                if shown[str(E)]<2: shown[str(E)]+=1; print('  CTRFAIL a=%d B=%s'%(a,sorted(B)),fmt(c),'good',sorted(good),'slack a',sl[(a,0)],sl[(a,1)])
    print(n,len(E),'Phi',P,'#c',len(circs),dict(st),E,'%.0fs'%(time.time()-t0),flush=True)
