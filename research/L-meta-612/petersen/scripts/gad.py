from common import *
from indep import check
n=10; b=B(n); g=b.g
o09=g('|',0,9); o59=g('|',5,9); o06=g('|',0,6); o56=g('|',5,6)
s4=g('&',4,g('|',3,o09)); s7=g('&',7,g('|',2,o59)); s1=g('&',1,g('|',2,o06))
t14=g('&',o09,o59); t21=g('&',o06,t14); gad=g('&',o56,g('|',8,t21))
s3=g('&',3,g('|',2,8))
b.OR([s4,s7,s1,gad,s3])
r=analyze(n,b.c,PET); s=fmt(r['R']); print(s); print(check(n,PET,s))
