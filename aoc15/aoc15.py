#!/usr/bin/python

import sys
import math
import itertools
import copy

enableDebug = False

class TreeNode:
    def __init__(self, parent, loc):
        self.parent = parent
        self.loc    = loc
        self.val    = 3    # 3 means unknown

        self.children = []

    def setVal(self, val):
        self.val = val

    def addChild(self, loc):
        self.children.append(TreeNode(self, loc))

    def getParent(self):
        return self.parent

    def getNextToVisit(self):
        # visit unknown children
        for c in self.children:
            if c.val == 3: return c

        # go to parent if all children visited
        return self.parent

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getStr(self):
        return "({}, {})".format(self.x, self.y)

    def getHashStr(self):
        return "{}_{}".format(self.x, self.y)

def printGrid(locs, robLoc):
    maxX = 0
    maxY = 0
    minX = 0
    minY = 0
    for key in locs.keys():
        loc = locs[key][1]
        if maxX < loc.x: maxX = loc.x
        if minX > loc.x: minX = loc.x
        if maxY < loc.y: maxY = loc.y
        if minY > loc.y: minY = loc.y

    if maxX < robLoc.x: maxX = robLoc.x
    if minX > robLoc.x: minX = robLoc.x
    if maxY < robLoc.y: maxY = robLoc.y
    if minY > robLoc.y: minY = robLoc.y

    grid = []
    for y in range(maxY-minY+1):
        gridRow = []
        for x in range(maxX-minX+1):
            gridRow.append('?')
        grid.append(gridRow)

    for key in locs.keys():
        (val, loc) = locs[key]

        if val == 0:
            grid[loc.y - minY][loc.x - minX] = '#'
        elif val == 1:
            grid[loc.y - minY][loc.x - minX] = '.'
        elif val == 2:
            grid[loc.y - minY][loc.x - minX] = 'X'
        else:
            assert "invalid grid hash value"

    grid[robotLoc.y-minY][robotLoc.x-minX] = "D"
    grid[0-minY][0-minX] = "0"

    for g in grid:
        print "".join(g)
    

def getOpStr(op):
    assert (op > 0 and op < 10) or op == 99, "invalid op! {}".format(op)
    if   op == 1: return "ADD"
    elif op == 2: return "MUL"
    elif op == 3: return "INPUT"
    elif op == 4: return "OUTPUT"
    elif op == 5: return "BNEZ"
    elif op == 6: return "BEZ"
    elif op == 7: return "LT"
    elif op == 8: return "EQ"
    elif op == 9: return "RELUPDATE"
    elif op == 99: return "TERMINATE"

class Program:
    def __init__(self,prog):
        self.program = copy.deepcopy(prog)
        self.relBase = 0

    # Return Tuple is PC, Outputs[2], Terminated
    def runProgram(self, initPC, inputVal, setInput):
        pc = initPC
        terminated = False
        while pc < len(self.program) and not terminated:

            opRaw  = self.program[pc]

            op    = opRaw % 100
            pmode = [(opRaw / 100) % 10, (opRaw / 1000) % 10, (opRaw / 10000) % 10]

            if enableDebug: 
                print "PC[{}]\t{}\top={}".format(pc, getOpStr(op), opRaw)

            if op == 99:
                return (pc, 13131313, 0)

            ### Decode ###
            opIsJump = False
            if op == 1 or op == 2:
                num_params = 3
                dst_param  = 2
            elif op == 3:
                num_params = 1
                dst_param  = 0
            elif op == 4:
                num_params = 1
                dst_param  = -1 # no destination for read
            elif op == 5 or op == 6:
                num_params = 2
                dst_param  = -1 # no destination for jump
                opIsJump = True
            elif op == 7 or op == 8:
                num_params = 3
                dst_param  = 2
            elif op == 9:
                num_params = 1
                dst_param  = -1
            else:
                assert "invalid op"

            # increment to params
            pc += 1

            params       = []
            for i in range(num_params):
                paramIndex = -1
                if   pmode[i] == 2:   paramIndex = self.program[pc+i] + self.relBase # relative mode (affects destinations too)
                elif i == dst_param:  paramIndex = self.program[pc+i]                # destination parameter
                elif pmode[i] == 0:   paramIndex = self.program[pc+i]                # position mode
                elif pmode[i] == 1:   paramIndex = pc+i                         # immediate mode
                else:
                    assert "invalid pmode"

                # allocation check
                if paramIndex >= len(self.program):
                    self.program = self.program + ([0] * (paramIndex - len(self.program) + 1))

                if i == dst_param:
                    params.append(paramIndex)
                else:
                    params.append(self.program[paramIndex])

                if enableDebug:
                    print "\tP{} | pmode = {:1d} | param = {:10d} | pIdx = {:5d} | val = {:10d} | isDst = {:1} |".format(i, pmode[i], self.program[pc+i], paramIndex, params[-1], i==dst_param)

            jumpPtr = -1
            if op == 1:
                # Add
                self.program[params[dst_param]] = params[0] + params[1]
                if enableDebug: print "\tADD: {} = {} + {}".format(self.program[params[dst_param]], params[0], params[1])
            elif op == 2:
                # Mul
                self.program[params[dst_param]] = params[0] * params[1]
                if enableDebug: print "\tMUL: {} = {} * {}".format(self.program[params[dst_param]], params[0], params[1])
            elif op == 3:
                # Input
                if setInput:
                    self.program[params[dst_param]] = inputVal
                    setInput=False
                else:
                    return (pc-1, 13131313, 2)

                if enableDebug: print "\tINPUT: {}".format(inputVal)

            elif op == 4:
                # Output
                #print "OUTPUT: {}".format(params[0])
                return (pc+num_params, params[0], 1)
            elif op == 5:
                # branch NEZ
                if params[0] != 0:
                    jumpPtr = params[1]
                else:
                    jumpPtr = pc + num_params
                if enableDebug: print "\tBRANCH NEZ: val={} to={} finalPtr={}".format(params[0], params[1], jumpPtr)
            elif op == 6:
                # branch EZ
                if params[0] == 0:
                    jumpPtr = params[1]
                else:
                    jumpPtr = pc + num_params
                if enableDebug: print "\tBRANCH EZ: val={} to={} finalPtr={}".format(params[0], params[1], jumpPtr)
            elif op == 7:
                # LT
                if params[0] < params[1]:
                    self.program[params[dst_param]] = 1
                else:
                    self.program[params[dst_param]] = 0

                if enableDebug: print "\tLT: {} = ({} < {})".format(self.program[params[dst_param]], params[0], params[1])
            elif op == 8:
                # EQ
                if params[0] == params[1]:
                    self.program[params[dst_param]] = 1
                else:
                    self.program[params[dst_param]] = 0
                if enableDebug: print "\tEQ: {} = ({} == {})".format(self.program[params[dst_param]], params[0], params[1])
            elif op == 9:
                # Relative base update
                if enableDebug: print "\tREL_UPDATE: {} = {} + {}".format(self.relBase + params[0], self.relBase, params[0])
                self.relBase = self.relBase + params[0]
            else:
                assert "invalid opcode: {}".format(op)

            if opIsJump:
                pc = jumpPtr
            else:
                pc += num_params

            if enableDebug: print "=================================================================================================="

        assert "reached end of program without hitting term instruction"

