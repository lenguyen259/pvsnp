import json,subprocess
from lib6 import *
from facts import facts
L=json.load(open('c601.json'))
for s_,cs in L:
    out=subprocess.run(['python3','enc6.py','6','0,1','--s',str(len(parse(cs))),'--nocanon','--timeout','60','--fix',cs,'--norun'],capture_output=True,text=True).stdout.strip().split('\n')[-1]
    if 'UNSAT' in out:
        print(cs)
        for fl in [['--norun','--noholder','--nolb','--nozr'],['--norun','--nolb','--nozr','--nodist'],['--norun','--noholder','--nozr'],['--norun','--noholder','--nolb'],['--norun','--nolb','--nozr']]:
            o=subprocess.run(['python3','enc6.py','6','0,1','--s',str(len(parse(cs))),'--nocanon','--timeout','60','--fix',cs]+fl,capture_output=True,text=True).stdout.strip().split('\n')[-1]
            print(fl,o)
