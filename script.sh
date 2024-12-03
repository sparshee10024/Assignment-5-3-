#!/bin/bash

mkdir -p results expected_outputs

TIMEOUT=6

for INPUT_FILE in small.txt medium.txt large.txt; do
    for typ in 0 1 2; do
        echo "Generating output for $INPUT_FILE and type $typ..."
        python3 run.py "$INPUT_FILE" "$typ" > my_outputs/"${INPUT_FILE%.*}"_"$typ".txt 2>&1
        # python3 run.py "$INPUT_FILE" "$typ" 
        # Run the second one to see print statements on terminal.
        if [[ $? -ne 0 ]]; then
            echo "Error generating output for $INPUT_FILE and type $typ. Check correct_code or run.py."
            exit 1
        fi
    done
done