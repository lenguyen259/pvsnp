from common import *
def jt(n,E,pairs,cover):
    b=B(n)
    J=b.OR([b.g('&',a,c) for a,c in pairs])
    node={v:b.g('|',v,J) for v in range(n)}
    starcover(b,E,node,cover)
    return b.c
if __name__=="__main__":
  n=10;E=PET
  print('C4',has_c4(n,E),'tau',tau(E))
  r=analyze(n,jt(n,E,[(0,1),(2,3)],[0,2,4,6,7,8]),E)
  print({k:r[k] for k in ('ok','size','nor','nand','ch','slack')}); print(fmt(r['R']))
  # star cover check
  b=B(n); starcover(b,E,{v:v for v in range(n)},[0,2,4,6,7,8]); r=analyze(n,b.c,E)
  print('plain',{k:r[k] for k in ('ok','size','nor','nand','ch','slack')})
