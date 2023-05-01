from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from pysmt.solvers.z3 import *

def translate_Not(phi_p_D, phi_p_C, phi_notp_D, phi_notp_C):
    translated = And(And(Implies(And(phi_p_D, phi_p_C), And(Not(phi_notp_D), phi_notp_C)),
                         Implies(And(phi_p_D, Not(phi_p_C)), And(Not(phi_notp_D), Not(phi_notp_C)))),
                     And(Implies(And(Not(phi_p_D), phi_p_C), And(phi_notp_D, phi_notp_C)),
                         Implies(And(Not(phi_p_D), Not(phi_p_C)), And(phi_notp_D, Not(phi_notp_C)))))

    return translated


def translate_and(phi_pandq_D, phi_pandq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C):
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
                                   And(Not(phi_pandq_D), phi_pandq_C)))  # F and T = F
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

def translate_box(phi_p_D, phi_p_C, phi_boxp_D, phi_boxp_C):

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

def translate_or(phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C):

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

def translate_implies(phi_pimpliesq_D, phi_pimpliesq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C):

    translated = And(Implies(And(And(phi_p_D, phi_p_C),
                                 And(phi_q_D, phi_q_C)),
                             And(phi_pimpliesq_D, phi_pimpliesq_C))  # T implies T = T
                     , And(Implies(And(And(phi_p_D, phi_p_C),
                                       And(phi_q_D, Not(phi_q_C))),
                                   And(phi_pimpliesq_D, Not(phi_pimpliesq_C))))  # T implies t = t
                     , And(Implies(And(And(phi_p_D, phi_p_C),
                                       And(Not(phi_q_D), phi_q_C)),
                                   And(Not(phi_pimpliesq_D), phi_pimpliesq_C)))  # T implies F = F
                     , And(Implies(And(And(phi_p_D, phi_p_C),
                                       And(Not(phi_q_D), Not(phi_q_C))),
                                   And(Not(phi_pimpliesq_D), Not(phi_pimpliesq_C))))  # T implies f = f

                     , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                       And(phi_q_D, phi_q_C)),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # t implies T = T
                     , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                       And(phi_q_D, Not(phi_q_C))),
                                   Or(And(phi_pimpliesq_D, phi_pimpliesq_C),
                                   And(phi_pimpliesq_D, Not(phi_pimpliesq_C)))))  # t implies t = T or t
                     , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                       And(Not(phi_q_D), phi_q_C)),
                                   And(Not(phi_pimpliesq_D), Not(phi_pimpliesq_C))))  # t implies F = f
                     , And(Implies(And(And(phi_p_D, Not(phi_p_C)),
                                       And(Not(phi_q_D), Not(phi_q_C))),
                                      And(Not(phi_pimpliesq_D), Not(phi_pimpliesq_C))))  # t implies f = f

                     , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                       And(phi_q_D, phi_q_C)),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # F implies T = T
                     , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                       And(phi_q_D, Not(phi_q_C))),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # F implies t = T
                     , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                       And(Not(phi_q_D), phi_q_C)),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # F implies F = T
                     , And(Implies(And(And(Not(phi_p_D), phi_p_C),
                                       And(Not(phi_q_D), Not(phi_q_C))),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # F implies f = T

                     , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                       And(phi_q_D, phi_q_C)),
                                   And(phi_pimpliesq_D, phi_pimpliesq_C)))  # f implies T = T
                     , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                       And(phi_q_D, Not(phi_q_C))),
                                   Or(And(phi_pimpliesq_D, phi_pimpliesq_C),
                                      And(phi_pimpliesq_D, Not(phi_pimpliesq_C)))))  # f implies t = T or t
                     , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                       And(Not(phi_q_D), phi_q_C)),
                                   And(phi_pimpliesq_D, Not(phi_pimpliesq_C))))  # f implies F = t
                     , And(Implies(And(And(Not(phi_p_D), Not(phi_p_C)),
                                       And(Not(phi_q_D), Not(phi_q_C))),
                                   Or(And(phi_pimpliesq_D, phi_pimpliesq_C,
                                      And(phi_pimpliesq_D, Not(phi_pimpliesq_C))))))  # f implies f = T or t

                     )

    return translated
