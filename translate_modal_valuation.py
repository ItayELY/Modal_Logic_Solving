from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
from levels import *
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)


def translate_modal_valuation(sfs, s):
    valuation = {}
    for sf in sfs:
        # s = sf.serialize().replace("'", "")[-1]
        if sf.serialize().replace("'", "")[-1] == 'D':
            my_mate_id = sf.serialize()
            my_mate_id = my_mate_id.replace('D', 'C')
            my_mate_formula = [f for f in sfs if f.serialize() == my_mate_id][0]
            sf_v = s.get_value(sf).serialize()
            if sf_v == 'True':
                if s.get_value(my_mate_formula).serialize() == 'True':
                    val = 'T'
                else:
                    val = 't'
            else:
                if s.get_value(my_mate_formula).serialize() == 'True':
                    val = 'F'
                else:
                    val = 'f'
            inner_formula = (sf.serialize().split('{')[1]).split('}')[0]
            valuation[inner_formula] = val
    return valuation

def solve_and_print_valuations(formula, level):
    s = Solver()
    if level == 1:
        a, a_sfs = nth_level(1,formula)
    elif level == 2:
        a, a_sfs = nth_level_incremental(2, formula)
    elif level == 3:
        a, a_sfs = nth_level_incremental(3, formula)
    else:
        a, a_sfs = nth_level_incremental(level, formula)
    print("\n\n\n")
    s.push()
    s.add_assertion(a)
    s.solve()
    print(f"level {level} valuation")
    print(translate_modal_valuation(a_sfs, s))
    s.pop()
    print("\n\n\n")

# s = Solver()
# p = Symbol('p')
# q = Symbol('q')
#
#
# formula1 = Not((Box(Box(Implies(p, p)))))
# formula2 = Box(Implies(p, p))
# a, sfs = one(formula2, "Mazza")
# model = get_model(a)
# s.add_assertion(a)
# s.solve()
#
# valuation = translate_modal_valuation(sfs, s)
# print(valuation)
