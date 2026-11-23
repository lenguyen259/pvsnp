import sys
exec(open('run4.py').read().split('maxn=int')[0])
exec('def minimal_ands'+open('run7.py').read().split('def minimal_ands')[1].split('maxn=int')[0])
E=[(0, 4), (1, 5), (2, 3), (3, 4), (3, 5), (4, 5)]; n=6; P=phiG(E)
circs=exists_circuit(n,target_tt(n,E),P,enum_all=3000)
print(len(circs))
for c in circs:
    good={(v,b) for v in range(n) for b in (0,1) if restrict(n,c,v,b)<=(phi0(E,v) if b==0 else phi1(E,v))}
    mins=minimal_ands(n,c)
    if not all(any(v in A|B for (v,b) in good) for (A,B) in mins):
        print(c); print('  mins',[(set(A),set(B)) for A,B in mins],' good',sorted(good))
