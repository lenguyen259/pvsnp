from lib8 import *
st=collections.Counter(); bad=[]
for s_,d in allsrc():
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1; cert=cert2=False
    for nm,v,rho,need in g.options():
        if nm!='A': continue
        r=DV2(g,c,v)
        # theorem check: singok & single => |rest|<=kL
        if r['singok'] and r['single']:
            st['hyp23']+=1
            if len(r['rest'])>r['kL']: st['inj_viol']+=1; bad.append((d['c'],v,r))
        lb=r['F']+len(r['ND'])-r['pen']   # general bound F+|ND|-pen  (<= LD)
        if lb>r['LD']: st['lb_viol']+=1; bad.append(('lb',d['c'],v))
        if r['kZ']>=1 and r['pen']==0 and (len(r['rest'])==0 or (r['singok'] and r['single'])):
            cert2=True; st['cert2_pays']+= r['LD']>=need; st['cert2']+=1
            if r['LD']<need: bad.append(('c2',d['c'],v,r,need))
    st['circ_cert2']+=cert2
print(dict(st)); [print(b) for b in bad[:4]]
