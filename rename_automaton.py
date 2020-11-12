#!/usr/bin/python3

# ====================================================
# file name: rename_automaton.py
#
# Script to rename automaton with name given by the argument
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

import os
import sys


# Main script function
def main():
    # names of used files
    fa_name = sys.argv[1]  # automaton file
    fa_name_dest = fa_name + '_renamed'

    new_name = sys.argv[2]

    try:
        file_fa = open(fa_name, "r")
        file_fa_dest = open(fa_name_dest, "w+")
    except IOError:
        file_name = os.path.basename(__file__)
        print('ERROR: ' + file_name + ': Opening file failed.', sep='', end='\n', file=sys.stderr)
        exit()


    for line in file_fa:
        if 'Automaton' in line:
            splitted_line = line.split(' ', 3)
            splitted_line[1] = new_name
            file_fa_dest.write(splitted_line[0]+ ' ' + splitted_line[1] + ' ' + splitted_line[2])
        else:
            file_fa_dest.write(line)

    file_fa.close()
    file_fa_dest.close()

    os.rename(fa_name_dest, fa_name)



if __name__ == "__main__":
    print("Starting rename_automaton.py.")  # DEBUG
    main()
    print("Ending rename_automaton.py.")  # DEBUG

# End of file prepare_fa.py #
