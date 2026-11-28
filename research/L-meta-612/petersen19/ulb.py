# print the lexbot-canonical U circuit for a graph
import json,sys
from plib import lexbot_form
from mku import ucirc
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
E=[tuple(e) for e in json.loads(sys.argv[1])]; n=max(max(e) for e in E)+1
G=nx.Graph(E); G.add_nodes_from(range(n)); Au=[[m[i] for i in range(n)] for m in GraphMatcher(G,G).isomorphisms_iter()]
c=ucirc(E); print(len(c)); print(json.dumps(lexbot_form(c,Au,n)))
