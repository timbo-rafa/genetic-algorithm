#!/bin/bash
python3 main.py --cities 50 \
                --chromosomes 800 \
                --generations 1000 \
                --exchange 200 \
                --elite 20 \
                --mprobability 0.20 \
                --populations 2 \
                --workers 4 \
                --verbose 
