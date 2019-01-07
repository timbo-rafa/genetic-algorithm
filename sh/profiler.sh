#!/bin/bash
set -v
. ./sh/setup.sh
python3 -m cProfile                  \
        -s time                      \
        -o profiling/profiling.data  \
  tsp/main.py -n 200  \
          -c 220  \
          -g 1000 \
          -x 50   \
          -e 20   \
          -m 0.20 \
          -p 2    \
          -w 2    \
          -v
echo -e "sort time\nstats" | python3 -m pstats profiling/profiling.data > profiling/profiling.out
