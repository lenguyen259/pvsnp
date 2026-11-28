import sys, json, glob, collections
sys.path.insert(0,'../s_case'); sys.path.insert(0,'../e612')
from cl import tts
from lib import phiE, tauE, fmt
def check(n,E,c):
    ES={frozenset(e) for e in E}; T=tts(n,c)
    S={p:frozenset(u for u in range(n) if (T[p]>>(1<<u))&1) for p in T}
    fail=[]
    for i,o,j,k in c:
        if o=='&':
            A,B=S[j],S[k]
            if A&B: fail.append('sing')
            if not (A-B) or not (B-A): fail.append('killer')
            if any(frozenset((u,v)) not in ES for u in A-B for v in B-A): fail.append('junk')
    if fail: return sorted(set(fail)),None
    # counts
    m=sum(1 for x in c if x[1]=='&')
    M=sum(1 for i,o,j,k in c if o=='|' and S[j] and S[k] and len(S[i])>=2)
    Z=sum(1 for i,o,j,k in c if o=='|' and (not S[j] or not S[k]))
    t=tauE(E)
    assert m>=t and M>=len(E)-m and Z>=m-1 and len(c)>=len(E)+t-1,(m,M,Z)
    return [], (m-t, M-(len(E)-m), Z-(m-1), len(c)-m-M-Z)
for d in sys.argv[1:]:
    cnt=collections.Counter(); ex={}
    for fn in sorted(glob.glob(d+'/*.json')):
        D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
        if D.get('X',0): continue
        import networkx as nx
        g5= nx.girth(nx.Graph(E))>=5
        tot=0; sa=0
        for c in D['circs']:
            c=[tuple(x) for x in c]; f,sl=check(n,E,c); tot+=1
            if not f: sa+=1; cnt[('slack',g5)+sl]+=1
            else: cnt[('fail',g5)+tuple(f)]+=1; ex.setdefault(('fail',g5)+tuple(f),(fn,fmt(c)))
        cnt[('graphs_g5' if g5 else 'graphs_tri', 'all' if sa==tot else ('some' if sa else 'NONE'))]+=1
    print(d); [print(' ',k,v) for k,v in sorted(cnt.items(),key=str)]
    [print('  ex',k,v) for k,v in ex.items()]
