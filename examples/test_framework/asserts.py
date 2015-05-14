#!/usr/bin/python3
"""If you run this file, it will stop at the first failing assertion.
"""
import random

diceroll = random.randint(1, 6)
# All but one of these will fail.
assert diceroll == 1
assert diceroll == 2
assert diceroll == 3
assert diceroll == 4
assert diceroll == 5
assert diceroll == 6

assert "Because it's parsing the code first, it works with" < \
       "Multi-line statements too." < \
       "This one will pass."
