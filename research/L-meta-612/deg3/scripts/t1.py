import collections,sys
from lib import *
st=collections.Counter(); ex=collections.defaultdict(list)
cache={}
for n,E,c in data():
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    k=tuple(E)
    if k not in cache:
        P=phi(E); t=tau(E)
        cache[k]={v:(P-phi([e for e in E if v not in e]), t-tau([e for e in E if v not in e]) if [e for e in E if v not in e] else t, deg[v]-(0 if [e for e in E if v not in e] else 0)) for v in sup}
    need=cache[k]
    R,T,o=red(n,c); a0,o0=cnt(R)
    sv={}
    for v in sup:
        R1,_,_=red(n,c,{v:0}); a1,o1=cnt(R1)
        sv[v]=(a0-a1,o0-o1)
    Gv={v:[e for e in E if v not in e] for v in sup}
    needor={v:deg[v]-(0 if Gv[v] else 1) for v in sup}
    st['n']+=1
    tot=[v for v in sup if sum(sv[v])>=need[v][0]]
    st['T1 tot']+=bool(tot)
    orr=[v for v in sup if sv[v][1]>=needor[v]]
    st['T2 or']+=bool(orr)
    andd=[v for v in sup if sv[v][0]>=need[v][1]]
    st['T3 and']+=bool(andd)
    # minimal OR gates
    def cone(q,acc):
        if q in R and q not in acc: acc.add(q); cone(R[q][1],acc); cone(R[q][2],acc)
        return acc
    ors=[i for i in R if R[i][0]=='|']; ands=[i for i in R if R[i][0]=='&']
    def supp(q): # variables in cone
        s=set(); st2=[q]; vis=set()
        while st2:
            x=st2.pop()
            if x in vis: continue
            vis.add(x)
            if x in R: st2+= [R[x][1],R[x][2]]
            else: s.add(x)
        return s
    minor=[g for g in ors if not any(R[h][0]=='|' for h in cone(R[g][1],set())|cone(R[g][2],set()))]
    minand=[g for g in ands if not any(R[h][0]=='&' for h in cone(R[g][1],set())|cone(R[g][2],set()))]
    st['T4 everyminOR has orgood']+=all(supp(g)&set(orr) for g in minor)
    st['T4b someminOR has orgood']+=any(supp(g)&set(orr) for g in minor)
    st['T5 everyminAND tot']+=all(supp(g)&set(tot) for g in minand)
    st['T5b someminAND tot']+=any(supp(g)&set(tot) for g in minand)
    md=min(deg.values())
    st['T6 mindeg orgood']+=any(deg[v]==md for v in orr)
    for nm,ok in [('T1',tot),('T2',orr),('T3',andd)]:
        if not ok and len(ex[nm])<3: ex[nm].append((E,c))
    if not all(supp(g)&set(orr) for g in minor) and len(ex['T4'])<3: ex['T4'].append((E,c,sv))
    if not any(deg[v]==md for v in orr) and len(ex['T6'])<3: ex['T6'].append((E,c,sv))
print(dict(st))
for k,v in ex.items():
    for e in v: print(k,e)
