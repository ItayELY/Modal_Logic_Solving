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
        Ψ_p_T = Symbol('phi{' + inner_expr + '}T')

        Ψ_p_C = Symbol('phi{' + inner_expr + '}C')

        Ψ_notp_T = Symbol('phi{' + p_form + '}T')

        Ψ_notp_C = Symbol('phi{' + p_form + '}C')

        translated = And(And(Implies(And(Ψ_p_T, Ψ_p_C), And(Not(Ψ_notp_T), Ψ_notp_C)),
                             Implies(And(Ψ_p_T, Not(Ψ_p_C)), And(Not(Ψ_notp_T), Not(Ψ_notp_C)))),
                         And(Implies(And(Not(Ψ_p_T), Ψ_p_C), And(Ψ_notp_T, Ψ_notp_C)),
                             Implies(And(Not(Ψ_p_T), Not(Ψ_p_C)), And(Ψ_notp_T, Not(Ψ_notp_C)))))

        # translated = And(And(Implies(And(Ψ_p_T, Ψ_p_C), And(Not(Ψ_p_T), Ψ_p_C)),
        #             Implies(And(Ψ_p_T, Not(Ψ_p_C)), And(Not(Ψ_p_T), Not(Ψ_p_C)))),
        #         And(Implies(And(Not(Ψ_p_T), Ψ_p_C), And(Ψ_p_T, Ψ_p_C)),
        #             Implies(And(Not(Ψ_p_T), Not(Ψ_p_C)), And(Ψ_p_T, Not(Ψ_p_C)))))
        return translated


def translate_and(and_pq):
    if and_pq.is_and():
        assert (and_pq.is_and)
        # inner_expr = Symbol(not_p.arg(0))
        # assert(len(get_free_variables(not_p)) == 1)

        and_expr = and_pq.serialize()
        p = and_pq.arg(0)
        q = and_pq.arg(1)

        phi_pandq_T = Symbol('phi{' + and_expr + '}T')
        phi_pandq_C = Symbol('phi{' + and_expr + '}C')

        phi_p_T = Symbol('phi{' + p.serialize() + '}T')
        phi_p_C = Symbol('phi{' + p.serialize() + '}C')

        phi_q_T = Symbol('phi{' + q.serialize() + '}T')
        phi_q_C = Symbol('phi{' + q.serialize() + '}C')

        translated = And(Implies(And(And(phi_p_T, phi_p_C),
                                     And(phi_q_T, phi_q_C)),
                                 And(phi_pandq_T, phi_pandq_C))  # T and T = T
                         , And(Implies(And(And(phi_p_T, phi_p_C),
                                           And(phi_q_T, Not(phi_q_C))),
                                       And(phi_pandq_T, Not(phi_pandq_C))))  # T and t = t
                         , And(Implies(And(And(phi_p_T, phi_p_C),
                                           And(Not(phi_q_T), phi_q_C)),
                                       And(Not(phi_pandq_T), phi_pandq_C)))  # T and F = F
                         , And(Implies(And(And(phi_p_T, phi_p_C),
                                           And(Not(phi_q_T), Not(phi_q_C))),
                                       And(Not(phi_pandq_T), Not(phi_pandq_C))))  # T and f = f

                         , And(Implies(And(And(phi_p_T, Not(phi_p_C)),
                                           And(phi_q_T, phi_q_C)),
                                       And(phi_pandq_T, Not(phi_pandq_C))))  # t and T = t
                         , And(Implies(And(And(phi_p_T, Not(phi_p_C)),
                                           And(phi_q_T, Not(phi_q_C))),
                                       And(phi_pandq_T, Not(phi_pandq_C))))  # t and t = t
                         , And(Implies(And(And(phi_p_T, Not(phi_p_C)),
                                           And(Not(phi_q_T), phi_q_C)),
                                       And(Not(phi_pandq_T), phi_pandq_C)))  # t and F = F
                         , And(Implies(And(And(phi_p_T, Not(phi_p_C)),
                                           And(Not(phi_q_T), Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_T), phi_pandq_C),
                                          And(Not(phi_pandq_T), Not(phi_pandq_C)))))  # t and f = F or f

                         , And(Implies(And(And(Not(phi_p_T), phi_p_C),
                                           And(phi_q_T, phi_q_C)),
                                       And(Not(phi_pandq_T), Not(phi_pandq_C))))  # F and T = F
                         , And(Implies(And(And(Not(phi_p_T), phi_p_C),
                                           And(phi_q_T, Not(phi_q_C))),
                                       And(Not(phi_pandq_T), Not(phi_pandq_C))))  # F and t = f
                         , And(Implies(And(And(Not(phi_p_T), phi_p_C),
                                           And(Not(phi_q_T), phi_q_C)),
                                       And(Not(phi_pandq_T), phi_pandq_C)))  # F and F = F
                         , And(Implies(And(And(Not(phi_p_T), phi_p_C),
                                           And(Not(phi_q_T), Not(phi_q_C))),
                                       And(Not(phi_pandq_T), Not(phi_pandq_C))))  # F and f = F

                         , And(Implies(And(And(Not(phi_p_T), Not(phi_p_C)),
                                           And(phi_q_T, phi_q_C)),
                                       And(Not(phi_pandq_T), Not(phi_pandq_C))))  # f and T = f
                         , And(Implies(And(And(Not(phi_p_T), Not(phi_p_C)),
                                           And(phi_q_T, Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_T), phi_pandq_C),
                                          And(Not(phi_pandq_T), Not(phi_pandq_C)))))  # f and t = F or f
                         , And(Implies(And(And(Not(phi_p_T), Not(phi_p_C)),
                                           And(Not(phi_q_T), phi_q_C)),
                                       And(Not(phi_pandq_T), phi_pandq_C)))  # f and F = F
                         , And(Implies(And(And(Not(phi_p_T), Not(phi_p_C)),
                                           And(Not(phi_q_T), Not(phi_q_C))),
                                       Or(And(Not(phi_pandq_T), (phi_pandq_C)),
                                          And(Not(phi_pandq_T), Not(phi_pandq_C)))))  # f and f = F or f

                         )

        # translated = And(And(Implies(And(Ψ_p_T, Ψ_p_C), And(Not(Ψ_p_T), Ψ_p_C)),
        #             Implies(And(Ψ_p_T, Not(Ψ_p_C)), And(Not(Ψ_p_T), Not(Ψ_p_C)))),
        #         And(Implies(And(Not(Ψ_p_T), Ψ_p_C), And(Ψ_p_T, Ψ_p_C)),
        #             Implies(And(Not(Ψ_p_T), Not(Ψ_p_C)), And(Ψ_p_T, Not(Ψ_p_C)))))
        return translated

