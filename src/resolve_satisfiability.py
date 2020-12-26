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

# Main script function
def main():
    fa_a_name = sys.argv[1]
    fa_b_name = sys.argv[2]
    fa_a = symboliclib.parse(fa_a_name)
    fa_b = symboliclib.parse(fa_b_name)

    fa_a.unify_transition_symbols()
    fa_b.unify_transition_symbols()

    fa_a = fa_a.simple_reduce()
    fa_a = fa_a.determinize()

    fa_b = fa_b.simple_reduce()
    fa_b = fa_b.determinize()

    fa_a_formulas_dict = fa_a.count_formulas_for_lfa()
    print(fa_a_formulas_dict)  # DEBUG
    fa_b_formulas_dict = fa_b.count_formulas_for_lfa()
    print(fa_b_formulas_dict)  # DEBUG
    """

    fa_b_formulas_dict = change_formulas_variable(fa_b_formulas_dict, 'l')




    fa_a_only_formulas = get_only_formulas(fa_a_formulas_dict)
    fa_b_only_formulas = get_only_formulas(fa_b_formulas_dict)

    print(fa_a_only_formulas)  # DEBUG
    print(fa_b_only_formulas)  # DEBUG

"""
    """
    (declare-const x Int)
    (declare-const y Int)
    (assert (= x y))
    (check-sat)
    (get-model)
    """


    """
    # Using eval to parse the string.
    x = fa_a_only_formulas[0]
    y = fa_b_only_formulas[0]
    s = "( == )"
    f2 = eval(s)
    print(f2)
    """





def change_formulas_variable(formulas_dict, new_var):
    """
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

def get_only_formulas(formulas_dict):
    only_formulas = []
    for accept_state in formulas_dict:
        only_formulas.append(formulas_dict[accept_state][1])

    return only_formulas








if __name__ == "__main__":
    print("Starting resolve_satisfiability.py.")  #DEBUG
    main()
    print("Ending resolve_satisfiability.py.")  #DEBUG

# End of file #
