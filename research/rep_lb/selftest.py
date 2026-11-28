#!/usr/bin/env python3
"""Python-only checks of the generator (no Lean): data reproduction and the three validation instances."""
import re, subprocess, sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model import Inst, Search, represents, mono2
import gen

def run(n, m, mask, K, upper=False):
    inst = Inst(n, m, mask)
    S = Search(inst)
    c = gen.find_circuit(inst, K, S)
    return c, inst

# (1) lower bound holds: no circuit of size 7 for 3x5 mask 3242, one of size 8
assert run(3, 5, 3242, 7)[0] is None
g, o = run(3, 5, 3242, 8)[0]
assert mono2(g) and represents(3, 5, 3242, g, o) and len(g) == 8
# (3) 3x5 mask 7549: none of size 8, one of size 9
assert run(3, 5, 7549, 8)[0] is None
g, o = run(3, 5, 7549, 9)[0]
assert represents(3, 5, 7549, g, o) and len(g) == 9
# the 5x5 accepted instance L_meta_20635 (data rows identical to the accepted file when run against it)
assert run(5, 5, 32441376, 7)[0] is None and run(5, 5, 32441376, 8)[0] is not None
print('selftest OK')
