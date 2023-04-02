from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from pysmt.solvers.z3 import *

def translate_Not(not_p):
    if not_p.is_not():
        assert (not_p.is_not)
        # inner_expr = Symbol(not_p.arg(0))
        # assert(len(get_free_variables(not_p)) == 1)

        inner_expr = not_p.serialize()
        p_form = Not(not_p).serialize()
        phi_p_D = Symbol('phi{' + inner_expr + '}D')

        phi_p_C = Symbol('phi{' + inner_expr + '}C')

        phi_notp_D = Symbol('phi{' + p_form + '}D')

        phi_notp_C = Symbol('phi{' + p_form + '}C')

        translated = And(And(Implies(And(phi_p_D, phi_p_C), And(Not(phi_notp_D), phi_notp_C)),
                             Implies(And(phi_p_D, Not(phi_p_C)), And(Not(phi_notp_D), Not(phi_notp_C)))),
                         And(Implies(And(Not(phi_p_D), phi_p_C), And(phi_notp_D, phi_notp_C)),
                             Implies(And(Not(phi_p_D), Not(phi_p_C)), And(phi_notp_D, Not(phi_notp_C)))))

        return translated


def translate_and(and_pq):
    if and_pq.is_and():
        assert (and_pq.is_and)
        # inner_expr = Symbol(not_p.arg(0))
        # assert(len(get_free_variables(not_p)) == 1)

        and_expr = and_pq.serialize()
        p = and_pq.arg(0)
        q = and_pq.arg(1)

        phi_pandq_D = Symbol('phi{' + and_expr + '}D')
        phi_pandq_C = Symbol('phi{' + and_expr + '}C')

        phi_p_D = Symbol('phi{' + p.serialize() + '}D')
        phi_p_C = Symbol('phi{' + p.serialize() + '}C')

        phi_q_D = Symbol('phi{' + q.serialize() + '}D')
        phi_q_C = Symbol('phi{' + q.serialize() + '}C')

        translated = And(Implies(And(And(phi_p_D, phi_p_C),
                                     And(phi_q_D, phi_q_C)),
                                 And(phi_pandq_D, phi_pandq_C))  # T and T = T
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(phi_q_D, Not(phi_q_C))),
                                       And(phi_pandq_D, Not(phi_pandq_C))))  # T and t = t
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_pandq_D), phi_pandq_C)))  # T and F = F
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       And(Not(phi_pandq_D), Not(phi_pandq_C))))  # T and f = f

                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(phi_q_D, phi_q_C)),
                                       And(phi_pandq_D, Not(phi_pandq_C))))  # t and T = t
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(phi_q_D, Not(phi_q_C))),
                                       And(phi_pandq_D, Not(phi_pandq_C))))  # t and t = t
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_pandq_D), phi_pandq_C)))  # t and F = F
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_D), phi_pandq_C),
                                          And(Not(phi_pandq_D), Not(phi_pandq_C)))))  # t and f = F or f

                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(phi_q_D, phi_q_C)),
                                       And(Not(phi_pandq_D), Not(phi_pandq_C))))  # F and T = F
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(phi_q_D, Not(phi_q_C))),
                                       And(Not(phi_pandq_D), Not(phi_pandq_C))))  # F and t = f
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_pandq_D), phi_pandq_C)))  # F and F = F
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       And(Not(phi_pandq_D), Not(phi_pandq_C))))  # F and f = F

                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(phi_q_D, phi_q_C)),
                                       And(Not(phi_pandq_D), Not(phi_pandq_C))))  # f and T = f
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(phi_q_D, Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_D), phi_pandq_C),
                                          And(Not(phi_pandq_D), Not(phi_pandq_C)))))  # f and t = F or f
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_pandq_D), phi_pandq_C)))  # f and F = F
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_D), (phi_pandq_C)),
                                          And(Not(phi_pandq_D), Not(phi_pandq_C)))))  # f and f = F or f

                         )

        return translated

