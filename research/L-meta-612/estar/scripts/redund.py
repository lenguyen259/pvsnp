import re,sys
def parse(s):
    c=[]
    for tok in s.split():
        m=re.match(r'(\d+)=(\d+)([&|])(\d+)',tok); i,j,o,k=m.groups(); c.append((int(i),o,int(j),int(k)))
    return c
def tts(n,c):
    T={}
    for v in range(n): T[v]=sum(1<<r for r in range(1<<n) if (r>>v)&1)
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    return T
def redundant(n,c):
    T=tts(n,c); seen={}
    for x,t in T.items():
        if t in seen: return (seen[x] if False else (seen[t],x))
        seen[t]=x
    return None
if __name__=='__main__':
    n=int(sys.argv[1])
    for line in open(sys.argv[2]):
        if 'E*FAIL' in line:
            c=parse(line.split('E*FAIL')[1].split('[')[0]); print(redundant(n,c), line.split('[')[0].strip())
