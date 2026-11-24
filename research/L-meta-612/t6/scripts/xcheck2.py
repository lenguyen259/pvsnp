import subprocess,sys,json,collections
from facts import facts
from lib6 import *
tests=[('6','0,1',13,['6,5']),('6','0,1',13,['7,2']),('6','0,3',13,['6,1']),('6','0,3',13,['6,5','7,4']),('5','0,1,2',13,['5,4']),('5','0,1,2',13,['7,3']),('6','0,1',13,['6,1']),('5','0,1,2',13,['6,0']),('6','0,1',12,['6,5'])]
for n0,S,s,fz in tests:
    args=['python3','enc6.py',n0,S,'--s',str(s),'--nolb','--nozr','--nodist','--timeout','200']
    for x in fz: args+=['--forcezw',x]
    o=subprocess.run(args,capture_output=True,text=True).stdout
    line=[l for l in o.split('\n') if l.startswith('VERIFIED')]
    if not line: print(n0,S,fz,'no circuit',o.strip().split('\n')[-1]); continue
    cs=line[0].split(' ',1)[1]
    F=facts(int(n0),[int(x) for x in S.split(',')],cs)
    o2=subprocess.run(['python3','enc6.py',n0,S,'--s',str(s),'--nocanon','--nodist','--timeout','60','--fix',cs]+['--no'+k for k in F if not F[k]],capture_output=True,text=True).stdout.strip().split('\n')[-1].split()[1]
    print(n0,S,fz,cs,F,o2)
