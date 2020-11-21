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
        nonlocal length
        curr_state = {fa.transitions.get(next(iter(curr_state))).get('*')[0]}
        length += 1


    automaton_name = sys.argv[1]
    fa = symboliclib.parse(automaton_name)

    curr_state = fa.start
    length = 0
    formulas_for_states = {}
    last_state_to_stop = ''

    while True:
        if not curr_state.issubset(fa.final):
            get_next_state()
            curr_state_iter = next(iter(curr_state))
        else:  # current state is also an accept state
            try:
                if not formulas_for_states[curr_state_iter][0]:
                    formulas_for_states[curr_state_iter][0] = True
                    formulas_for_states[curr_state_iter][1] += ' + ' + str(length - int(formulas_for_states[curr_state_iter][1])) + 'k'
                if last_state_to_stop == curr_state_iter:
                    break
            except KeyError:
                formulas_for_states[curr_state_iter] = [False, str(length)]
                last_state_to_stop = curr_state_iter

            get_next_state()

    print(formulas_for_states)










if __name__ == "__main__":
    print("Starting change_transitions.py.")  #DEBUG
    main()
    print("Ending change_transitions.py.")  #DEBUG

# End of file prepare_fa.py #
