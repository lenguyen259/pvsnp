# run7.py NAME EDGES [--to SEC] [--drat-to SEC] [--nodrat] [--smin M] [--smax M]
# Bottom-up base case: prove size(f_G) >= Phi(G) by showing the enc5 encoding (with --factc --viol --lexbot
# and restriction constraints from PROVED bounds of proper induced subgraphs) is UNSAT for every size
# m = 1..Phi-1. Each m: enc5 -> DIMACS -> kissat (DRAT proof) -> drat-trim. Non-vacuity first: the
# lexbot-canonical U (star-cover) circuit must be accepted at s = Phi (all flags except --viol).
# Results: logs/NAME.log (one line per step) and ../ledger/proven_subcubic.json (on full success).
import sys, json, os, subprocess, time, argparse
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
P19 = os.path.join(HERE, '..', 'petersen19')
KISSAT = os.path.join(P19, 'kissat'); DRATTRIM = os.path.join(P19, 'drat-trim')
LEDGER = os.path.join(HERE, '..', 'ledger', 'proven_subcubic.json')
SCR = '/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/base7'
sys.path.insert(0, HERE)
from grest import tau, is_pf
from grest2 import family2
from mku import ucirc
from plib import lexbot_form
from networkx.algorithms.isomorphism import GraphMatcher

def proven_table():
    """[(nx.Graph, L)] from petersen19/proven.json (H7, H8a, H8b) and our ledger (status PROVED only)."""
    out = [(nx.Graph([tuple(e) for e in Es]), L) for Es, L in json.load(open(os.path.join(P19, 'proven.json')))]
    if os.path.exists(LEDGER):
        for r in json.load(open(LEDGER)):
            if r.get('status') == 'UNSAT-all-m':
                out.append((nx.Graph([tuple(e) for e in r['edges']]), r['L']))
    return out

def missing_subgraphs(E, proven):
    """proper induced non-pseudoforest subgraphs with an edge that have no proven bound (reported only)."""
    import itertools
    n = max(max(e) for e in E) + 1; miss = []
    for k in range(1, n):
        for S in itertools.combinations(range(n), k):
            V = set(range(n)) - set(S)
            H = [(a, b) for a, b in E if a in V and b in V]
            if not H or is_pf(H): continue
            GH = nx.Graph(H)
            if not any(PG.number_of_edges() == GH.number_of_edges() and nx.is_isomorphic(PG, GH) for PG, _ in proven):
                if not any(nx.is_isomorphic(nx.Graph(M), GH) for M in miss): miss.append(H)
    return miss

