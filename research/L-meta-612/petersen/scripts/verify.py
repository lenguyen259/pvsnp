import sys, json
from common import *
E=[tuple(e) for e in json.loads(sys.argv[1])]; c=[tuple(x) for x in json.loads(sys.argv[2])]
n=max(max(e) for e in E)+1; r=analyze(n,c,E)
print({k:r[k] for k in ('ok','size','nor','nand','ch','deg','slack')}); print(fmt(r['R']))
