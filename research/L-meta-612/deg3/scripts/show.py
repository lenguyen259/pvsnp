import json,sys
for l in open(sys.argv[1]):
    p=l.split(' ',1)
    if len(p)<2 or not p[1].startswith('{'): print(l[:100].strip()); continue
    d=json.loads(p[1]); print(p[0],d['target'],'K',d['K'],'it',d['it'],'best',d['best'],d['found'][:1])
