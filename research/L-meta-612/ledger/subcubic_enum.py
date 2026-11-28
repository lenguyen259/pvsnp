"""Enumerate connected C4-free graphs of maximum degree <= 3 (n <= NMAX) and classify them for
subcubic.md: pseudoforest (Theorem PF), max degree 2 (Theorem F2), Theorem F class (<= 1 vertex of
degree 3; OR half only), exact Phi SAT-verified (n <= 6 sweep, 7-vertex sweep s7.txt, petersen19
hierarchy), or open. Writes subcubic_graphs.json.  Usage: python3 -I subcubic_enum.py [NMAX=9]
"""
import sys, os, json, ast
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib612 import *

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9


def creates_c4(G, S):
    S = list(S)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if set(G[S[i]]) & set(G[S[j]]):
                return True
    return False


def gen():
    levels = {1: [nx.empty_graph(1)]}
    for n in range(2, NMAX + 1):
        buckets = {}
        out = []
        for H in levels[n - 1]:
            free = [v for v in H if H.degree(v) < 3]
            for k in (1, 2, 3):
                for S in itertools.combinations(free, k):
                    if creates_c4(H, S):
                        continue
                    G = H.copy()
                    G.add_node(n - 1)
                    G.add_edges_from((n - 1, s) for s in S)
                    h = nx.weisfeiler_lehman_graph_hash(G, iterations=4)
                    L = buckets.setdefault(h, [])
                    if any(nx.is_isomorphic(G, F) for F in L):
                        continue
                    L.append(G)
                    out.append(G)
        levels[n] = out
        print("n=%d: %d connected C4-free subcubic graphs" % (n, len(out)), flush=True)
    return levels


def sat_verified():
    """graphs whose exact Phi is SAT-verified (UNSAT at Phi - 1): returns list of nx graphs + note"""
    ver = []
    for line in open(os.path.join(RES, "data/n6.txt")):
        i = line.find("[(")
        if i >= 0:
            E = ast.literal_eval(line[i:].strip())
            ver.append((nx.Graph(E), "n6.txt (run1.py, all C4-free graphs n<=6)"))
    for line in open(os.path.join(RES, "data/s7.txt")):
        i = line.find("[[")
        if i >= 0 and "unsat" in line:
            E = ast.literal_eval(line[i:].strip())
            ver.append((nx.Graph(E), "s7.txt (one.py, 7-vertex sweep)"))
    for E, ph in json.load(open(os.path.join(RES, "petersen19/proven.json"))):
        ver.append((nx.Graph([tuple(e) for e in E]), "petersen19/proven.json (enc5.py, Phi=%d)" % ph))
    return ver


def main():
    levels = gen()
    ver = sat_verified()
    s7all = []
    for line in open(os.path.join(RES, "data/g7s.txt")):
        if line.strip():
            s7all.append(nx.Graph(ast.literal_eval(line.strip())))
    rows = []
    for n in range(2, NMAX + 1):
        for G in levels[n]:
            E = [tuple(sorted(e)) for e in G.edges()]
            c = graph_class(n, E)
            t = tau(n, E)
            ph = phi(n, E)
            how = []
            for H, note in ver:
                if H.number_of_nodes() == n and H.number_of_edges() == len(E) and nx.is_isomorphic(G, H):
                    how.append(note)
                    break
            if c["maxdeg"] <= 2:
                status = "PROVED (Theorem F2, max degree <= 2)"
            elif c["pseudoforest"]:
                status = "PROVED (Theorem PF, LEAN)"
            elif how:
                status = "SAT (exact Phi): " + how[0]
            else:
                status = "OPEN"
                if n == 7 and any(H.number_of_edges() == len(E) and nx.is_isomorphic(G, H) for H in s7all):
                    status = "OPEN (7-vertex sweep: TIMEOUT 900 s)"
            rows.append({"n": n, "m": len(E), "tau": t, "phi": ph, "edges": E,
                         "hubs": c["n_hubs"], "girth": c["girth"], "pseudoforest": c["pseudoforest"],
                         "cyclomatic": len(E) - n + 1, "thmF_or": c["n_hubs"] <= 1, "cubic": c["mindeg"] == 3,
                         "status": status})
    json.dump(rows, open(os.path.join(HERE, "subcubic_graphs.json"), "w"), indent=0)
    from collections import Counter
    cnt = Counter((r["n"], r["status"].split(" (")[0].split(":")[0]) for r in rows)
    for k in sorted(cnt):
        print(k, cnt[k])
    print("smallest OPEN:")
    for r in sorted((r for r in rows if r["status"].startswith("OPEN")), key=lambda r: (r["n"], r["m"]))[:25]:
        print(r["n"], r["m"], "tau", r["tau"], "Phi", r["phi"], "girth", r["girth"], "hubs", r["hubs"],
              "beta", r["cyclomatic"], " ".join("%d%d" % e for e in r["edges"]), r["status"])


if __name__ == "__main__":
    main()
