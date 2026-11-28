import sys, json
from rup import *
m, n, k, f = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
L = 2 * m * n
pos = set()
for line in open(f):
    if line.startswith('v'):
        pos |= {int(x) for x in line.split()[1:] if int(x) > 0}
run = [frozenset(l for l in range(L) if s * L + l + 1 in pos) for s in range(k)]
print(show(run, n)); print('checker:', refutes(php(m, n), run, k))
json.dump([sorted(C) for C in run], open(f + '.json', 'w'))
