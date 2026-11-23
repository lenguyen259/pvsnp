import sys, json, glob, collections
sys.path.insert(0,'../s_case'); sys.path.insert(0,'../e612')
from cl import *
cnt=collections.Counter(); ex={}
def note(k,fn,c):
    cnt[k]+=1; ex.setdefault(k,(fn,fmt(c)))
files=sorted(glob.glob('circs/*.json'))
for fn in files:
    D=json.load(open(fn)); n=D['n']; E=[tuple(e) for e in D['E']]; ES={frozenset(e) for e in E}
    for c in D['circs']:
        c=[tuple(x) for x in c]; G,rd,need,dead=info(n,E,c); T=tts(n,c)
        sing=lambda p: frozenset(u for u in range(n) if (T[p]>>(1<<u))&1)
        pr=lambda p,u,v: (T[p]>>((1<<u)|(1<<v)))&1
        cnt['circ']+=1
        clean=True
        for i,o,j,k in c:
            S=sing(i)
            for u in range(n):
                for v in range(u+1,n):
                    if frozenset((u,v)) not in ES and u not in S and v not in S and pr(i,u,v): clean=False
            if o=='&':
                S1,S2=sing(j),sing(k)
                if S1&S2: note('AND_with_singleton',fn,c)
                if not (S1-S2) or not (S2-S1): note('AND_killer(side empty)',fn,c)
                if len(S1-S2)>=2 and len(S2-S1)>=2: note('AND_rect>=2x2',fn,c)
        if not clean: note('UNCLEAN',fn,c)
        good={vb for vb in need if len(dead[vb])>=need[vb]}
        ma=minimal_ands(n,c)
        for g,A,B in ma:
            if A&B: note('minAND_overlap',fn,c)
            elif min(len(A),len(B))>=2: note('minAND_rect',fn,c)
        st=stars(n,E,c,G,rd)
        okE=False
        for S in st:
            a=S['a']; B=set(S['B']); priv=S['priv']==S['T']
            if not B<=nbrs(E,a): note('star_B_notin_N(a)',fn,c)
            orr=[r for r in rd[a] if G[r][0]=='|']
            zs={p:sing(G[p][1] if G[p][2]==a else G[p][2]) for p in orr}
            att=all(any(zs[p] and zs[p]<=nbrs(E,cc) for p in orr) for cc in nbrs(E,a)-B)
            key=('star',S['cat'],'|B|=1' if len(B)==1 else '|B|>=2','priv' if priv else 'SHARED','ATT' if att else 'noATT')
            cnt[key]+=1; ex.setdefault(key,(fn,fmt(c)))
            thm = S['cat'] in('A1','A2') or (priv and att)
            if thm:
                assert (a,0) in good; okE=True
            if any((v,b) in good for v in {a}|B for b in (0,1)): cnt['starE*']+=1
            else: note('star_no_good_vertex',fn,c)
        if not okE: note('CIRC_no_star_proved_by_ThmAB',fn,c)
        # fanout of a: AND readers count
        for a in range(n):
            ar=[r for r in rd[a] if G[r][0]=='&']
            if len(ar)>=2: note('var_with_>=2_AND_readers',fn,c)
for k,v in sorted(cnt.items(),key=str): print(k,v)
print('--- examples')
for k,v in ex.items():
    if k not in ('circ',) : print(k,v)
print(len(files),'graphs')
