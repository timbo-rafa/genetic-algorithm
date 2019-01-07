#!/bin/bash

# export PYTHONPATH=.
. ./sh/setup.sh
nosetests -v --processes=8 --process-timeout=60 test
