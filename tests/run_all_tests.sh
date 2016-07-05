#!/bin/bash

export PYTHONPATH=../src

for file in memory_controller_tests opcode_tests addressing_modes_tests registers_tests; do

    python3 $file.py

done