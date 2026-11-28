from lib8 import *
import time
st=collections.Counter(); fails=[]; t0=time.time()
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1
    opts=g.options(); okLD=okLR=False; okA=False
    for nm,v,rho,need in opts:
        ld=LD(g,c,rho); lr=LR(g,c,rho)
        if ld>lr: st['LD>LR!']+=1
        if ld>=need: okLD=True; 
        if ld>=need and nm=='A': okA=True
        if lr>=need: okLR=True
    st['LD']+=okLD; st['LR']+=okLR; st['LD_A']+=okA
    if not okLD and len(fails)<5: fails.append((d.get('g'),d['E'],d['c']))
print(dict(st),time.time()-t0); [print(f) for f in fails]
