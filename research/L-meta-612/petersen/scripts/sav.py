# OR-savings of restriction x_v:=0 (with reduction), and AND savings
import sys, re, json
from common import *
def parse(s):
    c=[]
    for t in s.split():
        m=re.match(r'(\d+)=(\d+)([&|])(\d+)$',t); c.append((int(m[1]),m[3],int(m[2]),int(m[4])))
    return c
def sav(n,E,c):
    R,_,_=breduce(n,c); a0,o0=counts(R)
    out={}
    for v in range(n):
        Rv,_,_=breduce(n,c,dead=(v,)); a,o=counts(Rv); out[v]=(o0-o,a0-a)
    return out
def counts(R):
    a=sum(1 for g in R.values() if g[0]=='&'); return a,len(R)-a
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])]; n=max(max(e) for e in E)+1
    s=sav(n,E,parse(sys.argv[2])); deg={v:sum(1 for e in E if v in e) for v in range(n)}
    print('ORsav',{v:s[v][0] for v in s},'deg',deg,'vertices with ORsav>=deg',[v for v in s if s[v][0]>=deg[v]])
