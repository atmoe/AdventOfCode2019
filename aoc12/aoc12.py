#!/usr/bin/python

import sys
import math
import re

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
        print "pos=<x={:3}, y={:3}, z={:3}>, vel=<x={:3}, y={:3}, z={:3}>".format(self.pos.x, self.pos.y, self.pos.z, self.vel.x, self.vel.y, self.vel.z)



def applyGravity(m1, m2):
    m1Update = Vector3(0,0,0)
    m2Update = Vector3(0,0,0)
    if m1.pos.x > m2.pos.x:
        m1Update.x = -1
        m2Update.x =  1
    elif m1.pos.x < m2.pos.x:
        m1Update.x =  1
        m2Update.x = -1

    if m1.pos.y > m2.pos.y:
        m1Update.y = -1
        m2Update.y =  1
    elif m1.pos.y < m2.pos.y:
        m1Update.y =  1
        m2Update.y = -1

    if m1.pos.z > m2.pos.z:
        m1Update.z = -1
        m2Update.z =  1
    elif m1.pos.z < m2.pos.z:
        m1Update.z =  1
        m2Update.z = -1

    m1.updateVel(m1Update)
    m2.updateVel(m2Update)

def genStateHash(moons):
    stateHash = ""
    for m in moons:
        stateHash+=str(m.pos.x)
        stateHash+=str(m.pos.y)
        stateHash+=str(m.pos.z)
        stateHash+=str(m.vel.x)
        stateHash+=str(m.vel.y)
        stateHash+=str(m.vel.z)

    return stateHash


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")
moons=[]
for line in inputFile.readlines():
    m = re.match("^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
    assert m, "invalid input line!"    

    x = int(m.group(1))
    y = int(m.group(2))
    z = int(m.group(3))

    moons.append(Moon(Vector3(x,y,z)))

inputFile.close()


print "----------------------"
print "---- Part 1 ----------"
print "----------------------"

print "Step = 0"
for m in moons:
    m.printMe()
print "----------------------"

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

    print "Step = {}".format(step)
    for m in moons:
        m.printMe()
    print "----------------------"

totalEnergy = 0
for m in moons:
    moonTotalEnergy = m.getKineticEnergy()*m.getPotentialEnergy()
    totalEnergy += moonTotalEnergy

    print "p={} k={} t={}".format(m.getPotentialEnergy(), m.getKineticEnergy(),moonTotalEnergy)

print "Total Energy = {}".format(totalEnergy)


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"

revisitedState=False
priorStates = {}
step = 0
priorStates[genStateHash(moons)] = 1
while not revisitedState:
    step+=1

    for comb in moonCombos:
        applyGravity(comb[0], comb[1])

    for m in moons:
        m.updatePos()

    stHash = genStateHash(moons)

    if stHash in priorStates:
        revisitedState=True
    else:
        priorStates[stHash] = 1

    if step % 100000 == 0:
        print step


print "Num Steps to Revisit = {}".format(step)
