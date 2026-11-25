import json, sys, itertools, collections
sys.argv=['meas.py','5','[(0,1),(1,2),(2,3),(3,4),(4,0)]','1']
exec(open('meas.py').read().split("def downsets")[0])
res=json.load(open('req_c5.json'))
c=collections.Counter()
ex=[]
for X,Ys,Yn,L,m in res:
    X=frozenset(tuple(e) for e in X); mm=mu(X,frozenset(Ys),frozenset(tuple(p) for p in Yn))
    c[(L-mm)]+=1
    if L-mm>0 and len(ex)<10: ex.append((sorted(X),Ys,Yn,L,mm))
print(c); [print(e) for e in ex]
