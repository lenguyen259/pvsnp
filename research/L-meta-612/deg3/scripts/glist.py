import json,itertools
def has_c4(E):
    n=max(max(e) for e in E)+1; N=[set() for _ in range(n)]
    for a,b in E: N[a].add(b); N[b].add(a)
    return any(len(N[a]&N[b])>=2 for a in range(n) for b in range(a+1,n))
def theta(l1,l2,l3):
    E=[];nxt=[2]
    for l in (l1,l2,l3):
        prev=0
        for t in range(l-1):
            v=nxt[0]; nxt[0]+=1; E.append((prev,v)); prev=v
        E.append((prev,1))
    return E
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
def relabel(E):
    vs=sorted({x for e in E for x in e}); m={v:i for i,v in enumerate(vs)}
    return sorted(tuple(sorted((m[a],m[b]))) for a,b in E)
G={
 'tri+C5':[(0,2),(0,5),(1,2),(1,3),(2,3),(3,4),(4,5)],
 '2tri+bridge':[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)],
 'th233':theta(2,3,3),'th125':theta(1,2,5),'th333':theta(3,3,3),'th144':theta(1,4,4),
 '2tri+P2':[(0,1),(0,2),(1,2),(2,3),(3,4),(4,5),(4,6),(5,6)],
 'constrS7':[(0,1),(0,4),(0,5),(1,2),(1,4),(2,6),(3,5),(3,6),(5,6)],
 'P6':[(0,1),(1,2),(2,3),(3,4),(4,5)],
 'net':[(0,1),(1,2),(0,2),(0,3),(1,4),(2,5)],
 'C5+pend':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5)],
 'C5+2pend':[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(2,6)],
 'C6+2pend':[(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(3,7)],
 'spider':[(0,1),(1,2),(0,3),(3,4),(0,5),(5,6)],
 'C7':[(i,(i+1)%7) for i in range(7)],
 'Pet-v':relabel([e for e in PET if 0 not in e]),
 'Pet':PET,
}
for k,E in G.items():
    assert not has_c4(E),k
    d={}
    for a,b in E: d[a]=d.get(a,0)+1; d[b]=d.get(b,0)+1
    assert max(d.values())<=3,k
if __name__=='__main__':
    for k,E in G.items(): print(k,json.dumps(E))
