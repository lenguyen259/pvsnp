# Lemma D, case (a): the proposed target is false; what is proved

Labels: PROVED (proof here, or explicit circuit checked by `star.py`/`cex2.py`/`thmN*.py` with Boolean
semantics via tr.breduce), DATA (SAT / enumeration only). Notation as in lemma-d/lemD.md.
Case (a): G C4-free, delta = 2, |H| >= 2. Target T(a): "some v in V2 has ch(v) >= 2".

## 1. T(a) is FALSE (PROVED, explicit circuits)

**Construction S (stars).** If every v in V2 has N(v) ⊆ H, put s_v = x_v & (x_u | x_w), cover G[H] by any
star circuit, OR everything. The inner OR charges only u,w in H; s_v is charged once (where it enters the
outer OR tree). So every V2 vertex is single-charged.
* Smallest: n=7, E=[01,04,05,12,14,26,35,36,56], H={0,1,5,6}, V2={2,3,4} independent.
  `7=6|1 8=2&7 9=5|6 10=3&9 11=0|1 12=4&11 13=1|5 14=0&13 15=5&6 16=8|10 17=16|12 18=17|14 19=18|15`
  size 13 = Phi+1, #OR = 8 = |E|-1 (OR-optimal). ch = {0:2,1:3,2:1,3:1,4:1,5:3,6:3}: good = {1,5,6}, all hubs.
* Subdivided K4 (n=10): ch = 3 = deg on the 4 hubs, 1 on all 6 subdivision vertices.

**Theorem N (PROVED).** If G[H] has an edge ab, then for every case-(a) G there is a reduced circuit in which
every V2 vertex is single-charged: z_v = x_v | x_a x_b (v in V2), then any circuit for f_G with x_v replaced
by z_v. Correct because x_a x_b <= f. No node of the second part is <= x_v: at the point "all vertices but v"
every z is 1, so any non-zero node is 1. So the only v-charged gate is z_v.
* Smallest counter-instance: two triangles + bridge [01,02,03,12,34,35,45] (n=6, the smallest case-(a) graph):
  `6=0&3 7=1|6 8=2|6 9=4|6 10=5|6 11=7&8 12=7|8 13=0&12 14=11|13 15=9&10 16=9|10 17=3&16 18=15|17 19=14|18`
  size 14 = Phi+4, ch = {0:5,1:1,2:1,3:5,4:1,5:1}. Also triangle+C5 (size 14 = Phi+5) and all 5 hub-edge
  graphs with n=7 (`thmN.py`).

**Construction N2 (PROVED by check).** H independent, but two V2 vertices p,q with N(p),N(q) ⊆ H:
B = s_p | s_q (one gate, labels p,q), z_v = x_v | B for the other v, z_p = z_q = B. Checked on a 10-vertex graph
with V2-edges and H independent ([03,13,14,24,05,25,06,67,17,28,89,09]): all V2 have ch 1; only hub 1 is good.

Consequences:
* "Some min-degree vertex is good" (DATA-unrefuted in lemD §4) is FALSE. Smallest: the n=7 circuit above.
* In case (a), Lemma D must sometimes be paid by a hub, even when G[V2] has edges.

## 2. Structure when every V2 vertex is single-charged (PROVED)

Assume every v in V2 is single-charged with gate g_v. Let P = {g_v}.

**Lemma A.** If no OR gate in cone(q) is charged by u, then q is u-free or q <= x_u. (Induction: an AND of a
dominated node is dominated. An OR with no dominated input has two u-free inputs.)

**Lemma C (factorisation).** Cut every g in P, replacing it by a fresh variable z_g. Then every node is, for each
v in V2, x_v-free or <= x_v. So f(x) = F(x_H, z(x)) with F monotone, and every non-P OR gate reads only
functions of (x_H, z). For g in P, with W = {u in V2 : g_u not strictly below g}, the inputs are
x_{D} ∧ h(x_H, z_below), with D ⊆ W and h free of x_W.

**P1.** g_v is not <= x_v. (Otherwise follow consumers to a second v-charged OR.) Every label of g is in
exactly one input, and that input's D is {label}. So g = x_v h1 | x_w h2 (labels v,w), or x_v h1 | h2.

**P2.** Adjacent V2 vertices have different gates. (h1, h2 are free of x_u,x_v. BN(v) at {u} gives h1(∅) = 1,
and BN(u) at {v} gives h1(∅) = 0.)

**P3.** If uv ∈ E(G[V2]) and g_u is not strictly below g_v, then g_v = x_v | b (type X). This sharpens L6/L7.

**P4.** A type-X gate x_v | b has exactly one label. (A second label w gives either an independent {v,t} with
t ∈ N(w) and g = 1, or N(w) ⊆ N(v), which is a C4.)

**Theorem A1.** Suppose H is independent and every V2 vertex is single-charged. Then the topologically first
gate of P is one of:
* (F1) x_v | h2(x_H) with N(v) ⊆ V2;
* (F2) x_v h1(x_H) | x_w h2(x_H) with N(v), N(w) ⊆ H.

*Proof.* One label with a hub neighbour t: BN gives h2(J+t) = 0 for every J ⊆ H, so b ≡ 0, which is not
allowed. Two labels: P4 plus BN at {u} for a V2-neighbour u. ∎

**Corollary A2.** Lemma D holds, via a V2 vertex, whenever H is independent, no V2 vertex has N(v) ⊆ V2, and at
most one V2 vertex has N(v) ⊆ H. Examples: θ(2,2,1) = [01,05,06,12,23,34,36,45], and two triangles joined by
a path of length 2 = [01,04,14,23,25,35,36,46], both with n=7.

## 3. Exact remaining gap for case (a)

All-V2-single-charged circuits exist when G[H] has an edge (Theorem N), or when two V2 vertices have N ⊆ H
(S/N2). In those graphs the good vertex must be a hub.

Open:
* (i) H independent, at most one v with N(v) ⊆ H, and some thread of length >= 3 (F1 possible). Is T(a) true
  there? Not decided. The smallest such graph has n=8: hubs 0 and 3 with threads of lengths 3, 2 and 1.
* (ii) In general: if every V2 vertex is single-charged, is some hub h good (ch(h) >= deg h)? This holds in
  every construction above. It is a degree->=3 statement of case-(b) type.

## 4. SAT / data (dsat2.py = dsat.py with only V2 constrained to ch <= 1, H free; timeout 2400 s)

See slog.txt and elog.txt.

| graph | Phi+X | "all V2 single-charged" circuit? | time |
|---|---|---|---|
| triangle+C5 [02,05,12,13,23,34,45] | X=0 | UNSAT | 156 s |
| triangle+C5 | X=1 | UNSAT | 329 s |
| two triangles + bridge [01,02,03,12,34,35,45] | X=0 | UNSAT | 448 s |
| two triangles + bridge | X=1 | not finished (stopped after ~20 min to free the solver) | - |
| both | X=4/5 | SAT by Theorem N (explicit circuits, §1) | - |

So in both n=6 graphs the minimum size of an all-V2-single-charged circuit lies in Phi+2..Phi+4 (resp. Phi+2..Phi+5): small-size
data can never see this phenomenon. Enumeration of more case-(a) circuits (edrive.sh) did not finish within its time budget;
the 29 triangle+C5 circuits at Phi (tdat.py): Lemma D 29/29, T(a) 29/29, all-V2-single 0, hub good 0.

Files: graphs.py (case-(a) graphs n<=7), star.py (construction S + checker), cex2.py, thmN.py, thmN2.py, dsat2.py, slog.txt, tdat.py.
