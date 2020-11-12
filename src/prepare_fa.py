#!/usr/bin/python3

# ====================================================
# file name: prepar_fa.py
#
# Script to prepare given finite automata for optimizing
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

import sys
import symboliclib


# Main script function
def main():
    automaton_name = sys.argv[1]

    fa_a = symboliclib.parse(automaton_name)
    name = fa_a.get_automaton_name()
    print(name)

    fa_a.rename_automaton("test")
    name = fa_a.get_automaton_name()
    print(name)
    fa_a = fa_a.simple_reduce()
    fa_a = fa_a.determinize()
    #fa_a.print_automaton() #DEBUG

    fa_a.change_initial_state(fa_a.states)

    fa_a.print_automaton(automaton_name)






if __name__ == "__main__":
    print("Starting prepare_fa.py.")  # DEBUG
    main()
    print("Ending prepare_fa.py.")  # DEBUG

# End of file prepare_fa.py #
