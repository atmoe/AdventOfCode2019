#!/usr/bin/python

import sys
import math
import re
import copy

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def plus(self, vec):
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z

class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector3(0,0,0)

    def updatePos(self):
        self.pos.plus(self.vel)

    def updateVel(self, update):
        self.vel.plus(update)

    def getPotentialEnergy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def getKineticEnergy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    def printMe(self):
        print "pos=<x={:5}, y={:5}, z={:5}>, vel=<x={:5}, y={:5}, z={:5}>".format(self.pos.x, self.pos.y, self.pos.z, self.vel.x, self.vel.y, self.vel.z)

    def printPos(self):
        print "{:5} {:5} {:5}".format(self.pos.x, 0,0)#self.pos.y, self.pos.z)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def applyGravity(m1, m2):
    m1Update = Vector3(0,0,0)
    m2Update = Vector3(0,0,0)

    m1Update.x = int(m1.pos.x < m2.pos.x) - int(m1.pos.x > m2.pos.x)
    m2Update.x = int(m1.pos.x > m2.pos.x) - int(m1.pos.x < m2.pos.x)

    m1Update.y = int(m1.pos.y < m2.pos.y) - int(m1.pos.y > m2.pos.y)
    m2Update.y = int(m1.pos.y > m2.pos.y) - int(m1.pos.y < m2.pos.y)

    m1Update.z = int(m1.pos.z < m2.pos.z) - int(m1.pos.z > m2.pos.z)
    m2Update.z = int(m1.pos.z > m2.pos.z) - int(m1.pos.z < m2.pos.z)

    m1.updateVel(m1Update)
    m2.updateVel(m2Update)

def applyGravityOneAxis(m1, m2, axis):
    m1Update = Vector3(0,0,0)
    m2Update = Vector3(0,0,0)

    if axis == 0:
        m1Update.x = int(m1.pos.x < m2.pos.x) - int(m1.pos.x > m2.pos.x)
        m2Update.x = int(m1.pos.x > m2.pos.x) - int(m1.pos.x < m2.pos.x)

    if axis == 1:
        m1Update.y = int(m1.pos.y < m2.pos.y) - int(m1.pos.y > m2.pos.y)
        m2Update.y = int(m1.pos.y > m2.pos.y) - int(m1.pos.y < m2.pos.y)

    if axis == 2:
        m1Update.z = int(m1.pos.z < m2.pos.z) - int(m1.pos.z > m2.pos.z)
        m2Update.z = int(m1.pos.z > m2.pos.z) - int(m1.pos.z < m2.pos.z)

    m1.updateVel(m1Update)
    m2.updateVel(m2Update)


### MAIN PROGRAM ####

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")
moonsInput=[]
for line in inputFile.readlines():
    m = re.match("^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
    assert m, "invalid input line!"    

    x = int(m.group(1))
    y = int(m.group(2))
    z = int(m.group(3))

    moonsInput.append(Moon(Vector3(x,y,z)))

inputFile.close()


print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
moons = copy.deepcopy(moonsInput)
moonCombos = []
moonCombos.append((moons[0], moons[1]))
moonCombos.append((moons[0], moons[2]))
moonCombos.append((moons[0], moons[3]))
moonCombos.append((moons[1], moons[2]))
moonCombos.append((moons[1], moons[3]))
moonCombos.append((moons[2], moons[3]))

for step in range(1,1001):
    for comb in moonCombos:
        applyGravity(comb[0], comb[1])

    for m in moons:
        m.updatePos()

    #print "Step = {}".format(step)
    #for m in moons:
    #    m.printMe()
    #print "----------------------"

totalEnergy = 0
for m in moons:
    moonTotalEnergy = m.getKineticEnergy()*m.getPotentialEnergy()
    totalEnergy += moonTotalEnergy

    print "p={} k={} t={}".format(m.getPotentialEnergy(), m.getKineticEnergy(),moonTotalEnergy)

print "Total Energy = {}".format(totalEnergy)


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"

moons = copy.deepcopy(moonsInput)
moonCombos.append((moons[0], moons[1]))
moonCombos.append((moons[0], moons[2]))
moonCombos.append((moons[0], moons[3]))
moonCombos.append((moons[1], moons[2]))
moonCombos.append((moons[1], moons[3]))
moonCombos.append((moons[2], moons[3]))

stepsPerAxis = [-1,-1,-1]
for axis in [0,1,2]:
    step = 0
    revisitedState=False
    while not revisitedState:
        step+=1

        for comb in moonCombos:
            applyGravityOneAxis(comb[0], comb[1], axis)

        for m in moons:
            m.updatePos()

        revisitedState = True
        for idx,m in enumerate(moons):
            if axis == 0: revisitedState &= ((m.pos.x == moonsInput[idx].pos.x) and (m.vel.x == 0))
            if axis == 1: revisitedState &= ((m.pos.y == moonsInput[idx].pos.y) and (m.vel.y == 0))
            if axis == 2: revisitedState &= ((m.pos.z == moonsInput[idx].pos.z) and (m.vel.z == 0))

        if revisitedState:
            stepsPerAxis[axis] = step

print stepsPerAxis
lcmXY  = (stepsPerAxis[0] * stepsPerAxis[1])/gcd(stepsPerAxis[0], stepsPerAxis[1])
lcmXYZ = (stepsPerAxis[2] * lcmXY)/gcd(stepsPerAxis[2], lcmXY)

print "Num Steps to Revisit = {}".format(lcmXYZ)

