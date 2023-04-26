from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
from levels import *
from translate_modal_valuation import *
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)





DEMO_SMTLIB=\
"""
(set-logic ALL)
(declare-fun Box (Bool) Bool)

(declare-const x Bool)

(assert (not x))
(check-sat)
"""

# parser = SmtLibParser()
# script = parser.get_script(StringIO(DEMO_SMTLIB))
# f = script.get_last_formula()
# test(And(f))
# box_f = And(Box(And(Not(y), x)), And(Not(y), x), Box(Box(And(Not(y), x))))
# print(box_f.get_free_variables())
# print("hello")
# test(box_f)

p = Symbol('p')
q = Symbol('q')
# test(And(p,Not(q)))
Box
# a, b = one(And(Implies(x, Not(x)), Not(Implies(x, Not(x)))), 'Passover')
# print(a.serialize())
# print(b)
#a, b = two(Box(Implies(Box(Implies(p,p)),Box(Implies(p,p)))))

# s = Solver()
# formula = Not((Box(Box(Implies(p, p)))))#Not(Box(Implies(p, p))) #And(Not(Box(Implies(p, p))) ,Box(Implies(p, p)))
# a, a_sfs = one(formula, "Mazza")
# b, b_sfs = two(formula)
# c, c_sfs = three(formula)
# print("\n\n\n")
# s.push()
# s.add_assertion(a)
# s.solve()
# print(translate_modal_valuation(a_sfs, s))
# s.pop()
# print("\n\n\n")
# s.push()
# s.add_assertion(b)
# s.solve()
# print(translate_modal_valuation(b_sfs, s))
# s.pop()
#
# print("\n\n\n")
# s.push()
# s.add_assertion(c)
# s.solve()
# print(translate_modal_valuation(c_sfs, s))
# s.pop()
A = Symbol('A')
B = Symbol('B')
C = Symbol('C')

formula = Not(Box(Box(Implies(And(Implies(A,B),Implies(B,C)), Implies(A, C)))))#Not(Box(Implies(p, p)))#Not(Box(Implies(p, p)))
sovle_and_print_valuations(formula, 1)
sovle_and_print_valuations(formula, 2)
sovle_and_print_valuations(formula, 3)


# test(And(Implies(x,Not(x)), Not(Implies(x,Not(x)))))

