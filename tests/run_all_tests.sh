#!/bin/bash

export PYTHONPATH=../src

for file in memory_controller_tests opcode_tests opcode_tests_loads opcode_tests_stores opcode_tests_jumps_and_branches addressing_modes_tests registers_tests cpu6502_tests; do

    python3 $file.py

done