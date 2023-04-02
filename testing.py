from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators import *


Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)
def test(formula):
  constrainset = set()
  constrainset.clear()
  def walk_and(formula, args, **kwargs):
    translated = translate_and(formula)
    constrainset.add(translated)
    return formula

  def walk_not(formula, args, **kwargs):
    translated = translate_Not(formula)
    constrainset.add(translated)
    return formula

  def walk_box(formula, args, **kwargs):
    return formula

  def walk_or(formula, args, **kwargs):
    translated = translate_or(formula)
    constrainset.add(translated)
    return formula

  walker = IdentityDagWalker()
  walker.set_function(walk_and, op.AND)
  # walker
  walker.set_function(walk_not, op.NOT)
  walker.set_function(walk_or, op.OR)
  inner_expr = formula.serialize()
  phi_p_T = Symbol('phi{'+inner_expr+'}T')
  phi_p_C = Symbol('phi{'+inner_expr+'}C')
  constrainset.add(phi_p_T)
  #print([c.serialize() for c in constrainset])
  def check_box(formula, args, **kwargs):
    args = formula.args()
    translated = translate_box(formula)
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



