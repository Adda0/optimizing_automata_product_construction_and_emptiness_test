#!/bin/sh

# ====================================================
# file name: run.sh
#
# Base script for optimizing automata product constract and emptiness test
# ====================================================
# project: IP1 | Optimizing Automata Product Construction and Emptiness Test
# "Optimalizace automatové konstrukce produktu a testu prázdnosti jazyka"
#
# author: David Chocholatý (xchoch08), FIT BUT
# ====================================================

export POSIXLY_CORRECT=yes

echo "Starting ruh.sh."


# functions
print_stderr() { printf "%s\n" "$*" >&2; } # print message to stderr (newline character included): print_stderr "<message>"

# default files
F_FA_A_ORIG=""
F_FA_B_ORIG=""

# handle given arguments
# ./run.sh [-a finite_automaton_A] [-b finite_automaton_B] [-o output]"
while getopts :a:b:o:h o; do
    case "$o" in
    # input files
    a) # finite_automaton_A file
        if [ -z "$OPTARG" ]; then # parameter -a without given finite_automaton_A file following '-a'
            print_stderr "Invalid flag: -a <finite_automaton_A_file>."
            exit 1;
        else
            if test -f "$OPTARG"; then
                F_FA_A_ORIG="$OPTARG"
                echo "finite_automaton_A_file: $OPTARG"
            else
                print_stderr "No such file: $OPTARG"
                exit 1;
            fi
        fi
        ;;
    b) # finite_automaton_B file
        if [ -z "$OPTARG" ]; then # parameter -b without given finite_automaton_A file following '-b'
            print_stderr "Invalid flag: -b <finite_automaton_B_file>."
            exit 1;
        else
            if test -f "$OPTARG"; then
                F_FA_B_ORIG="$OPTARG"
                echo "finite_automaton_B_file: $OPTARG"
            else
                print_stderr "No such file: $OPTARG"
                exit 1;
            fi
        fi
        ;;
    # output files
    o) # result //TODO
        if [ -z "$OPTARG" ]; then # parameter -o without given output file following '-o'
            print_stderr "Invalid flag: -o <output_file>."
            exit 1;
        else
            if ! test -f "$OPTARG"; then
                case $OPTARG in (/*) pathchk -pP -- "$OPTARG";; (*) mkdir -p "${OPTARG%/*}" && touch "$OPTARG";; esac
                F_OUTPUT="$OPTARG"
                echo "output_file_name: $OPTARG"
                #exit 1;
            fi

            F_OUTPUT="$OPTARG"
            echo "output_file_name: $OPTARG"
        fi
        ;;
    h) # help
        printf "Usage: ./run.sh [-a finite_automaton_A_file] [-b finite_automaton_B_file] [-o output]\n\n"
        echo "   [-a finite_automaton_A_file] –– set finite_automaton_A file to be Timbuk description of finite automaton A"
        echo "   [-b finite_automaton_B_file] –– set finite_automaton_B file to be Timbuk description of finite automaton B"
        echo "   [-o output_file] –– set output file containing the result"
        exit 0
        ;;
    *) # invalid flag
        print_stderr "Invalid flag: $*."
        exit 1;
        ;;
    esac
done

cp "$F_FA_A_ORIG" ./
F_FA_A_NAME=$(basename "$F_FA_A_ORIG")

#cp "$F_FA_B_ORIG" ./
#F_FA_B_NAME=$(basename "$F_FA_B_ORIG")

#python3 ./remove_comments_from_fa.py "$(pwd)"/"$F_FA_A_NAME" "$(pwd)"/"$F_FA_A_NAME"_no_comments

#echo "$F_FA_A_STAR" #DEBUG

#python3 ./prepare_fa.py "$(pwd)"/"$F_FA_A_NAME"

# set all transitons to '*'
python3 ./change_transitions.py "$(pwd)"/"$F_FA_A_NAME" "$(pwd)"/"$F_FA_A_NAME"_ASTERISK

# determinize the FA with '*' transitions
python3 ./determinize_fa.py "$(pwd)"/"$F_FA_A_NAME"_ASTERISK "$(pwd)"/"$F_FA_A_NAME"_DETERMINIZED



















echo "Ending run.sh."

# End of file run.sh #
