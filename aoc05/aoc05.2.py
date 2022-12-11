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
ic = intcode.Intcode(instructions, [1])
ic.exec()
print(ic.outputs)

print("----------------------")
print("---- Part 2 ----------")
print("----------------------")
ic = intcode.Intcode(instructions, [5])
ic.exec()
print(ic.outputs)