def translate_box(box_p):
    # inner_expr = Symbol(not_p.arg(0))
    # assert(len(get_free_variables(not_p)) == 1)

    inner_expr = box_p.serialize()
    p_form = box_p.arg(0).serialize()
    phi_p_D = Symbol('phi{' + p_form + '}D')

    phi_p_C = Symbol('phi{' + p_form + '}C')

    phi_boxp_D = Symbol('phi{' + inner_expr + '}D')

    phi_boxp_C = Symbol('phi{' + inner_expr + '}C')

    translated = And(
                    Implies(And(phi_p_D, phi_p_C),
                            Or(And(phi_boxp_D, phi_boxp_C), And(phi_boxp_D, Not(phi_boxp_C)))), #T -> T or t

                And( Implies(And(phi_p_D, Not(phi_p_C)),
                            Or(And(Not(phi_boxp_D), Not(phi_boxp_C)), And(Not(phi_boxp_D), phi_boxp_C)))), # t -> F or f

                And(Implies(And(Not(phi_p_D), Not(phi_p_C)),
                            Or(And(Not(phi_boxp_D), Not(phi_boxp_C)), And(Not(phi_boxp_D), phi_boxp_C)))),# f -> F or f

                And(Implies(And(Not(phi_p_D), phi_p_C),
                            Or(And(Not(phi_boxp_D), Not(phi_boxp_C)), And(Not(phi_boxp_D), phi_boxp_C))))# F -> F or f
                )

    return translated

def translate_or(or_pq):
    if or_pq.is_or():
        assert (or_pq.is_or)

        and_expr = or_pq.serialize()
        p = or_pq.arg(0)
        q = or_pq.arg(1)

        phi_porq_D = Symbol('phi{' + and_expr + '}D')
        phi_porq_C = Symbol('phi{' + and_expr + '}C')

        phi_p_D = Symbol('phi{' + p.serialize() + '}D')
        phi_p_C = Symbol('phi{' + p.serialize() + '}C')

        phi_q_D = Symbol('phi{' + q.serialize() + '}D')
        phi_q_C = Symbol('phi{' + q.serialize() + '}C')

        translated = And(Implies(And(And(phi_p_D, phi_p_C),
                                     And(phi_q_D, phi_q_C)),
                                 And(phi_porq_D, phi_porq_C))  # T or T = T
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(phi_q_D, Not(phi_q_C))),
                                       And(phi_porq_D, phi_porq_C)))  # T or t = T
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(phi_porq_D, phi_porq_C)))  # T or F = T
                         , And(Implies(And(And(phi_p_D, phi_p_C),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       And(phi_porq_D, Not(phi_porq_C))))  # T or f = T

                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(phi_q_D, phi_q_C)),
                                       And(phi_porq_D, phi_porq_C)))  # t or T = T
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(phi_q_D, Not(phi_q_C))),
                                       Or(And(phi_porq_D, phi_porq_C),
                                       And(phi_porq_D, Not(phi_porq_C)))))  # t or t = T or t
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(phi_porq_D, Not(phi_porq_C))))  # t or F = t
                         , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       Or(And(phi_porq_D, phi_porq_C),
                                          And(phi_porq_D, Not(phi_porq_C)))))  # t or f = T or t

                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(phi_q_D, phi_q_C)),
                                       And(phi_porq_D, phi_porq_C)))  # F or T = T
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(phi_q_D, Not(phi_q_C))),
                                       And(phi_porq_D, Not(phi_porq_C))))  # F or t = t
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_porq_D), phi_porq_C)))  # F or F = F
                         , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                       And(Not(phi_porq_D), Not(phi_porq_C))))  # F or f = f

                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(phi_q_D, phi_q_C)),
                                       And(phi_porq_D, phi_porq_C)))  # f or T = T
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(phi_q_D, Not(phi_q_C))),
                                       Or(And(phi_porq_D, phi_porq_C),
                                          And(phi_porq_D, Not(phi_porq_C)))))  # f or t = T or t
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(Not(phi_q_D), phi_q_C)),
                                       And(Not(phi_porq_D), Not(phi_porq_C))))  # f or F = f
                         , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                           And(Not(phi_q_D), Not(phi_q_C))),
                                          And(Not(phi_porq_D), Not(phi_porq_C))))  # f or f = f

                         )

        return translated
