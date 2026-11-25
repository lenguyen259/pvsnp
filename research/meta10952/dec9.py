# decode a kissat model and verify on all 512 inputs
import sys, json
info=json.load(open(sys.argv[1])); M=set()
for line in open(sys.argv[2]):
    if line.startswith('v'): M|={int(v) for v in line.split()[1:] if int(v)>0}
n,s=info['n'],info['s']
E=[(0,4),(1,5),(0,6),(2,6),(1,7),(3,7),(5,7),(2,8),(3,8),(4,8),(7,8)]
g=[]
for i in range(s):
    a=[j for j,v in enumerate(info['sa'][i]) if v in M][0]; b=[j for j,v in enumerate(info['sb'][i]) if v in M][0]
    op='NOT' if info['isn'][i] in M else ('AND' if info['isa'][i] in M else 'OR'); g.append((op,a,b))
ok=True
for t in range(1<<n):
    w=[(t>>j)&1 for j in range(n)]
    for op,a,b in g: w.append(1-w[a] if op=='NOT' else (w[a]&w[b] if op=='AND' else w[a]|w[b]))
    ok &= w[-1]==int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
print('gates',s,'verified on all 512 inputs:',ok); print(g)