### Main Program

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputsStr = inputFile.readline().rstrip().split(",")
prog = [int(i) for i in inputsStr]
inputFile.close()


print "-----------------"
print "---- Part 1------"
print "-----------------"

myProgram = Program(prog)
term = False
pc = 0

robotLoc = Point(0,0)
gridHash = {}
gridHash[robotLoc.getHashStr()] = (1, robotLoc)

treeRoot = TreeNode(None, Point(0,0))
treeRoot.setVal(1)
treeRoot.addChild(Point(-1, 0))
treeRoot.addChild(Point( 1, 0))
treeRoot.addChild(Point( 0,-1))
treeRoot.addChild(Point( 0, 1))

currNode = treeRoot.getNextToVisit()
setNextInput = False
if currNode.loc.y < robotLoc.y: nextInput = 1 # north
if currNode.loc.y > robotLoc.y: nextInput = 2 # south
if currNode.loc.x < robotLoc.x: nextInput = 3 # west
if currNode.loc.x > robotLoc.x: nextInput = 4 # east

nextIsInput = True

step=0
while not term:
    (pc, outputVal, returnMode) = myProgram.runProgram(pc, nextInput, setNextInput)
    setNextInput=False

    if returnMode == 0:
        term = True
        assert returnMode != 0, "terminate not expected!"
        continue

    elif returnMode == 1:
        # OUTPUT
        assert not nextIsInput, "incorrect timing, expecting output"
        nextIsInput = True

        #print currNode.loc.getStr()

        if outputVal == 0:
            #print "WALL"
            # set wall position
            #assert not currNode.loc.getHashStr() in gridHash, "Revisited wall check!"

            gridHash[currNode.loc.getHashStr()] = (outputVal, currNode.loc)

            # set to wall
            currNode.setVal(outputVal)

            # robot didn't move, move pointer to next child
            currNode = currNode.getParent().getNextToVisit()

        elif outputVal == 1 or outputVal == 2:
            #print "OPEN SPACE"
            # move robot
            robotLoc = currNode.loc 

            # add more possible locations
            if not robotLoc.getHashStr() in gridHash:
                # set open position
                gridHash[robotLoc.getHashStr()] = (outputVal, robotLoc)
                currNode.setVal(outputVal)

                north = Point(robotLoc.x,   robotLoc.y-1)
                south = Point(robotLoc.x,   robotLoc.y+1)
                west  = Point(robotLoc.x-1, robotLoc.y)
                east  = Point(robotLoc.x+1, robotLoc.y)

                # add neighbor points to check
                #  - ensure visited points are not added
                if not north.getHashStr() in gridHash: currNode.addChild(north)
                if not south.getHashStr() in gridHash: currNode.addChild(south)
                if not west.getHashStr()  in gridHash: currNode.addChild(west)
                if not east.getHashStr()  in gridHash: currNode.addChild(east)

                currNode = currNode.getNextToVisit()

            else:
                # this branch only taken when traversing backwards
                assert gridHash[robotLoc.getHashStr()][0] == outputVal, "Prior visit was not the same! prev: {}  curr: {}".format(gridHash[robotLoc.getHashStr()][0], outputVal)

                currNode = currNode.getNextToVisit()

        else:
            assert "illegal output value! {}".format(outputVal)

    elif returnMode == 2:
        # INPUT
        assert nextIsInput, "incorrect timing, expecting input"
        nextIsInput = False

        setNextInput = True

        assert currNode.loc.x == robotLoc.x or currNode.loc.y == robotLoc.y, "node is more than one away from robot"
        assert currNode.loc.x != robotLoc.x or currNode.loc.y != robotLoc.y, "node is same as robot"

        if currNode.loc.y < robotLoc.y: nextInput = 1 # north
        if currNode.loc.y > robotLoc.y: nextInput = 2 # south
        if currNode.loc.x < robotLoc.x: nextInput = 3 # west
        if currNode.loc.x > robotLoc.x: nextInput = 4 # east

    else:
        assert "invalid return value"

    # terminate if no positions left to check
    #   - determined by trying to go to parent of root
    if currNode == None:  ### FIXME does comparing against "None" work?
        term = True


    #if nextIsInput: 
    #    printGrid(gridHash, robotLoc)
    #    print "---------------------------------------------"


