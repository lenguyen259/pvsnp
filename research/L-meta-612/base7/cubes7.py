# cubes7.py NAME EDGES M [--to SEC] [--nodrat] [--only K1,K2,..]
# Cube-and-conquer for one size m: split on (output gate op) x (exact #AND = k), k = 0..m.
# The cubes cover every assignment (op(out) is & or |; #AND is some k in 0..m), so all cubes UNSAT
# => the size-m encoding is UNSAT. Same flags as run7.py (--factc --viol --lexbot --rest rest/rest_NAME.json;
# the restriction file must already exist from run7.py). Results appended to logs/NAME_cubes_M.jsonl.
import sys, json, os, subprocess, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
P19 = os.path.join(HERE, '..', 'petersen19')
KISSAT = os.path.join(P19, 'kissat'); DRATTRIM = os.path.join(P19, 'drat-trim')
SCR = '/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/base7'
ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('edges'); ap.add_argument('m', type=int)
ap.add_argument('--to', type=int, default=1800); ap.add_argument('--drat-to', type=int, default=5400)
ap.add_argument('--nodrat', action='store_true'); ap.add_argument('--only'); ap.add_argument('--splitops', help='comma list of gate wires whose op is split (&/|) inside every selected cube')
a = ap.parse_args(); nm = a.name; m = a.m
rf = os.path.join(HERE, 'rest', 'rest_%s.json' % nm); assert os.path.exists(rf)
out_f = os.path.join(HERE, 'logs', '%s_cubes_%d.jsonl' % (nm, m))
done = {}
if os.path.exists(out_f):
    for l in open(out_f):
        r = json.loads(l)
        if r['result'] == 'UNSAT' and (a.nodrat or r['drat'].startswith('VERIFIED')): done[r['cube']] = r
cubes = [(o, k) for k in range(m + 1) for o in '&|']
SPL = [int(x) for x in a.splitops.split(',')] if a.splitops else []
import itertools as _it
SUBS = [''.join(c) for c in _it.product('&|', repeat=len(SPL))] if SPL else ['']
if a.only: cubes = [c for c in cubes if '%s%d' % c in a.only.split(',')]
os.makedirs(SCR, exist_ok=True)
for (o, k), sub in [(c, sb) for c in cubes for sb in SUBS]:
    key = '%s%d%s' % (o, k, ('_' + sub.replace('&','a').replace('|','o')) if sub else '')
    if key in done: continue
    cnf = os.path.join(SCR, '%s_%d_%s.cnf' % (nm, m, key.replace('&', 'A').replace('|', 'O'))); prf = cnf[:-4] + '.drat'
    subprocess.run(['python3', os.path.join(HERE, 'enc5.py'), str(m), '--graph', a.edges, '--rest', rf, '--factc', '--lexbot',
                    '--viol', '--outop', o, '--nand', str(k), '--dimacs', cnf] + (['--cube', json.dumps([['o', w, 1 if c == '&' else 0] for w, c in zip(SPL, sub)])] if SPL else []), capture_output=True, cwd=HERE, check=True)
    t0 = time.time()
    kargs = [KISSAT, '-q', '--time=%d' % a.to] + ([cnf] if a.nodrat else ['--no-binary', cnf, prf])
    out = subprocess.run(kargs, capture_output=True, text=True).stdout; dt = time.time() - t0
    st = 'UNSAT' if 's UNSATISFIABLE' in out else ('SAT' if 's SATISFIABLE' in out else 'TIMEOUT')
    dr = '-'
    if st == 'UNSAT' and not a.nodrat:
        psz = os.path.getsize(prf); t1 = time.time()
        try:
            o2 = subprocess.run([DRATTRIM, cnf, prf, '-t', str(a.drat_to)], capture_output=True, text=True, timeout=a.drat_to + 60).stdout
            dr = 'VERIFIED' if '\ns VERIFIED' in '\n' + o2.replace('\r', '') else ('NOT VERIFIED' if 'NOT VERIFIED' in o2 else 'TIMEOUT/?')
        except subprocess.TimeoutExpired: dr = 'TIMEOUT'
        dr += ' (%.1fs, proof %.1f MB)' % (time.time() - t1, psz / 1e6)
    rec = {'cube': key, 'result': st, 'kissat_s': round(dt, 1), 'drat': dr, 'time': time.strftime('%H:%M:%S')}
    with open(out_f, 'a') as fh: fh.write(json.dumps(rec) + '\n')
    print(nm, m, rec, flush=True)
    for p in (cnf, prf):
        try: os.remove(p)
        except OSError: pass
    if st == 'SAT': print('SAT cube: stop'); break
