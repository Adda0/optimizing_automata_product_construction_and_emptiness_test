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
# ./czech_ssc_linker.sh [-c czech.lnp_file] [-s ssc.def_file] [-o output_file]"
while getopts :c:s:o:h o; do
    case "$o" in
    # input files
    c) # czech.lpn file
        if [ -z "$OPTARG" ]; then # parameter -c without given czech.lpn file following '-c'
            print_stderr "Invalid flag: -c <czech.lpn_file>."
            exit 1;
        else
            if test -f "$OPTARG"; then
                F_CZECH="$OPTARG"
                echo "czech_file_name: $OPTARG"
            else
                print_stderr "No such file: $OPTARG"
                exit 1;
            fi
        fi
        ;;
    s) # ssc.def file
        if [ -z "$OPTARG" ]; then # parameter -s without given ssc.def file following '-s'
            print_stderr "Invalid flag: -s <ssc.def_file>."
            exit 1;
        else
            if test -f "$OPTARG"; then
                F_SSC="$OPTARG"
                echo "ssc_file_name: $OPTARG"
            else
                print_stderr "No such file: $OPTARG"
                exit 1;
            fi
        fi
        ;;
    # output files
    o) # result of the merge
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
        printf "Usage: ./czech_ssc_linker.sh [-c czech.lpn_file] [-s ssc.def_file] [-o output_file]\n\n"
        echo "   [-c czech.lpn_file] –– set czech.lpn file to be merged"
        echo "   [-s ssc.def_file] –– set ssc.def file to be merged"
        echo "   [-o output_file] –– set output file containing the result of merge of both input files"
        exit 0
        ;;
    *) # invalid flag
        print_stderr "Invalid flag: $*."
        exit 1;
        ;;
    esac
done

F_FA_A_ORIG="/mnt/DATA/Data/David/School/projPrax/optimizing_automata_product_construction_and_emptiness_test/basicDFAs/DFA_4s1f_01"

cp "$F_FA_A_ORIG" ./
F_FA_A_NAME=$(basename "$F_FA_A_ORIG")
F_FA_A_STAR="$F_FA_A_NAME"_STAR

#echo "$F_FA_A_STAR" #DEBUG

python3 ./prepare_fa.py "$(pwd)"/"$F_FA_A_NAME"
python3 ./change_transitions.py "$(pwd)"/"$F_FA_A_NAME"_dawdawd "$(pwd)"/"$F_FA_A_STAR"






















echo "Ending run.sh."

# End of file run.sh #
