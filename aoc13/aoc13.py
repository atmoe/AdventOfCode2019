#!/usr/bin/python

import sys
import math
import itertools
import copy

enableDebug = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getStr(self):
        return "({}, {})".format(self.x, self.y)

def printGrid(locs, robLoc, dir):
    maxX = 0
    maxY = 0
    minX = 0
    minY = 0
    for k in locs.keys():
        if maxX < k[0]: maxX = k[0]
        if minX > k[0]: minX = k[0]
        if maxY < k[1]: maxY = k[1]
        if minY > k[1]: minY = k[1]

    if maxX < robLoc.x: maxX = robLoc.x
    if minX > robLoc.x: minX = robLoc.x
    if maxY < robLoc.y: maxY = robLoc.y
    if minY > robLoc.y: minY = robLoc.y

    grid = []
    for y in range(maxY-minY+1):
        gridRow = []
        for x in range(maxX-minX+1):
            gridRow.append('.')
        grid.append(gridRow)

    for k in locs.keys():

        if locs[k] == 1:
            grid[k[1] - minY][k[0] - minX] = '#'
        else:
            grid[k[1] - minY][k[0] - minX] = '.'

    if robotDir==0: grid[robLoc.y-minY][robLoc.x-minX] = '^'
    if robotDir==1: grid[robLoc.y-minY][robLoc.x-minX] = '>'
    if robotDir==2: grid[robLoc.y-minY][robLoc.x-minX] = 'v'
    if robotDir==3: grid[robLoc.y-minY][robLoc.x-minX] = '<'

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
outputMode = 0
setNextInput = True
nextInput = 0
x      = -1
y      = -1
tileID = -1
blocksSeen = 0
while not term:
    (pc, outputVal, returnMode) = myProgram.runProgram(pc, nextInput, setNextInput)

    term = returnMode == 0
    if term: continue

    if   outputMode == 0: x      = outputVal
    elif outputMode == 1: y      = outputVal
    elif outputMode == 2:
        tileID = outputVal
        if tileID==2:
            blocksSeen+=1 

    outputMode = (outputMode+1)%3


print "blocksSeen = {}".format(blocksSeen)

print "-----------------"
print "---- Part 2------"
print "-----------------"
prog[0] = 2
myProgram = Program(prog)
term = False
pc = 0
outputMode = 0
setNextInput = False
nextInput = 0
x      = -1
y      = -1
tileID = -1
blocksSeen = 0
ballX = 0
barX = 0

maxX=0
maxY=0
score=0
grid = []
for y in range(100):
    gridLine = []
    for x in range(100):
        gridLine.append('.')
    grid.append(gridLine)

while not term:
    # returnmode: 
    #   0 - terminate
    #   1 - output
    #   2 - input
    (pc, outputVal, returnMode) = myProgram.runProgram(pc, nextInput, setNextInput)

    setNextInput = False

    term = returnMode == 0
    if term: continue

    if returnMode == 1:

        if outputMode == 0:
            x = outputVal
            if maxX < x: maxX = x

        elif outputMode == 1:
            y = outputVal
            if maxY < y: maxY = y

        elif outputMode == 2: 
            if (x == -1) and (y == 0):
                score = outputVal
            else:
                tileID = outputVal
                glyph = "."
                if   tileID==0: glyph = '.'
                elif tileID==1: glyph = '#'
                elif tileID==2: glyph = 'X'
                elif tileID==3: glyph = '-'
                elif tileID==4: glyph = 'O'

                if tileID == 4: ballX = x
                if tileID == 3: barX = x

                grid[y][x] = glyph

        outputMode = (outputMode+1)%3

    elif returnMode == 2:
        for r in grid[0:maxY+1]:
            print "".join(r[0:maxX+1])
        print "Score = {}".format(score)

        setNextInput = True

        if   barX < ballX: nextInput =  1
        elif barX > ballX: nextInput = -1
        else:              nextInput =  0


for r in grid[0:maxY+1]:
    print "".join(r[0:maxX+1])
print "Score = {}".format(score)

