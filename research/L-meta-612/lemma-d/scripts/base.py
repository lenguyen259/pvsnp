import sys, collections, pickle, os
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb')
from tr import load, DIRS, breduce, counts, deg
PK='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemD/data.pkl'
def build():
    out=[]; seen=set()
    for fn,n,E,X,c in load(DIRS):
        key=(tuple(E),tuple(c))
        if key in seen: continue
        seen.add(key)
        sup=sorted({x for e in E for x in e})
        ds={v:deg(E,v) for v in sup}
        if min(ds.values())<2: continue
        R,T,o=breduce(n,c)
        # core of node q: {v: q<=x_v}
        xv={v:sum(1<<r for r in range(1<<n) if (r>>v)&1) for v in range(n)}
        core={}
        for q in list(range(n))+sorted(R):
            core[q]=frozenset(v for v in range(n) if T[q]&~xv[v]==0)
        ors={i:(j,k) for i,(op,j,k) in R.items() if op=='|'}
        ands={i:(j,k) for i,(op,j,k) in R.items() if op=='&'}
        chg={i:core[j]|core[k] for i,(j,k) in ors.items()}  # vertices charged at gate i
        out.append(dict(n=n,E=E,c=c,R=R,T=T,out=o,ds=ds,sup=sup,core=core,ors=ors,ands=ands,chg=chg,X=X,fn=fn))
    pickle.dump(out,open(PK,'wb'))
    return out
def get():
    if os.path.exists(PK): return pickle.load(open(PK,'rb'))
    return build()
def ch(d,v): return sum(1 for i in d['ors'] if v in d['chg'][i])
def QX(d,X): return sum(1 for i in d['ors'] if d['chg'][i]&X)
def eX(d,X): return sum(1 for a,b in d['E'] if a in X or b in X)
