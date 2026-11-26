import json,re,itertools
d=json.load(open('/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/got18173.json'))
s=d['gap']['statement']
terms=[frozenset(int(a) for a in re.findall(r'x (\d+)',t)) for t in re.findall(r'\(([^()]*)\)',s[s.index('!'):])]
N=15;M=1<<N
def var(i):
    # truth table int, bit idx = input value, x_i = bit i of index
    t=0
    blk=((1<<(1<<i))-1)<<(1<<i) # pattern
    # build via doubling
    p=(1<<(1<<i))-1; p<<= (1<<i)   # period 2^(i+1): low half 0, high half 1
    L=1<<(i+1); t=p
    while L<M: t|=t<<L; L<<=1
    return t
X=[var(i) for i in range(N)]
FULL=(1<<M)-1
def target():
    o=0
    for t in terms:
        a=FULL
        for i in t:a&=X[i]
        o|=a
    return FULL^o
