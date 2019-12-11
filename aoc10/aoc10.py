#!/usr/bin/python

import sys
import math
import fractions

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getStr(self):
        return "({}, {})".format(self.x, self.y)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def getAllRays(x, y, width, height):
    return

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

asteroids = []
grid = []
inputFile = open(sys.argv[1], "r")

for y,line in enumerate(inputFile.readlines()):
    gridLine = []
    for x,char in enumerate(line):
        if char == ".":
            gridLine.append(char)
        if char == "#":
            gridLine.append(char)
            asteroids.append(Point(x,y))

    grid.append(gridLine)
inputFile.close()

width  = len(grid[0])
height = len(grid)

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "WxH = {}x{}".format(width,height)
print "----------Grid----------"
for g in grid:
    print "".join(g)
print "------------------------"
print "numAsteroids = {}".format(len(asteroids))

maxVisible = 0
maxAsteroid = Point(0,0)
for a1 in asteroids:
    visibleAsteroids = 0
    for a2 in asteroids:
        if a1 == a2: continue
        x = a2.x - a1.x
        y = a2.y - a1.y
        divisor = gcd(abs(x), abs(y))
        ray = Point(x/divisor, y/divisor)
        
        currPoint = Point(a1.x + ray.x, a1.y + ray.y)
        otherPointSeen = False
        while currPoint.x != a2.x or currPoint.y != a2.y:
            assert currPoint.x >= 0 and currPoint.x < width,  "x traveled outside"
            assert currPoint.y >= 0 and currPoint.y < height, "y traveled outside"

            #print "    walk point = {} [{}]".format(currPoint.getStr(), grid[currPoint.y][currPoint.x])
            if grid[currPoint.y][currPoint.x] == "#":
                otherPointSeen = True

            currPoint.x += ray.x
            currPoint.y += ray.y

        if not otherPointSeen:
            visibleAsteroids+=1
            #print "    hit = {} ray = {}".format(a2.getStr(), ray.getStr())

    if maxVisible < visibleAsteroids:
        maxVisible = visibleAsteroids
        maxAsteroid = a1 

print "maxVisible @ {} = {}".format(maxAsteroid.getStr(), maxVisible)

print "----------------------"
print "---- Part 2 ----------"
print "----------------------"

visibleFromMax = []
for a in asteroids:
    if a == maxAsteroid: continue
    x = a.x - maxAsteroid.x
    y = a.y - maxAsteroid.y
    divisor = gcd(abs(x), abs(y))
    ray = Point(x/divisor, y/divisor)
        
    currPoint = Point(maxAsteroid.x + ray.x, maxAsteroid.y + ray.y)
    otherPointSeen = False
    while currPoint.x != a.x or currPoint.y != a.y:
        assert currPoint.x >= 0 and currPoint.x < width,  "x traveled outside"
        assert currPoint.y >= 0 and currPoint.y < height, "y traveled outside"

        if grid[currPoint.y][currPoint.x] == "#":
            otherPointSeen = True

        currPoint.x += ray.x
        currPoint.y += ray.y

    if not otherPointSeen:
        visibleFromMax.append(a)

orderedAsteroids = []
for a in visibleFromMax:
    ray = Point(a.x - maxAsteroid.x, a.y - maxAsteroid.y)
    if ray.x == 0 and ray.y >=0:
        angle = 90
    elif ray.x == 0 and ray.y < 0:
        angle = 270
    else:
        angle = (180.0/math.pi) * math.atan(ray.y / float(ray.x))

    if ray.x < 0: angle += 180
    if angle < 0: angle += 360
    #print "{} -> {}: {}".format(maxAsteroid.getStr(), a.getStr(), angle)

    angle = (angle+90) % 360

    orderedAsteroids.append((a, angle))
orderedAsteroids.sort(key=lambda c: c[1])

asteroidCount = 0
for a in orderedAsteroids:
    asteroidCount+=1

    #print "{}: {} -> {}: {}".format(asteroidCount, maxAsteroid.getStr(), a[0].getStr(), a[1])
    grid[a[0].y][a[0].x] = str(asteroidCount)

    if asteroidCount == 200:
        print "200th Asteroid = {}".format(a[0].x*100 + a[0].y)





