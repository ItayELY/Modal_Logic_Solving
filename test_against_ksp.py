from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *

import experimetns
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
import levels as lev
import levels_new_form as lnf
import experimetns as ex
from translate_modal_valuation import *
from ksp_to_pysmt_parser import parse_expression
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)






ksp_formulas = '''(box (p and q) imp (box p and box q))
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

ksp_solutions = '''Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Unsatisfiable
Unsatisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Unsatisfiable
Unsatisfiable'''.split("\n")

ksp_solutions = '''Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Satisfiable
Unsatisfiable
Satisfiable
Unsatisfiable
Unsatisfiable
Unsatisfiable'''.split("\n")

parsed_ksp_formulas = []
for e in ksp_formulas:
    try:
        parsed_ksp_formulas.append(parse_expression(e))
    except:
        print(e)
        pass

test_num = 1
hits = []
for formula, solution in zip(parsed_ksp_formulas, ksp_solutions):

    satisfiability = ''
    if is_modal_sat_new_form(formula, 3, ex.nth_level_incremental_new_stack):
        satisfiability = "Satisfiable"
    else:
        satisfiability = "Unsatisfiable"
    print('\n\n')
    print("..........................................")
    print("test number " + str(test_num))
    if satisfiability == solution:
        hits.append(1)
        print("test passed!")
    else:
        print("test failed!")
        hits.append(0)
    print(formula.serialize())
    print("ksp claims this formula to be " + solution)
    print("we claim it to be " + satisfiability)
    print("..........................................")
    test_num += 1

print("succeeded in " + str(sum(hits)) + " tests")
print("out of " + str(len(hits)) + " tests")

# #
