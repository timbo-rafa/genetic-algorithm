#!/bin/bash
python3 tsp/main.py --cities 50 \
                --chromosomes 820 \
                --generations 400 \
                --exchange 200 \
                --elite 20 \
                --mprobability 0.20 \
                --populations 2 \
                --workers 4 \
                --verbose 
