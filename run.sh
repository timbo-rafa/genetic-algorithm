#!/bin/bash
python3 main.py --cities 200 \
                --chromosomes 220 \
                --generations 100000 \
                --exchange 200 \
                --elite 20 \
                --mprobability 0.20 \
                --populations 6 \
                --workers 4 \
                --verbose 
