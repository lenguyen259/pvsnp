"""generalized options: rho = (S0,S1); need = Phi(G) - LB(f|rho) via Fact F."""
import sys
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import *
def gneed(g,S0,S1):
    S0=set(S0); S1=set(S1)
    if any(b in S1 for a in S1 for b in g.N[a]): return None
    F=set().union(*[g.N[a] for a in S1]) - S0 - S1 if S1 else set()
    H=g.Eminus(S0|S1|F)
    if not F and not H: return None
    if F: LB=len(F)+phi(H) if H else len(F)-1
    else: LB=phi(H)
    return g.P-LB
def gopt(g,c,S0,S1):
    nd=gneed(g,S0,S1)
    if nd is None: return None
    rho={x:0 for x in S0}; rho.update({x:1 for x in S1})
    e=elim(g,c,rho); return e,nd,e>=nd
