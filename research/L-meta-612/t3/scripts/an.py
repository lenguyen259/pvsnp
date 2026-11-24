import json,sys,collections
pool=sys.argv[1]; C=collections.Counter(); n=0; sizes=collections.Counter()
for l in open(pool):
    D=json.loads(l); n+=1; sizes[D['s']]+=1
    for k in set((a,v) for a,v,e,nd in D['good']): C[k]+=1
print(n,dict(sizes))
for k,v in sorted(C.items()): print(k,v)
