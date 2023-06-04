from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators import *
from pysmt.shortcuts import Symbol, Or, ForAll, GE, LT, Real, Plus
from levels_new_form import one
from levels import check_depth

def nth_level_incremental_old_stack(n, formula, valids = set(), too_shallow_to_be_valid =set()):
  valids = set()
  too_shallow_to_be_valid = set()
  phi_n_minus_one_formula, phi_one_sfs, phi_p_D = one(formula)
  for i in range(2, n+1):
    assert (is_sat(phi_n_minus_one_formula))
    new_assertion = phi_n_minus_one_formula
    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'D':
        if sf.serialize() in valids:
          continue
        if sf.serialize() in too_shallow_to_be_valid:
          continue
        not_valid = And(phi_n_minus_one_formula, Not(sf))
        if not is_sat(not_valid):
          my_mate_id = sf.serialize()
          my_mate_id = my_mate_id.replace('D', 'C')
          my_mate_formula = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          new_assertion = And(new_assertion, my_mate_formula)
          valids.add(sf.serialize())
        else:
          if check_depth(sf.serialize()) < i:
            too_shallow_to_be_valid.add(sf.serialize())
            continue
    phi_n_minus_one_formula = new_assertion


  return phi_n_minus_one_formula, phi_one_sfs, phi_p_D



def nth_level_incremental(n, formula, valid_pairs = set(), implied_leaders_pairs = set(), all_leaders_are_true_formula=Bool(True)):
  valid_pairs = set()
  implied_leaders_pairs = set()
  all_leaders_are_true_formula = Bool(True)

  def is_k_element_in_tuples(my_set, element, k):
    for tup in my_set:
      if tup[k] == element:
        return True
    return False
  def nth_level_incremental_rec(n, formula, all_leaders_are_true_formula):
    # nonlocal valids, too_shallow_to_be_valid
    assert (n > 0)
    if n ==1:
      return one(formula)
    phi_n_minus_one_formula, phi_one_sfs, phi_p_D = nth_level_incremental_rec(n-1, formula, all_leaders_are_true_formula)
    assert(is_sat(phi_n_minus_one_formula))
    if n == 3:
      x = 1
    #todo: add only new valif pairs.
    new_assertion = phi_n_minus_one_formula
    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'D':
        if is_k_element_in_tuples(valid_pairs, sf, 1):
          continue
        not_valid = And(phi_n_minus_one_formula, Not(sf))
        phi_n_minus_one_formula_s = phi_n_minus_one_formula.serialize()
        if not is_sat(not_valid):
          my_mate_id = sf.serialize()
          my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          my_mate_id = my_mate_id.replace('D', 'C')
          my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          new_assertion = And(new_assertion, my_mate_formula)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          valid_pairs.add((my_mate_formula_C, my_mate_formula_D))

    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        if is_k_element_in_tuples(valid_pairs, sf, 0):
          continue
        not_leader = And(And(phi_n_minus_one_formula, Not(sf)), phi_p_D)
        if not is_sat(not_leader):  # has to be a leader in level 1
          my_mate_id = sf.serialize()
          my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          my_mate_id = my_mate_id.replace('C', 'D')
          my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          # new_assertion = And(new_assertion, my_mate_formula)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))

    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        my_mate_id = sf.serialize()
        my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        my_mate_id = my_mate_id.replace('C', 'D')
        my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        if not is_sat(And(phi_n_minus_one_formula, And(all_leaders_are_true_formula, Not(my_mate_formula_D)))):
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))
          # new_assertion = And(new_assertion, my_mate_formula_C)

        # new_assertion = And(new_assertion, Implies(Implies(all_leaders_are_true_formula, my_mate_formula_D), my_mate_formula_C))
    # for c, d in valid_pairs:
    #   new_assertion = And(new_assertion, c)
    return new_assertion, phi_one_sfs, phi_p_D
  new_assertion, phi_one_sfs, phi_p_D = nth_level_incremental_rec(n, formula, all_leaders_are_true_formula)
  if n == 1:
    return new_assertion, phi_one_sfs, phi_p_D
  x = 5
  leaders = valid_pairs.union(implied_leaders_pairs)
  for sf in phi_one_sfs:
    if sf.serialize().replace("'", "")[-1] == 'C':
      if not is_k_element_in_tuples(leaders, sf, 0):
        new_assertion = And(new_assertion, Not(sf))
  return new_assertion, phi_one_sfs, phi_p_D





def nth_level_incremental_new_stack(n, formula, valid_pairs = set(), implied_leaders_pairs = set(), all_leaders_are_true_formula=Bool(True)):
  valid_pairs = set()
  implied_leaders_pairs = set()
  all_leaders_are_true_formula = Bool(True)

  def is_k_element_in_tuples(my_set, element, k):
    for tup in my_set:
      if tup[k] == element:
        return True
    return False

  phi_n_minus_one_formula, phi_one_sfs, phi_p_D = one(formula)
  assert (is_sat(And(phi_p_D, phi_n_minus_one_formula)))
  for i in range(2, n+1):
    new_assertion = phi_n_minus_one_formula
    assert (is_sat(And(phi_p_D, phi_n_minus_one_formula)))
    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'D':
        if is_k_element_in_tuples(valid_pairs, sf, 1):
          continue
        not_valid = And(phi_n_minus_one_formula, Not(sf))
        phi_n_minus_one_formula_s = phi_n_minus_one_formula.serialize()
        if not is_sat(not_valid):
          my_mate_id = sf.serialize()
          my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          my_mate_id = my_mate_id.replace('D', 'C')
          my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          # new_assertion = And(new_assertion, my_mate_formula)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          valid_pairs.add((my_mate_formula_C, my_mate_formula_D))

    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        if is_k_element_in_tuples(valid_pairs, sf, 0):
          continue
        not_leader = And(And(phi_n_minus_one_formula, Not(sf)), phi_p_D)
        if not is_sat(not_leader):  # has to be a leader in level 1
          my_mate_id = sf.serialize()
          my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          my_mate_id = my_mate_id.replace('C', 'D')
          my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          # new_assertion = And(new_assertion, my_mate_formula)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))

    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        my_mate_id = sf.serialize()
        my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        my_mate_id = my_mate_id.replace('C', 'D')
        my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        if not is_sat(And(phi_n_minus_one_formula, And(all_leaders_are_true_formula, Not(my_mate_formula_D)))):
          # new_assertion = And(new_assertion, my_mate_formula_C)
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))
    for c, d in valid_pairs:
      new_assertion = And(new_assertion, c)
    phi_n_minus_one_formula = new_assertion


        # new_assertion = And(new_assertion, Implies(Implies(all_leaders_are_true_formula, my_mate_formula_D), my_mate_formula_C))

  if n == 1:
    return phi_n_minus_one_formula, phi_one_sfs, phi_p_D
  x = 5
  leaders = valid_pairs.union(implied_leaders_pairs)
  for sf in phi_one_sfs:
    if sf.serialize().replace("'", "")[-1] == 'C':
      if not is_k_element_in_tuples(leaders, sf, 0):
        phi_n_minus_one_formula = And(phi_n_minus_one_formula, Not(sf))
  return phi_n_minus_one_formula, phi_one_sfs, phi_p_D

