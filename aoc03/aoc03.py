#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

class Point:
    def __init__(self, x, y):
        self.x         = x
        self.y         = y

    def printMe(self):
        print "({},{})".format(self.x, self.y)

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def intersects(self, l):
        return False

    def printMe(self):
        print "({},{}) -> ({},{})".format(self.p1.x, self.p1.y, self.p2.x, self.p2.y)


inputFile = open(sys.argv[1], "r")

wire1 = inputFile.readline().rstrip().split(",")
wire2 = inputFile.readline().rstrip().split(",")

inputFile.close()


### Part 1 ###
wire1_points = {}
curr_point = Point(0,0)
for w in wire1:
    direction = w[0]
    dist      = int(w[1:])
    for d in range(dist):
        if w[0] == "R":
            curr_point = Point(curr_point.x + 1, curr_point.y)
        if w[0] == "L":
            curr_point = Point(curr_point.x - 1, curr_point.y)
        if w[0] == "U":
            curr_point = Point(curr_point.x, curr_point.y - 1)
        if w[0] == "D":
            curr_point = Point(curr_point.x, curr_point.y + 1)

        curr_point_str = str(curr_point.x) + "_" + str(curr_point.y)
        wire1_points[curr_point_str] = curr_point


minDist = 1000000000
curr_point = Point(0,0)
for w in wire2:
    direction = w[0]
    dist      = int(w[1:])
    for d in range(dist):
        if w[0] == "R":
            curr_point = Point(curr_point.x + 1, curr_point.y)
        if w[0] == "L":
            curr_point = Point(curr_point.x - 1, curr_point.y)
        if w[0] == "U":
            curr_point = Point(curr_point.x, curr_point.y - 1)
        if w[0] == "D":
            curr_point = Point(curr_point.x, curr_point.y + 1)

        curr_point_str = str(curr_point.x) + "_" + str(curr_point.y)
        if curr_point_str in wire1_points:
            print "intersection @ ({}, {})".format(curr_point.x, curr_point.y)
            if minDist > abs(curr_point.x) + abs(curr_point.y):
                minDist = abs(curr_point.x) + abs(curr_point.y)


print "------" 
for p in wire1_points:
    print p
print "------" 

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "minDist = {}".format(minDist)

### Part 2 ###
wire1_points = {}
curr_point = Point(0,0)
steps = 0
for w in wire1:
    direction = w[0]
    dist      = int(w[1:])
    for d in range(dist):
        steps += 1

        if w[0] == "R":
            curr_point = Point(curr_point.x + 1, curr_point.y)
        if w[0] == "L":
            curr_point = Point(curr_point.x - 1, curr_point.y)
        if w[0] == "U":
            curr_point = Point(curr_point.x, curr_point.y - 1)
        if w[0] == "D":
            curr_point = Point(curr_point.x, curr_point.y + 1)

        curr_point_str = str(curr_point.x) + "_" + str(curr_point.y)
        wire1_points[curr_point_str] = steps


minSteps = 1000000000
curr_point = Point(0,0)
steps = 0
for w in wire2:
    direction = w[0]
    dist      = int(w[1:])
    for d in range(dist):
        steps += 1

        if w[0] == "R":
            curr_point = Point(curr_point.x + 1, curr_point.y)
        if w[0] == "L":
            curr_point = Point(curr_point.x - 1, curr_point.y)
        if w[0] == "U":
            curr_point = Point(curr_point.x, curr_point.y - 1)
        if w[0] == "D":
            curr_point = Point(curr_point.x, curr_point.y + 1)

        curr_point_str = str(curr_point.x) + "_" + str(curr_point.y)
        if curr_point_str in wire1_points:
            print "intersection @ ({}, {})".format(curr_point.x, curr_point.y)
            totalSteps = wire1_points[curr_point_str] + steps
            if minSteps > totalSteps:
                minSteps = totalSteps



print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
print "minSteps = {}".format(minSteps)
