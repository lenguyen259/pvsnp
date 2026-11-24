import sys,json
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from psun import psun
from t2lib import phi
def G(name):
    if name=='net+C3':
        E,_=psun(3,[0,1,2]); return E+[(6,7),(7,8),(6,8)]
    n,S=name.split(':'); return psun(int(n),[int(x) for x in S.split(',')])[0]
if __name__=='__main__':
    E=G(sys.argv[1]); print(json.dumps(E), phi(E))
