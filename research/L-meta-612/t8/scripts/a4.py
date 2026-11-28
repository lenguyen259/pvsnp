from lib8 import *
st=collections.Counter(); ex=[]
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1; R=readers(c); gate={x[0]:x for x in c}
    for nm,v,rho,need in g.options():
        Z,L,I,aI,F,exc=zone(g,c,rho); ld=LD(g,c,rho)
        st['opt']+=1
        if ld!=F+aI+exc: st['IDfail']+=1; ex.append((d['c'],nm,v,ld,F,aI,exc))
        if nm=='A':
            kor=sum(1 for r in R[v] if gate[r][1]=='|')
            if kor==0:
                st['kor0']+=1; st['kor0_ok']+= ld>=len(g.N[v])+1; st['kor0_need']+= ld>=need
                if ld<need and len(ex)<6: ex.append(('C1',d['g'],d['E'],d['c'],v,ld,need,F,aI,exc))
print(dict(st)); [print(e) for e in ex[:8]]