def translate_box(box_p):
    # inner_expr = Symbol(not_p.arg(0))
    # assert(len(get_free_variables(not_p)) == 1)

    inner_expr = box_p.serialize()
    p_form = box_p.arg(0).serialize()
    phi_p_T = Symbol('phi{' + p_form + '}T')

    phi_p_C = Symbol('phi{' + p_form + '}C')

    phi_boxp_T = Symbol('phi{' + inner_expr + '}T')

    phi_boxp_C = Symbol('phi{' + inner_expr + '}C')

    translated = And(
                    Implies(And(phi_p_T, phi_p_C),
                            Or(And(phi_boxp_T, phi_boxp_C), And(phi_boxp_T, Not(phi_boxp_C)))), #T -> T or t

                And( Implies(And(phi_p_T, Not(phi_p_C)),
                            Or(And(Not(phi_boxp_T), Not(phi_boxp_C)), And(Not(phi_boxp_T), phi_boxp_C)))), # t -> F or f

                And(Implies(And(Not(phi_p_T), Not(phi_p_C)),
                            Or(And(Not(phi_boxp_T), Not(phi_boxp_C)), And(Not(phi_boxp_T), phi_boxp_C)))),# f -> F or f

                And(Implies(And(Not(phi_p_T), phi_p_C),
                            Or(And(Not(phi_boxp_T), Not(phi_boxp_C)), And(Not(phi_boxp_T), phi_boxp_C))))# F -> F or f
                )

    # translated = And(And(Implies(And(Ψ_p_T, Ψ_p_C), And(Not(Ψ_p_T), Ψ_p_C)),
    #             Implies(And(Ψ_p_T, Not(Ψ_p_C)), And(Not(Ψ_p_T), Not(Ψ_p_C)))),
    #         And(Implies(And(Not(Ψ_p_T), Ψ_p_C), And(Ψ_p_T, Ψ_p_C)),
    #             Implies(And(Not(Ψ_p_T), Not(Ψ_p_C)), And(Ψ_p_T, Not(Ψ_p_C)))))
    return translated
