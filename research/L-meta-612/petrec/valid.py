import json,subprocess,sys
from chain import normal
from lib import *
txt=sys.argv[1]; fam=sys.argv[2] if len(sys.argv)>2 else 'A2,N,B,B1,BB'
c=[]
for tok in txt.split():
    g,ex=tok.split('=')
    for o in '&|':
        if o in ex: a,b=map(int,ex.split(o)); c.append([o,min(a,b),max(a,b)])
c=normal(c); s=len(c)
R=restrictions(PET,fam.split(','))
L=lambda h: 0 if h is None else info(h)['phi']
rest=[[S0,S1,s-((F-1) if Hc is None else F+L(Hc))] for S0,S1,F,Hc in R]
rest=[r for r in rest if r[2]<s]
cmd=['python3','enc4.py',str(s),'--chain','--factc','--rest',json.dumps(rest),'--fix',json.dumps(c)]+sys.argv[3:]
out=subprocess.run(cmd,capture_output=True,text=True).stdout
print(out[-600:])
