import json,sys,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import Graph
stats=collections.Counter(); ex={}
for pool in sys.argv[1:]:
  for l in open(pool):
    D=json.loads(l); E=[tuple(e) for e in D['E']]; g=Graph(E)
    good={(a,v) for a,v,e,nd in D['good']}
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        loc={'Nv':('N',v) in good,'Au':('A',u) in good,'Bu':('B',u) in good,'Bv':('B',v) in good,'Nu':('N',u) in good}
        Nu_minus=[w for w in g.N[u] if w!=v]
        loc['nbr']=any((a,w) in good for w in Nu_minus for a in 'ANB')
        pat=''.join(k for k in ['Nv','Au','Bu','Bv','Nu','nbr'] if loc[k])
        stats[pat]+=1
        for k in loc:
            if not loc[k]: stats['not_'+k]+=1
        if not (loc['Nv'] or loc['Au'] or loc['Bu'] or loc['Bv']):
            stats['FAIL_local4']+=1; ex.setdefault('local4',(D['s'],D['g'],D['c'],v))
        if not (loc['Nv'] or loc['Bu']): stats['FAIL_NvBu']+=1; ex.setdefault('NvBu',(D['s'],D['g'],D['c'],v))
        if not (loc['Nv'] ): stats['FAIL_Nv']+=1; ex.setdefault('Nv',(D['s'],D['g'],D['c'],v))
        stats['leafinst']+=1
for k,v in sorted(stats.items()): print(k,v)
for k,v in ex.items(): print(k,v)
