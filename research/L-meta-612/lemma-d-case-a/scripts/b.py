import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemD')
import base, collections
L=base.get()
def casea(d):
    ds=d['ds']; return min(ds.values())==2 and sum(1 for x in ds.values() if x>=3)>=2
