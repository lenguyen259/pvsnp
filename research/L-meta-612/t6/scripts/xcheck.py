import subprocess,sys,json,collections
from facts import facts
from lib6 import *
tests=[('6','0,1',12,['7,0']),('6','0,1',12,['6,1']),('6','0,1',12,['6,2']),('6','0,1',12,['6,2','7,2']),('6','0,3',12,['6,1']),('6','0,3',12,['6,5','7,4']),('5','0,1,2',12,['6,0']),('5','0,1,2',12,['5,4','7,3']),('6','0,1',11,['6,5'])]
for n0,S,s,fz in tests:
    args=['python3','enc6.py',n0,S,'--s',str(s),'--noholder','--norun','--nolb','--nozr','--nodist','--timeout','100']
    for x in fz: args+=['--forcezw',x]
    o=subprocess.run(args,capture_output=True,text=True).stdout
    line=[l for l in o.split('\n') if l.startswith('VERIFIED')]
    if not line: print(n0,S,fz,'no circuit',o.strip().split('\n')[-1]); continue
    cs=line[0].split(' ',1)[1]
    F=facts(int(n0),[int(x) for x in S.split(',')],cs)
    res={}
    for fact in ('holder','run','lb','zr'):
        others=['--no'+k for k in ('holder','run','lb','zr') if k!=fact]
        o2=subprocess.run(['python3','enc6.py',n0,S,'--s',str(s),'--nocanon','--nodist','--timeout','60','--fix',cs]+others,capture_output=True,text=True).stdout.strip().split('\n')[-1].split()[1]
        res[fact]=(F[fact],o2,'OK' if (o2=='SAT')==F[fact] else 'MISMATCH')
    print(n0,S,fz,cs,res)
