from pysmt.solvers import z3
from pysmt.walkers import IdentityDagWalker
import pysmt.operators as op
from translators_k import *
from pysmt.shortcuts import Symbol, Or, ForAll, GE, LT, Real, Plus

Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)

def check_depth(expr):
  stack = []
  max_depth = 0
  for char in expr:
    if char == '(':
      stack.append(char)
      max_depth = max(max_depth, len(stack))
    elif char == ')':
      if not stack:
        raise ValueError('Invalid expression: too many closing parentheses')
      stack.pop()
  if stack:
    raise ValueError('Invalid expression: too many opening parentheses')
  return max_depth

def one(formula, symbol="phi"):
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
    # inner_expr = not_p.serialize()
    # p_form = Not(not_p).serialize()

    inner_expr =  Not(not_p).serialize()
    p_form = not_p.serialize()

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

    add_to_set([phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C])

    translated = translate_or(phi_porq_D, phi_porq_C, phi_p_D, phi_p_C, phi_q_D, phi_q_C)
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
  #constrainset.add(phi_p_T)

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
  # constraints = ([c.serialize() for c in constrainset])
  # for c in constraints:
  #   print(c)
  for exp in constrainset:
    final_formula = And(final_formula, exp)
  return final_formula, sub_formulae_set, phi_p_T





def two(formula, symbol1="phi", symbol2="2psi"):
  sub_formulae_set = set()
  phi_one_formula, phi_one_sfs, phi_form_D = one(formula, symbol1)
  psi_one_formula, psi_one_sfs, _ = one(formula, symbol2)
  final_two_formula = phi_one_formula
  list_of_phi_psi = []
  list_phi_c_phi_d = []
  capitals = []
  for element in psi_one_sfs:
    s = element.serialize().replace("'","")[-1]
    if element.serialize().replace("'","")[-1] == 'D':
      my_mate_id = element.serialize()
      my_mate_id = my_mate_id.replace('D', 'C')
      my_mate_id = my_mate_id.replace(symbol2, symbol1)
      my_mate = [el for el in phi_one_sfs if el.serialize() == my_mate_id][0]
      list_of_phi_psi.append((element, my_mate))
    else:
      capitals.append(element)
  phi_capital_is_psi_designated = Bool(True)
  for sfs_psi_D, sfs_phi_C  in list_of_phi_psi:
    phi_capital_is_psi_designated = And(
      phi_capital_is_psi_designated,
      Implies(sfs_phi_C, sfs_psi_D)
    )
  phi_capital_is_psi_designated_ser = phi_capital_is_psi_designated.serialize()
  for sfs_psi_D, sfs_phi_C  in list_of_phi_psi:
    sfs_phi_D_id = element.serialize()
    sfs_phi_D_id = my_mate_id.replace('C', 'D')
    sfs_phi_D = [el for el in phi_one_sfs if el.serialize() == my_mate_id][0]
    for_all_sf = Implies(ForAll(psi_one_sfs, Implies(And(psi_one_formula, phi_capital_is_psi_designated), sfs_psi_D)), sfs_phi_C)
    sub_formulae_set.add(for_all_sf)
    final_two_formula = And(final_two_formula, for_all_sf)

    #Implies(ForAll(psi_one_sfs, Implies(psi_one_formula, sfs_psi_D)), sfs_phi_C)
  final_two_formula_s = final_two_formula.serialize()
  return final_two_formula, phi_one_sfs, phi_form_D



def nth_level(n, formula, symbol1="phi", PRINT_FINAL_FORMULA = False):
  assert(n>0)
  if n ==1:
    a = one(formula, symbol1)
    return a
  symbol1 = "phi"
  symbol2 = str(n)+"psi"

  if n ==1:
    return one(formula, symbol1)

  sub_formulae_set = set()
  phi_n_minus_one_formula, phi_n_minus_one_sfs, phi_form_D = nth_level(n-1,formula)
  psi_n_minus_one_formula, psi_n_minus_one_sfs, _ = nth_level(n-1, formula, symbol1=str(n)+"psi")
  final_n_formula = phi_n_minus_one_formula
  list_of_phi_psi = []
  for element in  psi_n_minus_one_sfs:
    s = element.serialize().replace("'","")[-1]
    if element.serialize().replace("'","")[-1] == 'D':
      my_mate_id = element.serialize()
      my_mate_id = my_mate_id.replace('D', 'C')
      my_mate_id = my_mate_id.replace(symbol2, symbol1)
      my_mate = [el for el in phi_n_minus_one_sfs if el.serialize() == my_mate_id][0]
      list_of_phi_psi.append((element, my_mate))

  phi_capital_is_psi_designated = Bool(True)
  for sfs_psi_D, sfs_phi_C in list_of_phi_psi:
    phi_capital_is_psi_designated = And(
      phi_capital_is_psi_designated,
      Implies(sfs_phi_C, sfs_psi_D)
    )
  for sf_psi_D, sf_phi_C  in list_of_phi_psi:
    for_all_sf = Implies(ForAll(psi_n_minus_one_sfs, Implies(And(psi_n_minus_one_formula
                                                                 , phi_capital_is_psi_designated), sf_psi_D)), sf_phi_C)
    sub_formulae_set.add(for_all_sf)
    final_n_formula = And(final_n_formula, for_all_sf)



  return final_n_formula, phi_n_minus_one_sfs, phi_form_D

