from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *

import experimetns
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
import omori_skourt_solver as lev
import zohar_lahav_solver as lnf
import experimetns as ex
from translate_modal_valuation import *
from ksp_to_pysmt_parser import parse_expression
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)

import subprocess
import time
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
def execute_terminal_commands(commands):
    for command in commands:
        start_time = time.perf_counter()
        process = subprocess.Popen(['/home/yon/Downloads/ksp-0.1.5/ksp', '-f', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        output, error = process.communicate()
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        output = output.decode('utf-8').strip()

        print(f"Command: {' '.join(['./ksp', '-fsub', '-f', command])}")
        print(f"Output:\n{output}")
        print(f"Execution time: {execution_time:.2f} seconds")
        print("--------------------------------------")

# Example usage:
command_list = ["formula1", "formula2", "formula3"]
execute_terminal_commands(ksp_formulas)
