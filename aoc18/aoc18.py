#!/usr/bin/python

import sys
import math
import copy

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{x}_{y}'

class Cave:
    def __init__(self, pos):
        self.keys = []
        self.steps = 0
        self.pos = pos

cave = []
inputFile = open(sys.argv[1], "r")
for line in inputFile.readlines():
    cave.append(list(line.rstrip()))
inputFile.close()

initPos = Pos(-1,-1)
keys  = []
doors = []
for y,row in enumerate(cave):
    for x,val in enumerate(row):
        if val == '@':
            initPos.x = x
            initPos.y = y
            cave[y][x] = '.'
        elif val.isalpha() and val.islower():
            keys.append((val,x,y))
        elif val.isalpha() and val.isupper():
            doors.append((val,x,y))

print(initPos)
print(keys)
print(doors)


print("----------------------")
print("---- Part 1 ----------")
print("----------------------")
caves = []
caves.append(Cave(initPos))

allKeysFound = False
while not allKeysFound:
    c = caves.pop()
    if len(c.keys) == len(keys):
        allKeysFound = True
        print(c.steps)
        break
    
    # determine all moves to a key from current position, create new cave instance for each
    moves = []
    visited = {}
    visited[str(c.pos)] = True
    moves.append([0, c.pos])
    while len(moves) > 0:
        m = moves.pop()
        dist = m[0]
        loc  = m[1]
        up    = Pos(loc.x,   loc.y-1)
        down  = Pos(loc.x,   loc.y+1)
        left  = Pos(loc.x-1, loc.y)
        right = Pos(loc.x+1, loc.y)

        print(up.y)
        print(up)
        print(down)
        print(left)
        print(right)


        dirs = []
        if str(up)    not in visited.keys() and up.y   >= 0:            dirs.append(up)
        if str(down)  not in visited.keys() and down.y < len(cave):     dirs.append(down)
        if str(left)  not in visited.keys() and left.x >= 0:            dirs.append(left)
        if str(right) not in visited.keys() and right.x < len(cave[0]): dirs.append(right)


        for d in dirs:
            visited[str(d)] = True
            val = cave[d.y][d.x] 
            print(val)
            if val == '.':
                moves.append([dist+1, d])
            elif val.isalpha() and val.isupper() and val.lower() in c.keys:
                moves.append([dist+1, d])
            elif val.isalpha() and val.islower() and val not in c.keys:
                print(f'{val} {dist} {c.keys}')
                newCave = Cave(d)
                newCave.steps = c.steps + dist + 1
                newCave.keys = copy.deepcopy(c.keys)
                newCave.keys.append(val)
                caves.append(newCave)


    caves.sort(key=lambda x: x.steps, reverse=True)


print("----------------------")
print("---- Part 2 ----------")
print("----------------------")
