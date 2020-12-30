#!/usr/bin/python3

# ====================================================
# file name: resolve_satisfiability.py
#
# Script to resolve satisfiability of given formulas using Z3 SMT solver.
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

import os
import sys
import symboliclib
from z3 import *
from copy import deepcopy
from collections import deque


# Main script function
def main():
    fa_a_name = sys.argv[1]
    fa_b_name = sys.argv[2]
    fa_a_orig = symboliclib.parse(fa_a_name)
    fa_b_orig = symboliclib.parse(fa_b_name)

    q_a_states = deque()
    q_b_states = deque()

    # enqueue the initial states
    for initial_state in fa_a_orig.start:
        q_a_states.append(initial_state)
    for initial_state in fa_b_orig.start:
        q_b_states.append(initial_state)

    q_pair_states = deque()

    def make_pair_states(q_pair_states, q_a_states, q_b_states):
        for a_state in q_a_states:
            for b_state in q_b_states:
                q_pair_states.append([a_state, b_state])

        q_a_states.clear()
        q_b_states.clear()

    make_pair_states(q_pair_states, q_a_states, q_b_states)


    """
    # enqueue the rest of the states
    for state in fa_a_orig.states:
        if not state in fa_a_orig.start:
            fa_a_states.put(state)
    """

    fa_a = deepcopy(fa_a_orig)
    fa_b = deepcopy(fa_b_orig)

    fa_a.unify_transition_symbols()
    fa_b.unify_transition_symbols()

    curr_pair = q_pair_states.popleft()
    fa_a.start = {curr_pair[0]}
    fa_b.start = {curr_pair[1]}

    fa_a = fa_a.simple_reduce()
    fa_a = fa_a.determinize()

    fa_b = fa_b.simple_reduce()
    fa_b = fa_b.determinize()

    fa_a_formulas_dict = fa_a.count_formulas_for_lfa()
    #print(fa_a_formulas_dict)  # DEBUG
    fa_b_formulas_dict = fa_b.count_formulas_for_lfa()
    #print(fa_b_formulas_dict)  # DEBUG

    #fa_a_only_formulas = [[1, 0], [8, 0]]

    satisfiability = check_satisfiability(fa_a_formulas_dict, fa_b_formulas_dict)
    print(satisfiability)

    # ^ fast test whether the initial state is satisfiable.





def check_satisfiability(fa_a_formulas_dict, fa_b_formulas_dict):
    """
    Check satisfiability for formulas using SMT solver Z3.
    :param fa_a_formulas_dict: Dictionary with formulas for FA A.
    :param fa_b_formulas_dict: Dictionary with formulas for FA B.
    :return: True if satisfiable; False if not satisfiable.
    """

    def get_only_formulas(formulas_dict):
        only_formulas = []
        for accept_state in formulas_dict:
            try:
                only_formulas.append([formulas_dict[accept_state][1], formulas_dict[accept_state][2]])
            except IndexError:
                only_formulas.append([formulas_dict[accept_state][1]])

        return only_formulas


    fa_a_only_formulas = get_only_formulas(fa_a_formulas_dict)
    fa_b_only_formulas = get_only_formulas(fa_b_formulas_dict)
    #print(fa_a_only_formulas)  # DEBUG
    #print(fa_b_only_formulas)  # DEBUG

    smt = Solver()
    fa_a_var = Int('fa_a_var')
    fa_b_var = Int('fa_b_var')

    for fa_a_id in fa_a_only_formulas:
        for fa_b_id in fa_b_only_formulas:
            smt.push()
            smt.add(fa_a_var >= 0, fa_b_var >= 0)
            smt.add(fa_a_id[0] + fa_a_id[1] * fa_a_var == fa_b_id[0] + fa_b_id[1] * fa_b_var)

            if smt.check() == sat:
                #print(smt.model())  # DEBUG
                return True

            smt.pop()

    return False


def change_formulas_variable(formulas_dict, new_var):
    """
    OBSOLETE
    Change variable symbol in formulas for handle and loop automaton.
    :param formulas_dict: Dictionary with formulas for handle and loop automaton
    :param new_var: variable symbol to use instead of the former variable symbol
    :return: formulas dictionary with new variable symbol instead
    """

    for accept_state in formulas_dict:
            for c in formulas_dict[accept_state][1]:
                if c.isalpha():
                    formulas_dict[accept_state][1] = formulas_dict[accept_state][1].replace(c, new_var)

    return formulas_dict


if __name__ == "__main__":
    print("Starting resolve_satisfiability.py.")  #DEBUG
    main()
    print("Ending resolve_satisfiability.py.")  #DEBUG

# End of file #
