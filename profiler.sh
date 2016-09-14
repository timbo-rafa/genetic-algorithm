#!/bin/bash
set -v
python3 -m cProfile       \
        -s time           \
        -o profiling.data \
  main.py -n 200  \
          -c 220  \
          -g 1000 \
          -x 50   \
          -e 20   \
          -m 0.20 \
          -p 2    \
          -w 2    \
          -v
echo stats | python3 -m pstats profiling.data > profiling.out
