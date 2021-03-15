#!/usr/bin/env python3

# ====================================================
# file name: resolve_satisfiability.py
#
# Script to resolve satisfiable of given formulas using Z3 SMT solver.
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

import os
import sys
import symboliclib
#from sa import SA
from lfa import LFA
from z3 import *
from collections import deque


# Main script function
def main():
    fa_a_name = sys.argv[1]
    fa_b_name = sys.argv[2]
    fa_a_orig = symboliclib.parse(fa_a_name)
    fa_b_orig = symboliclib.parse(fa_b_name)

    q_a_states = deque()
    q_b_states = deque()

    q_pair_states = deque()

    q_checked_pairs = {}

    # enqueue the initial states
    for initial_state in fa_a_orig.start:
        q_a_states.append(initial_state)
    for initial_state in fa_b_orig.start:
        q_b_states.append(initial_state)

    # Pair the initial states.
    make_pairs(q_pair_states, q_checked_pairs, q_a_states, q_b_states, False)

    fa_a_handle_and_loop = LFA.get_new()
    fa_b_handle_and_loop = LFA.get_new()

    fa_a_orig.unify_transition_symbols()
    fa_b_orig.unify_transition_symbols()

    while(q_pair_states):
        curr_pair = q_pair_states.popleft()
        q_checked_pairs[curr_pair[1] + ',' + curr_pair[2]] = True
        if curr_pair[0]:
            print('New skip: ' + str(curr_pair))
        else:
            print(curr_pair)

        fa_a_orig.start = {curr_pair[1]}
        fa_b_orig.start = {curr_pair[2]}


        if not curr_pair[0]:
            fa_a_orig.determinize_check(fa_a_handle_and_loop)

            fa_b_orig.determinize_check(fa_b_handle_and_loop)

            fa_a_formulas_dict = fa_a_handle_and_loop.count_formulas_for_lfa()
            #print(fa_a_formulas_dict)  # DEBUG
            fa_b_formulas_dict = fa_b_handle_and_loop.count_formulas_for_lfa()
            #print(fa_b_formulas_dict)  # DEBUG

            satisfiable = check_satisfiability(fa_a_formulas_dict, fa_b_formulas_dict)
            print(satisfiable)
        else:
            satisfiable = True

        if curr_pair[1] in fa_a_orig.final and curr_pair[2] in fa_b_orig.final and satisfiable:
            # Automata have a non-empty intersection. We can end the testing here as we have found a solution.
            #fa_a_handle_and_loop.print_automaton()
            #fa_b_handle_and_loop.print_automaton()
            print('SUCCESS: Automata have a non-empty intersection.')
            exit(0)
        #elif not q_pair_states and not satisfiable:
            # When there is only one branch and satisfiable is False, intersection must be empty. Stop generating another states.
        #    break
        elif satisfiable:
            # Enqueue the following state(s).
            for initial_state in fa_a_orig.start:
                enqueue_next_states(q_a_states, fa_a_orig, initial_state)
            for initial_state in fa_b_orig.start:
                enqueue_next_states(q_b_states, fa_b_orig, initial_state)

            print(q_pair_states)
            make_pairs(q_pair_states, q_checked_pairs, q_a_states, q_b_states)
            print(q_pair_states)

    print("FAILURE: Automata have an empty intersection.")
    exit(1)


def make_pairs(q_pair_states, q_checked_pairs, q_a_states, q_b_states, single_pair = None):
    if single_pair == None:
        single_pair = True if (len(q_a_states) == 1 and len(q_b_states) == 1) else False


    for a_state in q_a_states:
        for b_state in q_b_states:
            if a_state + ',' + b_state not in q_checked_pairs and [single_pair, a_state, b_state] not in q_pair_states:
                q_pair_states.append([single_pair, a_state, b_state])
                q_checked_pairs[a_state + ',' + b_state] = True

    q_a_states.clear()
    q_b_states.clear()

def enqueue_next_states(q_states, fa_orig, curr_state):
    transitions = fa_orig.get_deterministic_transitions(curr_state)

    for trans_symbol in transitions:
        for state_dict_elem in transitions[trans_symbol]:
            for state in state_dict_elem.split(','):
                q_states.append(state)

def check_satisfiability(fa_a_formulas_dict, fa_b_formulas_dict):
    """
    Check satisfiable for formulas using SMT solver Z3.
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


if __name__ == "__main__":
    #print("Starting resolve_satisfiability.py.")  #DEBUG
    main()
    #print("Ending resolve_satisfiability.py.")  #DEBUG

# End of file #
