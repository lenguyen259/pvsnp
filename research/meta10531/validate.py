import sys,time
from enc import *
from localimp import star14
from pysat.solvers import Solver
G=canon(star14()); print(G, check(G)==[])
for mono in (False,True):
    S=Solver(name='cadical195'); e=Enc(14,mono=mono,add=S.add_clause)
    for t in range(512): e.addrow(t)
    t0=time.time(); r=S.solve(assumptions=e.assume(G)); print('mono',mono,'star14 admitted:',r,time.time()-t0)
