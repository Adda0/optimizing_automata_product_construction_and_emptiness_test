#!/usr/bin/python3

# ====================================================
# file name: count_formula_for_fa.py
#
# Script to count length of words for deterministic handle and loop automaton.
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

import os
import sys
import symboliclib


# Main script function
def main():
    def get_next_state():
        #'q4': {*: ['q3']}
        nonlocal curr_state
        curr_state = {fa.transitions.get(next(iter(curr_state))).get('*')[0]}
        print(curr_state)  #DEBUG
        print(type(curr_state))  #DEBUG


    automaton_name = sys.argv[1]
    fa = symboliclib.parse(automaton_name)

    curr_state = fa.start
    print(curr_state)  #DEBUG
    print(type(curr_state))  #DEBUG

    visited_states = {}

    num = 1

    formula = ''
    handle_length = 0

    handle = True

    print(fa.transitions)




    for state in fa.states:
        if handle:
            if not curr_state in fa.final:
                handle_length += 1
                get_next_state()
            else:
                formula = str(handle_length)
                print(handle_length)
                handle = False
    print(formula)










if __name__ == "__main__":
    print("Starting change_transitions.py.")  #DEBUG
    main()
    print("Ending change_transitions.py.")  #DEBUG

# End of file prepare_fa.py #
