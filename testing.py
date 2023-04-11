from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators import *


Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)


def test(formula):
  sub_formulae_set = set()
  constrainset = set()
  constrainset.clear()
  def walk_and(formula, args, **kwargs):
    and_pq = formula
    assert (and_pq.is_and)
    and_expr = and_pq.serialize()
    p = and_pq.arg(0)
    q = and_pq.arg(1)

    phi_pandq_D = Symbol('phi{' + and_expr + '}D')
    phi_pandq_C = Symbol('phi{' + and_expr + '}C')

    phi_p_D = Symbol('phi{' + p.serialize() + '}D')
    phi_p_C = Symbol('phi{' + p.serialize() + '}C')

    phi_q_D = Symbol('phi{' + q.serialize() + '}D')
    phi_q_C = Symbol('phi{' + q.serialize() + '}C')

    translated = translate_and(phi_pandq_D, phi_pandq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
    constrainset.add(translated)
    return formula

  def walk_not(formula, args, **kwargs):
    not_p = formula
    assert(not_p.is_not)
    inner_expr = not_p.serialize()
    p_form = Not(not_p).serialize()
    phi_p_D = Symbol('phi{' + inner_expr + '}D')
    phi_p_C = Symbol('phi{' + inner_expr + '}C')
    phi_notp_D = Symbol('phi{' + p_form + '}D')
    phi_notp_C = Symbol('phi{' + p_form + '}C')


    translated = translate_Not(phi_p_D, phi_p_C, phi_notp_D, phi_notp_C)
    constrainset.add(translated)
    return formula

  # def walk_box(formula, args, **kwargs):
  #   return formula

  def walk_or(formula, args, **kwargs):
    or_pq = formula
    assert (or_pq.is_or)

    or_expr = or_pq.serialize()
    p = or_pq.arg(0)
    q = or_pq.arg(1)

    phi_porq_D = Symbol('phi{' + or_expr + '}D')
    phi_porq_C = Symbol('phi{' + or_expr + '}C')

    phi_p_D = Symbol('phi{' + p.serialize() + '}D')
    phi_p_C = Symbol('phi{' + p.serialize() + '}C')

    phi_q_D = Symbol('phi{' + q.serialize() + '}D')
    phi_q_C = Symbol('phi{' + q.serialize() + '}C')

    translated = translate_and(phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
    constrainset.add(translated)
    return formula

  def walk_implies(formula, args, **kwargs):
    p_implies_q = formula
    assert (p_implies_q.is_implies)

    implies_expr = p_implies_q.serialize()
    p = p_implies_q.arg(0)
    q = p_implies_q.arg(1)

    phi_pimpliesq_D = Symbol('phi{' + implies_expr + '}D')
    phi_pimpliesq_C = Symbol('phi{' + implies_expr + '}C')

    phi_p_D = Symbol('phi{' + p.serialize() + '}D')
    phi_p_C = Symbol('phi{' + p.serialize() + '}C')

    phi_q_D = Symbol('phi{' + q.serialize() + '}D')
    phi_q_C = Symbol('phi{' + q.serialize() + '}C')

    translated = translate_implies(phi_pimpliesq_D, phi_pimpliesq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
    constrainset.add(translated)
    return formula

  walker = IdentityDagWalker()
  walker.set_function(walk_and, op.AND)
  # walker
  walker.set_function(walk_not, op.NOT)
  walker.set_function(walk_or, op.OR)
  walker.set_function(walk_implies, op.IMPLIES)
  inner_expr = formula.serialize()
  phi_p_T = Symbol('phi{'+inner_expr+'}D')
  phi_p_C = Symbol('phi{'+inner_expr+'}C')
  constrainset.add(phi_p_T)
  #print([c.serialize() for c in constrainset])
  def check_box(formula, args, **kwargs):
    args = formula.args()
    inner_expr = box_p.serialize()
    p_form = box_p.arg(0).serialize()
    phi_p_D = Symbol('phi{' + p_form + '}D')

    phi_p_C = Symbol('phi{' + p_form + '}C')

    phi_boxp_D = Symbol('phi{' + inner_expr + '}D')

    phi_boxp_C = Symbol('phi{' + inner_expr + '}C')

    translated = translate_box(phi_p_D, phi_p_C, phi_boxp_D, phi_boxp_C)
    constrainset.add(translated)
    return formula

  walker.set_function(check_box, 8)
  walker.walk(formula)
  final_formula = And(Bool(True), Bool(True))
  for exp in constrainset:
    final_formula = And(final_formula, exp)

  print(final_formula.serialize())
  print(is_sat(final_formula))
  m1 = get_model(final_formula)
  print(m1)