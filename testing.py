from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators import *
from levels import *
from translate_modal_valuation import *
import levels_new_form as lnf
import  experimetns as ex


Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)

p = Symbol('p')
q = Symbol('q')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
g = Symbol('g')


tests = [
  (Not(p), 1, True),

(Not(Box(Implies(p,p))), 1, True),
(Not(Box(Implies(p,p))), 2, False),
(Not(Box(Implies(p,p))), 3, False),

(Not(Box(Box(Implies(p,p)))), 1, True),
(Not(Box(Box(Implies(p,p)))), 2, True),
(Not(Box(Box(Implies(p,p)))), 3, False),

(Not(Box(Or(p,Not(p)))), 1, True),
(Not(Box(Or(p,Not(p)))), 2, False),
(Not(Box(Or(p,Not(p)))), 5, False),

(Not(And(Box(Implies(p,p)), q)), 1, True),
(Not(And(Box(Implies(p,p)), q)), 2, True),
(Not(And(Box(Implies(p,p)), q)), 3, True),

(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))), 1, True),
(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))), 2, True),
(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))), 3, True),

(Not(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), 1, False),
(Not(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), 2, False),

(Not(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))), 1, True),
(Not(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))), 2, False),

(Not(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))))), 1, True),
(Not(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))))), 2, True),
(Not(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))))), 3, False),

(Not(Box(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))))), 1, True),
(Not(Box(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))))), 2, True),
(Not(Box(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))))), 3, True),
#(Not(Box(Box(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d)))))))), 4, False),


(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p)), 1, True),
(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p)), 2, True),
(Not(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p))), 1, True),
(Not(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p))), 2, False),

(Not(Box(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p)))), 1, True),
(Not(Box(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p)))), 2, True),
(Not(Box(And(Box(Implies(And(Or(a,b), Or(c,d)), Or(Or(And(a,c), And(a,d)), Or(And(b,c), And(b,d))))), Implies(p, p)))), 3, False),

#(Not(p), 1, True),
#(Not(p), 1, True),
#(Not(p), 1, True)
]
tests2 = [

]
def test(solving_type = "karp_old"):
  solver_fun = None
  if solving_type == "karp_old":
    solver_fun = nth_level
  if solving_type == "oracle_old":
    solver_fun = ex.nth_level_incremental_old_stack
  if solving_type == "oracle_old_lazy":
    solver_fun = nth_level_incremental_lazy
  if solving_type == "oracle_new":
    solver_fun = ex.nth_level_incremental_new_stack
  for case in tests:
    sat = "unsat"
    if case[2] is True:
      sat = "sat"
    if is_modal_sat(case[0], case[1], solver_fun) is case[2]:
      print("test passed: for "+ case[0].serialize()+ " is indeed " + sat + " in level " + str(case[1]))
    else:
      print("test failed: for "+ case[0].serialize()+ " should be " + sat + " in level " + str(case[1]))