def two_incremental(formula):
  phi_one_formula, phi_one_sfs, phi_p_D = one(formula)
  assert(is_sat(phi_one_formula))
  valid_pairs = set()
  implied_leaders_pairs = set()
  all_leaders_are_true_formula = Bool(True)

  # possible_assignment = get_model(phi_one_formula)
  new_assertion = phi_one_formula
  for sf in phi_one_sfs:
    if sf.serialize().replace("'", "")[-1] == 'D':
      not_valid = And(phi_one_formula, Not(sf))
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
      not_leader = And(And(phi_one_formula, Not(sf)),phi_p_D)
      if not is_sat(not_leader): #has to be a leader in level 1
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
      if not is_sat(And(phi_one_formula, And(all_leaders_are_true_formula, Not(my_mate_formula_D)))):
        new_assertion = And(new_assertion, my_mate_formula_C)

      # new_assertion = And(new_assertion, Implies(Implies(all_leaders_are_true_formula, my_mate_formula_D), my_mate_formula_C))
  return new_assertion, phi_one_sfs, phi_p_D

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

    new_assertion = phi_n_minus_one_formula
    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'D':
        if is_k_element_in_tuples(valid_pairs, sf, 1):
          continue
        not_valid = And(phi_n_minus_one_formula, Not(sf))
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
          new_assertion = And(new_assertion, my_mate_formula_C)

        # new_assertion = And(new_assertion, Implies(Implies(all_leaders_are_true_formula, my_mate_formula_D), my_mate_formula_C))
    return new_assertion, phi_one_sfs, phi_p_D

  return nth_level_incremental_rec(n, formula, all_leaders_are_true_formula)




def nth_level_incremental_new_stack(n, formula, valid_pairs = set(), implied_leaders_pairs = set(), all_leaders_are_true_formula=Bool(True), PRINT_FINAL_FORMULA = False):
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
  new_assertion = phi_n_minus_one_formula
  for i in range(2, n+1):
    print("now checking level " + str(i))
    try:
      assert (is_sat(And(phi_p_D, phi_n_minus_one_formula)))
    except:
      if PRINT_FINAL_FORMULA:
        print(And(phi_p_D, phi_n_minus_one_formula).serialize())
      assert (False)
      return phi_n_minus_one_formula, phi_one_sfs, phi_p_D
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
          new_assertion = And(new_assertion, my_mate_formula_C)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          valid_pairs.add((my_mate_formula_C, my_mate_formula_D))
    current_smalls = Bool(True)
    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        if is_k_element_in_tuples(valid_pairs, sf, 0):
          continue
        not_leader = And(And(new_assertion, Not(sf)), phi_p_D, current_smalls)
        if not is_sat(not_leader):  # has to be a leader in level 1
          my_mate_id = sf.serialize()
          my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          my_mate_id = my_mate_id.replace('C', 'D')
          my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
          new_assertion = And(new_assertion, sf)
          all_leaders_are_true_formula = And(all_leaders_are_true_formula, my_mate_formula_D)
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))
        else:
          current_smalls = And(current_smalls, Not(sf))

    for sf in phi_one_sfs:
      if sf.serialize().replace("'", "")[-1] == 'C':
        my_mate_id = sf.serialize()
        my_mate_formula_C = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        my_mate_id = my_mate_id.replace('C', 'D')
        my_mate_formula_D = [f for f in phi_one_sfs if f.serialize() == my_mate_id][0]
        if not is_sat(And(phi_n_minus_one_formula, And(all_leaders_are_true_formula, Not(my_mate_formula_D)))):
          new_assertion = And(new_assertion, my_mate_formula_C)
          implied_leaders_pairs.add((my_mate_formula_C, my_mate_formula_D))
    for c, d in valid_pairs:
      phi_n_minus_one_formula = And(phi_n_minus_one_formula, c)
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
      # else:
      #   phi_n_minus_one_formula = And(phi_n_minus_one_formula, sf)
      #   # pass
  return phi_n_minus_one_formula, phi_one_sfs, phi_p_D

