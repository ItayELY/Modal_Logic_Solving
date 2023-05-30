from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
from levels import *
import levels_new_form as lnf
import time
from translate_modal_valuation import *
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)





DEMO_SMTLIB=\
"""
(set-logic ALL)
(declare-fun Box (Bool) Bool)

(declare-const x Bool)

(assert (not (Box(Box (=> x x)))))
(check-sat)
"""
# form = smtlib_to_formula(DEMO_SMTLIB)
# print(form.serialize())
# solve_and_print_valuations(form, 2)
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
#Box
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


# # formula1 = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(p))))))))))))))))))))
# # formula2 = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Implies(p,p)))))))))))))))))))))
# # # formula = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(formula))))))))))))))))))))
# # # formula = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(formula))))))))))))))))))))
# # # formula = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(formula))))))))))))))))))))
formula = Not(Box(Box(Implies(p, p))))
# #
# #
# # #Not(Box(Implies(p, p)))#Not(Box(Implies(p, p)))
# solve_and_print_valuations(formula, 2)
# # # solve_and_print_valuations(formula, 2)
# # # solve_and_print_valuations(formula, 3)
# # # solve_and_print_valuations(formula, 4)
# # # solve_and_print_valuations(formula, 5)
# # # solve_and_print_valuations(formula, 6)
# # # solve_and_print_valuations(formula, 7)
# # # solve_and_print_valuations(formula, 8)
# # # solve_and_print_valuations(formula, 9)
# # solve_and_print_valuations(formula, 200)
#
#
# formula1 = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(p))))))))))))))))))))
# formula2 = Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Box(Implies(p,p)))))))))))))))))))))
# formula = Or(Not(formula1), Not(formula2))
# solve_and_print_valuations(formula, 200)

f = Not(Box(Box(Box(Implies(p, p)))))# = (Box(Box(Implies(p, p))))

 # solve_and_print_valuations_nf(f, 3)
# test()
print("*************************************")
print("oracle old:")
start_time1 = time.perf_counter()
test("oracle_old")
end_time1 = time.perf_counter()
print("*************************************")
print("oracle old lazy:")
start_time2 = time.perf_counter()
test("oracle_old_lazy")
end_time2 = time.perf_counter()
print("*************************************")
print('time of one: {}, time of two: {}'.format(end_time1 - start_time1, end_time2 - start_time2))
