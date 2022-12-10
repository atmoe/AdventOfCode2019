#!/usr/bin/python

import sys
import math

sys.path.append("..")
from lib import intcode

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

codeStr = inputFile.readline().rstrip().split(",")
instructions = [int(i) for i in codeStr]
inputFile.close()

print("----------------------")
print("---- Part 1 ----------")
print("----------------------")
ic = intcode.Intcode(instructions, [])
ic.program[1] = 12
ic.program[2] = 2
ic.exec()
print(ic.program[0])

print("----------------------")
print("---- Part 2 ----------")
print("----------------------")
for i in range(100):
    for j in range(100):
        ic = intcode.Intcode(instructions, [])
        ic.program[1] = i
        ic.program[2] = j
        ic.exec()
        if ic.program[0] == 19690720:
            print(f'{i*100+j}')
            quit()

