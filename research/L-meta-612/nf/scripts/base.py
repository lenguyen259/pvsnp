import sys, json, glob, collections
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
sys.path.insert(0,SC+'/e612')
from lib import phiE, tauE, fmt
import networkx as nx
def tts(n,c):
    T={}
    for u in range(n): T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
def sing(n,T):
    return {p:frozenset(u for u in range(n) if (T[p]>>(1<<u))&1) for p in T}
def pairs(n,T,S):
    # accepted non-singleton pairs (u,v not in S)
    P={}
    for p in T:
        P[p]=frozenset(frozenset((u,v)) for u in range(n) for v in range(u+1,n) if u not in S[p] and v not in S[p] and (T[p]>>((1<<u)|(1<<v)))&1)
    return P
def load(dirs):
    for d in dirs:
        for fn in sorted(glob.glob(d+'/*.json')):
            D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]
            g5 = nx.girth(nx.Graph(E))>=5
            for c in D['circs']:
                yield fn,n,E,D.get('X',0),g5,[tuple(x) for x in c]
DIRS=[SC+'/s_case/circs',SC+'/tf/circs']
