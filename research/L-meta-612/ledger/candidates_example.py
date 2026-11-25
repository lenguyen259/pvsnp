"""Example candidate file for the conjecture-evolution loop (playbooks/conjecture-evolution.md).

Run:  research/tools/cpuslot.sh nice -n 19 python3 -I falsify.py --candidates candidates_example.py [--core-only]
Output: candidates_example_result.json (survivors ranked by tightness, dead ones with smallest counterexamples).

Each candidate maps to (fn, one-line statement). fn(x) returns None (out of scope), a bool, or a margin
(>= 0 holds, < 0 violated). The context x offers (all on R = red(C), the functionally reduced circuit):
  x.G: n, E, A (adjacency sets), deg, V (non-isolated), tau, phi, N(v) (closed nbhd),
       need_A(v), need_N(v), need_B(v), need_OR(X), need_AND(X), phi_minus(X), has_edge_minus(X)
  x.R (Circ: n, gates, out, size, n_and(), n_or(), tts(fix), readers(), live()), x.C (as stored)
  x.size(), x.n_and(), x.n_or(); x.tot(X), x.sav(X), x.sa(X) (eliminations under x_X := 0);
  x.elim1(v) (x_v := 1); x.ch(v); x.opt_A(v), x.opt_N(v), x.opt_B(v) (elim - need, None if not allowed);
  x.minimal_and_support(); x.violations() -> (j1, j2, j3) STAR-ALL violation counts.
  lib612 helpers: red, ruleR_size, LD, LR, sing, minimal_ands, is_clean, graph_class, girth, tau, phi, ...
"""
from lib612 import *


def best(vals):
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def t2_c3(x):
    if not x.G.E or is_star(x.G.E) or max(x.G.deg) > 3:
        return None
    return best([x.opt_A(v) for v in x.G.V] + [x.opt_N(v) for v in x.G.V])


def t2_hub_only(x):
    # stronger: the good option sits at a vertex of maximum degree
    if not x.G.E or is_star(x.G.E) or max(x.G.deg) > 3:
        return None
    d = max(x.G.deg)
    H = [v for v in x.G.V if x.G.deg[v] == d]
    return best([x.opt_A(v) for v in H] + [x.opt_N(v) for v in H])


def and_plus_or_trade(x):
    # #AND - tau >= (|E| - 1) - #OR, i.e. the main claim written as a trade (same as MAIN)
    if not x.G.E:
        return None
    return (x.n_and() - x.G.tau) - ((len(x.G.E) - 1) - x.n_or())


def n_option_somewhere(x):
    # some N(v) option alone is good (G - N[v] with an edge)
    if not x.G.E or is_star(x.G.E):
        return None
    return best([x.opt_N(v) for v in x.G.V])


CLAIMS = {
    "t2_c3": (t2_c3, "Lemma T2 on max degree <= 3 (A or N option at some vertex)"),
    "t2_hub_only": (t2_hub_only, "T2 with the good vertex of maximum degree"),
    "trade": (and_plus_or_trade, "#AND - tau >= |E| - 1 - #OR (= MAIN)"),
    "N_only": (n_option_somewhere, "some N(v) option is good"),
}
