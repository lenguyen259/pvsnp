import subprocess,sys,json,collections,random
from facts import facts
from lib6 import *
cand=[]
for l in open('../t3/locpool.jsonl'):
    D=json.loads(l)
    if not D['g'].startswith('psun'): continue
    _,n,S=D['g'].split(':'); E,L=psun(int(n),[int(x) for x in S.split(',')]); g=Graph(E); c=parse(D['c'])
    if struct(g,c,sorted(L),L)>=2: cand.append((n,S,D['c']))
random.seed(1); random.shuffle(cand); print(len(cand))
st=collections.Counter(); zwc=0
for n,S,cs in cand[:int(sys.argv[1])]:
    Sh=[int(x) for x in S.split(',')]; F=facts(int(n),Sh,cs)
    E,L=psun(int(n),Sh); c=parse(cs)
    zx=any(any(x[1]=='|' and v in x[2:] and (x[2] if x[3]==v else x[3])<int(n) for x in c) for v in L)
    zwc+=zx
    for fact in ('holder','run','lb','zr'):
        others=['--no'+k for k in ('holder','run','lb','zr') if k!=fact]
        o2=subprocess.run(['python3','enc6.py',n,S,'--s',str(len(c)),'--nocanon','--nodist','--timeout','60','--fix',cs]+others,capture_output=True,text=True).stdout.strip().split('\n')[-1].split()[1]
        st[(fact,F[fact],o2,zx)]+=1
print('z=input cases',zwc); 
for k in sorted(st,key=str): print(k,st[k])
