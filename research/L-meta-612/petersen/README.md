# Counterexample search on Petersen and case-(a) graphs

All circuits below compute f_G exactly (checked on all 2^n inputs by two independent checkers).

## (OR) split is false
- Smallest: n=8, E=[01,23,04,24,15,25,06,36,17,37] (C4-free, min degree 2), tau=4.
  Size 14, #OR=8 < |E|-1=9, #AND=6:
  `8=0|2 9=1|2 10=0|3 11=1|3 12=4&8 13=5&9 14=6&10 15=8&9 16=10&15 17=7|16 18=11&17 19=12|13 20=19|14 21=20|18`
  Gate 16 accepts the edges 01, 23 and the junk pair 02, which (x1|x3) removes.
- Petersen (edges 01,12,23,34,40,05,16,27,38,49,57,79,96,68,85) at size Phi=20 with #OR=13, #AND=7:
  `10=0|9 11=5|9 12=0|6 13=5|6 14=3|10 15=4&14 16=2|11 17=7&16 18=2|12 19=1&18 20=10&11 21=12&20 22=8|21 23=13&22 24=2|8 25=3&24 26=15|17 27=26|19 28=27|23 29=28|25`
- In every variant found, each OR saved costs one extra AND, so the total never drops below Phi.

## Lemma D is false
Construction: J = x_a x_b | x_c x_d for two disjoint hub edges, z_v = x_v | J, then any circuit on the z's.
Petersen example of size 24 with ch = [2,1,2,1,2,2,2,2,2,1] against degree 3 (`model.py`, `runmodel2.py`).
Survey over 107 graphs with 2 or 3 hubs: counterexamples in most classes; none found for two non-adjacent hubs or three hubs forming a triangle.

## Not found
No (AND) counterexample and no circuit below |E| + tau - 1. Petersen's exact monotone size is not determined
(<= 20; size-19 SAT timed out after 45 min).
