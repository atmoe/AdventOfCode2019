#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

# Get orbit pairs from file, put in dict
orbits = {}
for line in inputFile.readlines():
    orbitArr = line.rstrip().split(")")
    orbits[orbitArr[1]] = orbitArr[0]

inputFile.close()

# for each orbit trace back to COM
numOrbits = 0
for o in orbits:
    numOrbits+=1

    nextObj = orbits[o]
    while nextObj != 'COM':
        numOrbits+=1
        nextObj = orbits[nextObj]

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "Num Orbits = {}".format(numOrbits)
print ""

# Get paths to COM for you and santa
sanPathToCom = []  # will not contain SAN
youPathToCom = []  # will not contain YOU

nextObj = 'YOU'
while nextObj != 'COM':
    nextObj = orbits[nextObj]
    youPathToCom.append(nextObj)

nextObj = 'SAN'
while nextObj != 'COM':
    nextObj = orbits[nextObj]
    sanPathToCom.append(nextObj)

# walk backward from COM until you get to the split point
youPtr = len(youPathToCom)-1
sanPtr = len(sanPathToCom)-1

while sanPathToCom[sanPtr] == youPathToCom[youPtr]:
    youPtr-=1
    sanPtr-=1

transfers = youPtr+1 + sanPtr+1

print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
print "Num Transfers = {}".format(transfers)