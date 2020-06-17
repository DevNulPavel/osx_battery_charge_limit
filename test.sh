#!/usr/bin/env bash

# SMC binary app usage example:
#
# All keys:
# -> ./smc -l
#
# Current value:
# -> ./smc -r -k BCLM
#
# Set value:
# 1. convert dec value to hex using
# -> python -c "print(hex(60))"
#    0x3c
# 2. write 3c value to SMC
# -> sudo ./smc -k BCLM -w 3c

# python3 main.py
# python3 main.py -c
# python3 main.py -s 65
# sudo python3 main.py -s 65
# sudo python3 main.py -r


