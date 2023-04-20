from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators import *
from pysmt.shortcuts import Symbol, Or, ForAll, GE, LT, Real, Plus

Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)


def one(formula, symbol):
  sub_formulae_set = set()

  def add_to_set(lst):
    for item in lst:
      sub_formulae_set.add(item)

  constrainset = set()
  constrainset.clear()
  def walk_and(formula, args, **kwargs):
    and_pq = formula
    assert (and_pq.is_and)
    and_expr = and_pq.serialize()
    p = and_pq.arg(0)
    q = and_pq.arg(1)

    phi_pandq_D = Symbol(symbol+'{' + and_expr + '}D')
    phi_pandq_C = Symbol(symbol+'{' + and_expr + '}C')

    phi_p_D = Symbol(symbol+'{' + p.serialize() + '}D')
    phi_p_C = Symbol(symbol+'{' + p.serialize() + '}C')

    phi_q_D = Symbol(symbol+'{' + q.serialize() + '}D')
    phi_q_C = Symbol(symbol+'{' + q.serialize() + '}C')

    add_to_set([phi_pandq_D, phi_pandq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C])

    translated = translate_and(phi_pandq_D, phi_pandq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
    constrainset.add(translated)
    return formula

  def walk_not(formula, args, **kwargs):
    not_p = formula
    assert(not_p.is_not)
    inner_expr = not_p.serialize()
    p_form = Not(not_p).serialize()
    phi_p_D = Symbol(symbol+'{' + inner_expr + '}D')
    phi_p_C = Symbol(symbol+'{' + inner_expr + '}C')
    phi_notp_D = Symbol(symbol+'{' + p_form + '}D')
    phi_notp_C = Symbol(symbol+'{' + p_form + '}C')


    add_to_set([phi_p_D, phi_p_C, phi_notp_D, phi_notp_C])

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

    phi_porq_D = Symbol(symbol+'{' + or_expr + '}D')
    phi_porq_C = Symbol(symbol+'{' + or_expr + '}C')

    phi_p_D = Symbol(symbol+'{' + p.serialize() + '}D')
    phi_p_C = Symbol(symbol+'{' + p.serialize() + '}C')

    phi_q_D = Symbol(symbol+'{' + q.serialize() + '}D')
    phi_q_C = Symbol(symbol+'{' + q.serialize() + '}C')

    add_to_set(phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)

    translated = translate_and(phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
    constrainset.add(translated)
    return formula

  def walk_implies(formula, args, **kwargs):
    p_implies_q = formula
    assert (p_implies_q.is_implies)

    implies_expr = p_implies_q.serialize()
    p = p_implies_q.arg(0)
    q = p_implies_q.arg(1)

    phi_pimpliesq_D = Symbol(symbol+'{' + implies_expr + '}D')
    phi_pimpliesq_C = Symbol(symbol+'{' + implies_expr + '}C')

    phi_p_D = Symbol(symbol+'{' + p.serialize() + '}D')
    phi_p_C = Symbol(symbol+'{' + p.serialize() + '}C')

    phi_q_D = Symbol(symbol+'{' + q.serialize() + '}D')
    phi_q_C = Symbol(symbol+'{' + q.serialize() + '}C')

    add_to_set([phi_pimpliesq_D, phi_pimpliesq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C])

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
  phi_p_T = Symbol(symbol+'{'+inner_expr+'}D')
  phi_p_C = Symbol(symbol+'{'+inner_expr+'}C')
  constrainset.add(phi_p_T)
  #print([c.serialize() for c in constrainset])
  def check_box(formula, args, **kwargs):
    args = formula.args()
    inner_expr = formula.serialize()
    p_form = formula.arg(0).serialize()
    phi_p_D = Symbol(symbol+'{' + p_form + '}D')

    phi_p_C = Symbol(symbol+'{' + p_form + '}C')

    phi_boxp_D = Symbol(symbol+'{' + inner_expr + '}D')

    phi_boxp_C = Symbol(symbol+'{' + inner_expr + '}C')

    add_to_set([phi_p_D, phi_p_C, phi_boxp_D, phi_boxp_C])

    translated = translate_box(phi_p_D, phi_p_C, phi_boxp_D, phi_boxp_C)
    constrainset.add(translated)
    return formula

  walker.set_function(check_box, 8)
  walker.walk(formula)
  final_formula = And(Bool(True), Bool(True))
  for exp in constrainset:
    final_formula = And(final_formula, exp)
  return final_formula, sub_formulae_set

def two(formula, symbol1="phi", symbol2="2psi"):
  sub_formulae_set = set()
  phi_one_formula, phi_one_sfs = one(formula, symbol1)
  psi_one_formula, psi_one_sfs = one(formula, symbol2)
  final_two_formula = phi_one_formula
  list_of_phi_psi = []
  for element in psi_one_sfs:
    s = element.serialize().replace("'","")[-1]
    if element.serialize().replace("'","")[-1] == 'D':
      my_mate_id = element.serialize()
      my_mate_id = my_mate_id.replace('D', 'C')
      my_mate_id = my_mate_id.replace(symbol2, symbol1)
      my_mate = [el for el in phi_one_sfs if el.serialize() == my_mate_id][0]
      list_of_phi_psi.append((element, my_mate))


  for sfs_psi_D, sfs_phi_C  in list_of_phi_psi:
    for_all_sf = ForAll(psi_one_sfs, Implies(Implies(psi_one_formula, sfs_psi_D),sfs_phi_C))
    sub_formulae_set.add(for_all_sf)
    final_two_formula = And(final_two_formula, for_all_sf)

  return final_two_formula, sub_formulae_set

def three(formula, symbol1="phi", symbol2="3psi"):
  sub_formulae_set = set()
  phi_two_formula, phi_two_sfs = two(formula)
  _, phi_one_sfs = one(formula, symbol1)
  psi_two_formula, psi_two_sfs = two(formula, symbol1="3phi")
  psi_one_formula, psi_one_sfs = one(formula, symbol2)
  final_three_formula = phi_two_formula
  list_of_phi_psi = []
  for element in psi_one_sfs:
    s = element.serialize().replace("'","")[-1]
    if element.serialize().replace("'","")[-1] == 'D':
      my_mate_id = element.serialize()
      my_mate_id = my_mate_id.replace('D', 'C')
      my_mate_id = my_mate_id.replace(symbol2, symbol1)
      my_mate = [el for el in phi_one_sfs if el.serialize() == my_mate_id][0]
      list_of_phi_psi.append((element, my_mate))


  for sfs_psi_D, sfs_phi_C  in list_of_phi_psi:
    for_all_sf = ForAll(psi_one_sfs, Implies(Implies(psi_two_formula, sfs_psi_D),sfs_phi_C))
    sub_formulae_set.add(for_all_sf)
    final_three_formula = And(final_three_formula, for_all_sf)

  return final_three_formula, sub_formulae_set

