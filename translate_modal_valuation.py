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
from collections import OrderedDict



Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)
def smtlib_to_formula(smtlib_string):
    parser = SmtLibParser()
    script = parser.get_script(StringIO(smtlib_string))
    return script.get_last_formula()
def order_dict_by_key_length(d):
    ordered_dict = OrderedDict(sorted(d.items(), key=lambda x: len(x[0])))
    return ordered_dict
def print_dict_as_table(data):
    # Set the maximum width of each table column
    max_key_width = 20
    max_value_width = 20

    # Print the table header
    print("+{}+{}+".format("-" * (max_key_width + 2), "-" * (max_value_width + 2)))
    print("| {:<{}} | {:<{}} |".format("Sub-Formula", max_key_width, "Assignment", max_value_width))
    print("+{}+{}+".format("=" * (max_key_width + 2), "=" * (max_value_width + 2)))

    # Print each key-value pair as a row in the table
    for key, value in data.items():
        # Split the key into multiple lines if it is too long
        lines = [str(key)[i:i+max_key_width] for i in range(0, len(str(key)), max_key_width)]
        lines = [line.ljust(max_key_width) for line in lines]

        # Print the first line of the key with the value
        print("| {} | {:<{}} |".format(lines[0], str(value)[:max_value_width], max_value_width))

        # Print any additional lines of the key with no value
        for line in lines[1:]:
            print("| {} | {:<{}} |".format(line, "", max_value_width))

        # Print a vertical line between each row
        print("|{}|{}|".format("-" * (max_key_width + 2), "-" * (max_value_width + 2)))

    # Print the table footer
    print("+{}+{}+".format("-" * (max_key_width + 2), "-" * (max_value_width + 2)))




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
        a, a_sfs, phi_formula_D = nth_level(1,formula)
    elif level == 2:
        a, a_sfs, phi_formula_D= two_incremental_lazy(formula)
    elif level == 3:
        a, a_sfs, phi_formula_D = nth_level_incremental_lazy(3, formula)
    else:
        a, a_sfs, phi_formula_D = nth_level_incremental_lazy(level, formula)
    print("\n\n\n")
    s.push()
    s.add_assertion(a)
    s.add_assertion(phi_formula_D)
    s.solve()
    print(f"level {level} valuation")
    print_dict_as_table(order_dict_by_key_length(translate_modal_valuation(a_sfs, s)))
    s.pop()
    print("\n\n\n")

def solve_and_print_valuations_nf(formula, level):
    s = Solver()
    phi_formula_D = None
    if level == 1:
        a, a_sfs, phi_formula_D = lnf.one(formula)
    elif level == 2:
        a, a_sfs, phi_formula_D = lnf.two_incremental(formula)
    elif level == 3:
        a, a_sfs, phi_formula_D = lnf.nth_level_incremental(3, formula)
    else:
        a, a_sfs, phi_formula_D = lnf.nth_level_incremental(level, formula)
    print("\n\n\n")
    s.push()
    s.add_assertion(a)
    s.add_assertion(phi_formula_D)
    s.solve()
    print(f"level {level} valuation")
    print_dict_as_table(order_dict_by_key_length(translate_modal_valuation(a_sfs, s)))
    s.pop()
    print("\n\n\n")


def is_modal_sat(formula, level, reduction):
    try:
        a, a_sfs, phi_p_D = reduction(level, formula)
        return (is_sat(And(a, phi_p_D)))
    except:
        return False

def is_modal_sat_new_form(formula, level, reduction):
    try:
        a, a_sfs, phi_p_D = reduction(level, formula)
        return (is_sat(And(a,phi_p_D)))
    except:
        return False
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
