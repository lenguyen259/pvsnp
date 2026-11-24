import itertools
def key_rows(n,E):
    f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
    T=[(1<<a)|(1<<b) for a,b in E]
    F=[r for r in range(1<<n) if not f(r) and all(f(r|(1<<v)) for v in range(n) if not (r>>v)&1)]
    D=[((1<<n)-1)^(1<<v) for v in range(n)]
    return T,F,D
if __name__=='__main__':
    from common import PET
    T,F,D=key_rows(10,PET); print(len(T),len(F),len(D))
