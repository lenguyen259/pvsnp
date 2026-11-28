import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
import graphs, t3star, json
name,secs,K,seed,pool=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
print(json.dumps(t3star.search(name,secs,K,seed,pool,'N')),flush=True)
