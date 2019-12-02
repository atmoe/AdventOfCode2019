#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")

fuelRequirementsPart1 = 0
fuelRequirementsPart2 = 0

for line in inputFile.readlines():
    fuel = int(math.floor(int(line)/3.0)) - 2

    fuelRequirementsPart1 += fuel

    while fuel > 0:
        fuelRequirementsPart2 += fuel
        fuel = int(math.floor(int(fuel)/3.0)) - 2

inputFile.close()


print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "Total Fuel = {}".format(fuelRequirementsPart1)


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
print "Total Fuel = {}".format(fuelRequirementsPart2)