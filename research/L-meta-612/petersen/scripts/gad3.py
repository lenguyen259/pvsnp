from common import *
from indep import check
# a0 b1 c2 d3 h1=4 (a,c) h2=5 (b,c) h3=6 (a,d) h4=7 (b,d)
def run(n,E,with_h4):
    b=B(n); g=b.g
    ac=g('|',0,2); bc=g('|',1,2); ad=g('|',0,3); bd=g('|',1,3)
    s4=g('&',4,ac); s5=g('&',5,bc); s6=g('&',6,ad)
    t=g('&',ac,bc); t=g('&',ad,t)
    gad=g('&',bd,g('|',7,t)) if with_h4 else g('&',bd,t)
    b.OR([s4,s5,s6,gad])
    r=analyze(n,b.c,E); s=fmt(r['R']); print('C4',has_c4(n,E),'|E|',len(E),'tau',tau(E)); print(s); print(check(n,E,s))
E8=[(0,1),(2,3),(0,4),(2,4),(1,5),(2,5),(0,6),(3,6),(1,7),(3,7)]
run(8,E8,True)
E7=[(0,1),(2,3),(0,4),(2,4),(1,5),(2,5),(0,6),(3,6)]
run(7,E7,False)
