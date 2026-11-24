import subprocess,sys,json,collections,random
from facts import facts
from lib6 import *
def canon(n0,P,c):
    gv={}
    for i,o,j,k in c:
        if o=='|' and (j in P or k in P): gv[i]=(j if j in P else k, k if j in P else j)
    gates={i:(o,j,k) for i,o,j,k in c if i not in gv}
    def base(x): return gv[x][1] if x in gv else x
    dep={u:0 for u in range(n0)}
    for i,o,j,k in c:
        if i in gv: continue
        dep[i]=1+max(dep[base(j)],dep[base(k)])
    pos={u:u for u in range(n0)}; order=[]
    for d in sorted(set(dep[i] for i in gates)):
        layer=[i for i in gates if dep[i]==d]
        key=lambda i:(tuple(sorted((pos[base(gates[i][1])],pos[base(gates[i][2])]))),0 if gates[i][0]=='&' else 1)
        layer.sort(key=key)
        for i in layer: pos[i]=n0+len(order); order.append(i)
    # emit C in this order with g's before their reader
    out=[]; nm={u:u for u in range(n0)}; nm.update({v:v for v in P}); nxt=max(P)+1
    for i in order:
        o,j,k=gates[i]; ins=[]
        for x in (j,k):
            if x in gv:
                v,z=gv[x]; out.append((nxt,'|',v,nm[z])); ins.append(nxt); nxt+=1
            else: ins.append(nm[x])
        out.append((nxt,o,ins[0],ins[1])); nm[i]=nxt; nxt+=1
    return out
cand=[]
for l in open('../t3/locpool.jsonl'):
    D=json.loads(l)
    if not D['g'].startswith('psun'): continue
    _,n,S=D['g'].split(':'); E,L=psun(int(n),[int(x) for x in S.split(',')]); g=Graph(E); c=parse(D['c'])
    if struct(g,c,sorted(L),L)>=2: cand.append((n,S,D['c']))
random.seed(2); random.shuffle(cand); st=collections.Counter()
for n,S,cs in cand[:int(sys.argv[1])]:
    Sh=[int(x) for x in S.split(',')]; E,L=psun(int(n),Sh); g=Graph(E); c=parse(cs)
    c2=canon(int(n),sorted(L),c); assert tables(g,c2,{})[c2[-1][0]]==g.f
    F=facts(int(n),Sh,fmt(c2))
    o2=subprocess.run(['python3','enc6.py',n,S,'--s',str(len(c)),'--nodist','--timeout','60','--fix',fmt(c2)]+['--no'+k for k in F if not F[k]],capture_output=True,text=True).stdout.strip().split('\n')[-1].split()[1]
    st[o2]+=1
print(st)
