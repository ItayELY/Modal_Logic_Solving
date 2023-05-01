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
    print_dict_as_table(translate_modal_valuation(a_sfs, s))
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
