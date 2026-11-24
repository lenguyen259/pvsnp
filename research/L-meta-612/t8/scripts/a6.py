from lib8 import *
C=["6=0|3 7=4|5 8=6&7 9=5|8 10=2|8 11=1|4 12=11&9 13=3|12 14=10&13 15=14|12",
"6=0|3 7=3|4 8=2|5 9=7&8 10=4|9 11=1|9 12=10&6 13=5|12 14=11&13 15=12|14"]
g=Graph([(0, 4), (1, 5), (2, 3), (3, 4), (3, 5), (4, 5)])
for s in C:
    c=parse(s); print(s)
    for nm,v,rho,need in g.options():
        lr=LR(g,c,rho); 
        if lr<need: continue
        K,Cp,Dd=decomp(g,c,rho); surv=ruleR(g,c,rho); T=tables(g,c,rho); fo=T[c[-1][0]]
        tp=[x[0] for x in surv if T[x[0]]==fo]
        print(nm,v,'need',need,'K',sorted(K),'Cp',sorted(Cp),'Dead',sorted(Dd),'ruleR-elim',len(c)-len(surv),'Top among surv',tp)
