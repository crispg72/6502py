#!/bin/bash

export PYTHONPATH=../src

for file in memory_controller_tests; do

    python3 $file.py

done