def log(nm, msg):
    line = time.strftime('%H:%M:%S ') + msg
    print(line, flush=True)
    with open(os.path.join(HERE, 'logs', nm + '.log'), 'a') as fh: fh.write(line + '\n')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('edges')
    ap.add_argument('--to', type=int, default=1800); ap.add_argument('--drat-to', type=int, default=3600)
    ap.add_argument('--nodrat', action='store_true'); ap.add_argument('--smin', type=int, default=1)
    ap.add_argument('--smax', type=int); ap.add_argument('--minL', type=int, default=1)
    ap.add_argument('--novalid', action='store_true')
    a = ap.parse_args(); nm = a.name
    E = [tuple(e) for e in json.loads(a.edges)]; n = max(max(e) for e in E) + 1
    t = tau(E); phi = len(E) + t - 1
    os.makedirs(SCR, exist_ok=True)
    proven = proven_table()
    miss = missing_subgraphs(E, proven)
    fam = family2(E, proven, a.minL)
    rf = os.path.join(HERE, 'rest', 'rest_%s.json' % nm); os.makedirs(os.path.dirname(rf), exist_ok=True)
    json.dump(fam, open(rf, 'w'))
    log(nm, 'graph %s n=%d |E|=%d tau=%d Phi=%d; restrictions %d (max tL %d); missing proper subgraph bounds: %s'
        % (json.dumps(E), n, len(E), t, phi, len(fam), max(x[4] for x in fam), json.dumps(miss)))
    flags = ['--graph', json.dumps(E), '--rest', rf, '--factc', '--lexbot']
    # non-vacuity
    if not a.novalid:
        G = nx.Graph(E); G.add_nodes_from(range(n))
        Au = [[m[i] for i in range(n)] for m in GraphMatcher(G, G).isomorphisms_iter()]
        c = lexbot_form(ucirc(E), Au, n); assert len(c) == phi
        t0 = time.time()
        r = subprocess.run(['python3', os.path.join(HERE, 'enc5.py'), str(phi)] + flags + ['--fixc', json.dumps(c), '--solve'],
                           capture_output=True, text=True, cwd=HERE).stdout
        res = [l for l in r.splitlines() if l.startswith('RESULT') or l.startswith('VERIF')]
        log(nm, 'VALIDATION U circuit at s=Phi=%d (rest+factc+lexbot, fixc): %s' % (phi, ' | '.join(res)))
        if not any('RESULT SAT' in l for l in res) or not any(l.startswith('VERIFIED') for l in res):
            log(nm, 'VALIDATION FAILED: stop'); sys.exit(2)
    results = {}
    smax = a.smax or phi - 1
    tot = 0.0; alldrat = True
    for m in range(a.smin, smax + 1):
        cnf = os.path.join(SCR, '%s_%d.cnf' % (nm, m)); prf = cnf[:-4] + '.drat'
        subprocess.run(['python3', os.path.join(HERE, 'enc5.py'), str(m)] + flags + ['--viol', '--dimacs', cnf],
                       capture_output=True, cwd=HERE, check=True)
        hdr = open(cnf).readline().split()
        t0 = time.time()
        kargs = [KISSAT, '-q', '--time=%d' % a.to]
        if a.nodrat: kargs += [cnf]
        else: kargs += ['--no-binary', cnf, prf]
        out = subprocess.run(kargs, capture_output=True, text=True).stdout
        dt = time.time() - t0; tot += dt
        st = 'UNSAT' if 's UNSATISFIABLE' in out else ('SAT' if 's SATISFIABLE' in out else 'TIMEOUT')
        dr = '-'
        if st == 'UNSAT' and not a.nodrat:
            psz = os.path.getsize(prf)
            t1 = time.time()
            try:
                o = subprocess.run([DRATTRIM, cnf, prf, '-t', str(a.drat_to)], capture_output=True, text=True,
                                   timeout=a.drat_to + 60).stdout
                dr = 'VERIFIED' if '\ns VERIFIED' in '\n' + o.replace('\r', '') else ('NOT VERIFIED' if 'NOT VERIFIED' in o else 'TIMEOUT/?')
                if not dr.startswith('VERIFIED'):
                    with open(os.path.join(HERE, 'logs', '%s_%d_drattrim.txt' % (nm, m)), 'w') as fh: fh.write(o[-5000:])
            except subprocess.TimeoutExpired: dr = 'TIMEOUT'
            dr += ' (%.1fs, proof %.1f MB)' % (time.time() - t1, psz / 1e6)
        if not dr.startswith('VERIFIED'): alldrat = False
        results[m] = {'result': st, 'kissat_s': round(dt, 1), 'drat': dr, 'vars': int(hdr[2]), 'clauses': int(hdr[3])}
        log(nm, 's=%d vars=%s clauses=%s kissat: %s %.1fs ; drat-trim: %s' % (m, hdr[2], hdr[3], st, dt, dr))
        for p in (cnf, prf):
            try: os.remove(p)
            except OSError: pass
        if st != 'UNSAT':
            if st == 'SAT': log(nm, 'SAT at s=%d < Phi: inspect (counterexample candidate!)' % m)
            break
    ok = all(results.get(m, {}).get('result') == 'UNSAT' for m in range(1, phi))
    if ok and a.smin == 1:
        rec = {'name': nm, 'edges': [list(e) for e in E], 'n': n, 'm': len(E), 'tau': t, 'phi': phi, 'L': phi,
               'status': 'UNSAT-all-m', 'label': 'DRAT' if alldrat else 'UNSAT',
               'method': 'base7/run7.py: enc5.py sizes 1..Phi-1 each UNSAT (kissat 4.0.4); restrictions from proven bounds of proper induced subgraphs',
               'flags': '--factc --viol --lexbot --rest rest/rest_%s.json (grest2.family2, minL=%d; %d restrictions)' % (nm, a.minL, len(fam)),
               'subgraph_bounds_missing': miss,
               'validation': 'U circuit accepted at s=Phi (fixc, rest+factc+lexbot)' if not a.novalid else 'skipped',
               'kissat_total_s': round(tot, 1), 'drat': 'yes' if alldrat else 'no', 'per_size': results,
               'date': time.strftime('%Y-%m-%d')}
        L = json.load(open(LEDGER)) if os.path.exists(LEDGER) else []
        L = [r for r in L if r['name'] != nm] + [rec]
        json.dump(L, open(LEDGER, 'w'), indent=1)
        log(nm, 'PROVED size >= Phi = %d (label %s, kissat total %.1fs); recorded in ledger/proven_subcubic.json' % (phi, rec['label'], tot))
    else:
        log(nm, 'NOT CLOSED (results %s)' % json.dumps({k: v['result'] for k, v in results.items()}))

if __name__ == '__main__': main()
