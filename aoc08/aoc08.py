#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")

rawVals = [int(i) for i in list(inputFile.readline().rstrip())]

inputFile.close()

width  = 25
height = 6 

numLayers = len(rawVals)/(width*height)

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
# 0, 1, 2
maxCounts = [width*height, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for l in range(numLayers):
    counts    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    layerPtr = l * width * height
    for layerOff in range(width*height):
        counts[rawVals[layerPtr + layerOff]] += 1

    if maxCounts[0] > counts[0]:
        maxCounts = counts


print "result = {}".format(maxCounts[1] * maxCounts[2])


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
finalImage = [2] * width * height
#print rawVals
#print finalImage

for l in range(numLayers):
    layerPtr = l * width * height
    for layerOff in range(width*height):
        if finalImage[layerOff] == 2:
            finalImage[layerOff] = rawVals[layerPtr+layerOff]

finalImageStr = [" "] * width * height
for i in range(width*height):
    if finalImage[i] == 1:
        finalImageStr[i] = "#"

for i in range(height):
    print "".join(finalImageStr[i*width:i*width+width])


