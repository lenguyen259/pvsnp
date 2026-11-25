# known size-20 Petersen circuits (verified on all inputs below)
from plib import *
U=[["|", 0, 2], ["|", 0, 7], ["|", 0, 9], ["|", 2, 4], ["|", 2, 9], ["|", 8, 9], ["&", 4, 12], ["|", 6, 10], ["&", 6, 15], ["&", 7, 14], ["|", 8, 11], ["|", 8, 13], ["&", 1, 17], ["&", 3, 21], ["&", 5, 20], ["|", 22, 23], ["|", 16, 25], ["|", 24, 26], ["|", 18, 27], ["|", 19, 28]]
OR13=parse("10=0|9 11=5|9 12=0|6 13=5|6 14=3|10 15=4&14 16=2|11 17=7&16 18=2|12 19=1&18 20=10&11 21=12&20 22=8|21 23=13&22 24=2|8 25=3&24 26=15|17 27=26|19 28=27|23 29=28|25")
def renum(txt,n=10):
    d={}
    for tok in txt.split():
        g,rhs=tok.split('='); o='&' if '&' in rhs else '|'; a,b=map(int,rhs.split(o)); d[int(g)]=(o,a,b)
    m={i:i for i in range(n)}; c=[]
    for g in sorted(d):
        o,a,b=d[g]; c.append([o,m[a],m[b]]); m[g]=n+len(c)-1
    return c
OR13b=renum("10=0|9 11=5|9 12=0|6 13=3&8 14=10&11 15=5|6 16=7&11 17=1&12 18=3|10 19=4&18 20=2|16 21=12&14 23=1|3 25=7|23 26=13|20 28=25&26 29=8|21 30=17|28 31=15&29 32=19|30 33=31|32")
KNOWN={'U':U,'OR13':OR13,'OR13b':OR13b}
def symb_form(c):
    for p in auts():
        cc=canon(relabel(c,p))
        if symb_ok(cc): return cc,p
if __name__=='__main__':
    import json
    for k,c in KNOWN.items():
        print(k,len(c),verify(c),sum(o=='&' for o,_,_ in c))
        cc,p=symb_form(c); print(' symb form',json.dumps(cc),verify(cc))
        json.dump(cc,open('known_%s.json'%k,'w'))
