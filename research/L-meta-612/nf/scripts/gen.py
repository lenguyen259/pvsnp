import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from lib import graphs
import json
for n,E in graphs(2,int(sys.argv[1])): print(json.dumps(E))