# Get Grid
maxX = 0
maxY = 0
minX = 0
minY = 0
for key in gridHash.keys():
    loc = gridHash[key][1]
    if maxX < loc.x: maxX = loc.x
    if minX > loc.x: minX = loc.x
    if maxY < loc.y: maxY = loc.y
    if minY > loc.y: minY = loc.y

grid = []
for y in range(maxY-minY+1):
    gridRow = []
    for x in range(maxX-minX+1):
        gridRow.append(".")
    grid.append(gridRow)

for key in gridHash.keys():
    (val, loc) = gridHash[key]
    if val == 0: grid[loc.y - minY][loc.x - minX] = "#"
    if val == 1: grid[loc.y - minY][loc.x - minX] = "."
    if val == 2: grid[loc.y - minY][loc.x - minX] = "X"

for g in grid:
    print "".join(g)

oxygenFound = False
step=0
pointStack = [Point(0,0)]
pointStackNext = []
while not oxygenFound:

    for p in pointStack:
        if grid[p.y - minY][p.x - minX] == "X":
            oxygenFound = True

        if grid[p.y     - minY][p.x - 1 - minX] != "#": pointStackNext.append(Point(p.x-1, p.y))
        if grid[p.y     - minY][p.x + 1 - minX] != "#": pointStackNext.append(Point(p.x+1, p.y))
        if grid[p.y - 1 - minY][p.x     - minX] != "#": pointStackNext.append(Point(p.x,   p.y-1))
        if grid[p.y + 1 - minY][p.x     - minX] != "#": pointStackNext.append(Point(p.x,   p.y+1))

        grid[p.y-minY][p.x-minX] = "#"

    #print "------------------"
    #print step
    #for g in grid:
    #    print "".join(g)

    if oxygenFound: continue

    pointStack = copy.deepcopy(pointStackNext)
    pointStackNext = []
    #if step == 256:
    #    oxygenFound = True
    #    continue

    step+=1

print "minimum steps = {}".format(step)



print "-----------------"
print "---- Part 2------"
print "-----------------"
grid = []
for y in range(maxY-minY+1):
    gridRow = []
    for x in range(maxX-minX+1):
        gridRow.append(".")
    grid.append(gridRow)

for key in gridHash.keys():
    (val, loc) = gridHash[key]
    if val == 0: grid[loc.y - minY][loc.x - minX] = "#"
    if val == 1: grid[loc.y - minY][loc.x - minX] = "."
    if val == 2:
        grid[loc.y - minY][loc.x - minX] = "O"
        oxygenLoc = loc

oxygenFilled = False
step=0
pointStack = [oxygenLoc]
pointStackNext = []
while not oxygenFilled:

    for p in pointStack:
        if grid[p.y     - minY][p.x - 1 - minX] == ".": pointStackNext.append(Point(p.x-1, p.y))
        if grid[p.y     - minY][p.x + 1 - minX] == ".": pointStackNext.append(Point(p.x+1, p.y))
        if grid[p.y - 1 - minY][p.x     - minX] == ".": pointStackNext.append(Point(p.x,   p.y-1))
        if grid[p.y + 1 - minY][p.x     - minX] == ".": pointStackNext.append(Point(p.x,   p.y+1))

        grid[p.y-minY][p.x-minX] = "O"

    #print "------------------"
    #print step
    #for g in grid:
    #    print "".join(g)

    pointStack = copy.deepcopy(pointStackNext)
    pointStackNext = []
    #if step == 3:
    #    oxygenFilled = True
    #    continue

    if len(pointStack) == 0: 
        oxygenFilled=True
        continue

    step+=1

print "minimum steps = {}".format(step)
