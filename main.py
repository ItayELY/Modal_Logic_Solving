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
import experimetns as ex
from translate_modal_valuation import *
from ksp_to_pysmt_parser import parse_expression
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
# print("*************************************")
# print("oracle old:")
# test("oracle_old")
# print("*************************************")
# print("oracle new:")
# test("oracle_new")
# ~(box p & box q -> box (p & q))
# f = Not(Implies(And(Box(p), Box(q)), Box(And(p, q))))

# expression = "~((<>p & <>q) -> (<>(p & <>q) | <>(<>p & q) | <>(p & q)))"
expression = "~ (box (p and q) imp (box p and box q))"
formula = parse_expression(expression)
f_s = formula.serialize()
is_sat = "sat" if is_modal_sat_new_form(formula, 2, ex.nth_level_incremental_new_stack) else "unsat"
print(formula.serialize(), " is ", is_sat)
# solve_and_print_valuations_nf(formula, 2)
to_parse = '''(box (p and q) imp (box p and box q))
~ (box (p and q) imp (box p and box q))
(dia (p or q) imp (dia p or dia q))
~(dia (p or q) imp (dia p or dia q))
(box p imp ~dia~p)
~(box p imp ~dia~p)
(~dia~p imp box p)
~(~dia~p imp box p)
(box (p or ~p))
~(box (p or ~p))
(~dia~p imp box p)
~(~dia~p imp box p)
(box ((box dia (p & q)) & (p & box q)) -> box (box dia (p & q)))
~(box ((box dia (p & q)) & (p & box q)) -> box (box dia (p & q)))
(box p -> (dia (p & q) -> box p))
~(box p -> (dia (p & q) -> box p))
((box (p & q) -> (box q & box (~p | ~q))))
~(box ((p & q) -> p) -> (box (p & q) -> box q))
~([](p -> q) -> ([]p -> []q))
~([]p -> <>p)
~([]p -> p)
~([]p -> [][]p)
~(p -> []<>p)
~(<>p -> []<>p)
~(([]p & []q) -> [](p & q))
~([]([]p -> q) -> []p)
~([](<>p -> q) -> (p -> []q))
~(<>[](<>p -> []<>p))
~([](p -> [](q -> r)) -> <>(q ->([]p -> <> r)))
~([](p | <>q) -> ([]p | <>q))
~((<>p & <>q) -> (<>(p & <>q) & <>(<>p & q)))
~((<>p & <>q) -> (<>(p & <>q) | <>(<>p & q) | <>(p & q)))
~(<>p -> []p)
~([]<>p -> <>[]p)
~(<>[]p -> []<>p)
~([]([]p -> []q) | []([]q -> []p))
~([]([](p -> []p) -> p) -> p)
~([]([](p -> []p) -> p) -> (<>[]p -> p))
~((p & <>[]p) -> []p)
~(<>p -> <><>p)
~(([]p & ~[][]p) -> <>([][]p & ~[][][]p))
~([][]p <-> []p)
~(<>[]p <-> []p)
~([]<>[]<>p <-> []<>p)
~([][][]p <-> [][]p)
~([]<>[]p <-> [][]p)
~(<>[][]p <-> <>[]p)
~(<><>[]p <-> <>[]p)
~([][]p <-> <>[]p)
~ (box (p and q) imp (box p and box q))
(phi_1 | ~box 1 (a2 | a1)) & (phi_2 | ~box 1 (a1 | a2)) & phi_3
(~a1 | ~box a2) & (a1 | ~box false) & (~a1 | a3) & (~a1 | ~a3) & (a1 | box ~a4) & box a4
(~box ~a1 | ~box (~a2 & ~a3)) & box ~a1 & box ~a2 & box ~a3
(~box ~a1 | ~box (~a2 & ~a3)) & box ~a1 & box ~a2 & box~a3'''.split("\n")

to_parse = ["(box (p or ~p))"]

results = ''''''
print(len(to_parse))
parsed = []
for e in to_parse:
    try:
        parsed.append(parse_expression(e))
    except:
        print(e)
        pass
print(len(parsed))
for formu in parsed:
    print("Satisfiable") if is_modal_sat_new_form(formu, 1, ex.nth_level_incremental_new_stack) else print("Unsatisfiable")
# #
