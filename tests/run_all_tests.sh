#!/bin/bash

export PYTHONPATH=../src

for file in memory_controller_tests addressing_modes_tests registers_tests opcode_tests_implied opcode_tests_loads opcode_tests_stores opcode_tests_bitshifts opcode_tests_compares opcode_tests_jumps_and_branches opcode_tests_arithmetic cpu6502_tests; do

    python3 $file.py

done