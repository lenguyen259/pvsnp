from lib7 import *
import t3fuzz, graphs, time
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); fails=[]
extra=[('Pet-v',"9=4|2 10=4|1 11=10|8 12=8|2 13=3&12 14=7|8 15=14|0 16=5&15 17=6&11 18=7&9 19=16|18 20=1|19 21=19|13 22=2|0 23=20&22 24=23|17 25=21|24"),
 ('Pet',"10=1|5 11=10|4 12=0&11 13=3|7 14=1|13 15=2&14 16=8|1 17=16|9 18=6&17 19=8|4 20=3&19 21=4|7 22=9&21 23=7|8 24=5&23 25=18|20 26=25|12 27=26|24 28=15|22 29=28|27")]
src=[(n,{'E':t3fuzz.GR[n],'c':s,'g':n}) for n,s in extra]+list(pools())
for s_,d in src:
    if time.time()-t0>secs: break
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1
    ok_=any(LR(g,c,rho)>=need for nm,v,rho,need in g.options())
    st['LR']+=ok_
    if not ok_: fails.append((d.get('g'),d['c']))
print(dict(st)); print(fails[:3])
