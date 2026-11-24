import sys
sys.path.insert(0,'../core')
from h1 import red, parse
from lib import tau,phi
E=[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)]; n=6
c=parse(sys.argv[1]) if len(sys.argv)>1 else parse('6=2|4 7=5|2 8=1|0 9=3|5 10=6&8 11=3|10 12=11&7 13=4|12 14=0|12 15=9&13 16=1|2 17=14&16 18=17|15')
R,T=red(n,c)
full=sum(1<<r for r in range(1<<n) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
print('correct',T[c[-1][0]]==full,'size',len(R),'nand',sum(1 for g in R.values() if g[0]=='&'))
for v in range(n):
    R1,T1=red(n,c,{v:0})
    print(v,'AND after',sum(1 for g in R1.values() if g[0]=='&'),'OR after',sum(1 for g in R1.values() if g[0]=='|'))
print('tau',tau(E),'phi',phi(E))
