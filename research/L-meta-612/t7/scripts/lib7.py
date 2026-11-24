import sys,json,collections
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an4 import *   # Graph, parse, tables, LT, firstorder_sets, load, elim, phi, tau
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
POOLS=[SC+'/t3/locpool.jsonl',SC+'/t5/pool.jsonl',SC+'/t5/pool2.jsonl']
def pools(files=POOLS):
    for fn in files:
        for d in load([fn]): yield fn.split('/')[-1],d
def parts(g,c,rho):
    K,cp,T=firstorder_sets(g,c,rho); fo=T[c[-1][0]]
    Tp={i for i,o,j,k in c if T[i]==fo}
    return K,cp,Tp,T
from t2lib import ruleR
def LR(g,c,rho):
    """syntactic rule R (constants, copies, dead) + Top merge among survivors"""
    surv=ruleR(g,c,rho)
    if not surv: return len(c)
    T=tables(g,c,rho); fo=T[c[-1][0]]
    tp=sum(1 for x in surv if T[x[0]]==fo)
    return len(c)-len(surv)+max(tp-1,0)
