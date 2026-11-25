import re,sys,collections
res={}
for l in open('results.log'):
    m=re.search(r'job (\S+) nrest \d+ (.*)',l)
    if m:
        r='UNSAT' if 'RESULT UNSAT' in m.group(2) else ('SAT' if 'RESULT SAT' in m.group(2) else ('TIMEOUT' if 'TIMEOUT' in m.group(2) else 'ERR'))
        res[m.group(1)]=r
ids=[l.split('\t')[0] for l in open('jobs.txt') if l.strip()]
grp=collections.defaultdict(collections.Counter)
for i in ids:
    g='_'.join(i.split('_')[:1]); grp[g][res.get(i,'pending')]+=1
for g,c in grp.items(): print(g,dict(c))
for i,r in res.items():
    if r in('SAT','ERR'): print('!!',i,r)
