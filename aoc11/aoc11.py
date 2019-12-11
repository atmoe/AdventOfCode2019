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

def getOpStr(op):
    if op == 1: return "ADD"
    if op == 2: return "MUL"
    if op == 3: return "INPUT"
    if op == 4: return "OUTPUT"
    if op == 5: return "BNEZ"
    if op == 6: return "BEZ"
    if op == 7: return "LT"
    if op == 8: return "EQ"
    if op == 9: return "RELUPDATE"
    if op == 99: return "TERMINATE"

def getDirStr(dir):
    if dir == 0: return "UP"
    if dir == 1: return "RIGHT"
    if dir == 2: return "DOWN"
    if dir == 3: return "LEFT"

# Return Tuple is PC, Outputs[2], Terminated
def runProgram(program, initPC, inputVal):
    outputs = [-1000, -1000]
    outputsSeen = 0
    setInput = True

    relativeBase = 0
    pc = initPC
    terminated = False
    while pc < len(program) and not terminated:

        opRaw  = program[pc]

        op    = opRaw % 100
        pmode = [(opRaw / 100) % 10, (opRaw / 1000) % 10, (opRaw / 10000) % 10]

        if enableDebug: 
            print "PC[{}]\t{}\top={}".format(pc, getOpStr(op), opRaw)

        if op == 99:
            return (pc, outputs, True)

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
        paramIndices = []
        for i in range(num_params):
            paramIndex = -1
            if   pmode[i] == 2:   paramIndex = program[pc+i] + relativeBase # relative mode (affects destinations too)
            elif i == dst_param:  paramIndex = program[pc+i]                # destination parameter
            elif pmode[i] == 0:   paramIndex = program[pc+i]                # position mode
            elif pmode[i] == 1:   paramIndex = pc+i                         # immediate mode
            else:
                assert "invalid pmode"

            # allocation check
            if paramIndex >= len(program):
                program = program + ([0] * (paramIndex - len(program) + 1))

            if i == dst_param:
                params.append(paramIndex)
            else:
                params.append(program[paramIndex])

            paramIndices.append(paramIndex)

            if enableDebug:
                print "\tP{} | pmode = {:1d} | param = {:10d} | pIdx = {:5d} | val = {:10d} | isDst = {:1} |".format(i, pmode[i], program[pc+i], paramIndex, params[-1], i==dst_param)

        jumpPtr = -1
        if op == 1:
            # Add
            program[params[dst_param]] = params[0] + params[1]
            if enableDebug: print "\tADD: {} = {} + {}".format(program[params[dst_param]], params[0], params[1])
        elif op == 2:
            # Mul
            program[params[dst_param]] = params[0] * params[1]
            if enableDebug: print "\tMUL: {} = {} * {}".format(program[params[dst_param]], params[0], params[1])
        elif op == 3:
            # Input
            if setInput:
                program[params[dst_param]] = inputVal
                setInput=False
            else:
                return (pc-1, outputs, False)

            if enableDebug: print "\tINPUT: {}".format(inputVal)

        elif op == 4:
            # Output
            outputs[outputsSeen] = params[0]
            outputsSeen+=1
            #print "OUTPUT: {}".format(params[0])
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
                program[params[dst_param]] = 1
            else:
                program[params[dst_param]] = 0

            if enableDebug: print "\tLT: {} = ({} < {})".format(program[params[dst_param]], params[0], params[1])
        elif op == 8:
            # EQ
            if params[0] == params[1]:
                program[params[dst_param]] = 1
            else:
                program[params[dst_param]] = 0
            if enableDebug: print "\tEQ: {} = ({} == {})".format(program[params[dst_param]], params[0], params[1])
        elif op == 9:
            # Relative base update
            if enableDebug: print "\tREL_UPDATE: {} = {} + {}".format(relativeBase + params[0], relativeBase, params[0])
            relativeBase = relativeBase + params[0]
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

terminated = False
pc = 0
visitedLocs = {}
robotLoc = Point(0,0)
robotDir = 0 # 0 - up, 1 - right, 2 - down, 3 - left
iteration = 0
#while not terminated:
for i in range(20):
    color = 0
    if robotLoc.getStr() in visitedLocs:
        color = visitedLocs[robotLoc.getStr()]
        #print "r = {} ".format(color),

    returnVal = runProgram(prog, pc, color)

    terminated = returnVal[2]
    if terminated: continue

    pc = returnVal[0]
    color = returnVal[1][0]
    rotate = returnVal[1][1]

    visitedLocs[robotLoc.getStr()] = color

    if rotate == 1: # RIGHT
        robotDir = (robotDir + 1) % 4
    elif rotate == 0: # LEFT
        robotDir = (robotDir - 1 + 4) % 4

    #print robotLoc.getStr(),
    if   robotDir == 0:  robotLoc = Point(robotLoc.x + 0, robotLoc.y - 1)
    elif robotDir == 1:  robotLoc = Point(robotLoc.x + 1, robotLoc.y + 0)
    elif robotDir == 2:  robotLoc = Point(robotLoc.x + 0, robotLoc.y + 1)
    elif robotDir == 3:  robotLoc = Point(robotLoc.x - 1, robotLoc.y + 0)

    #print " -> {} color = {}  dir = {}".format(robotLoc.getStr(), color, getDirStr(robotDir))
    print iteration
    iteration+=1

print "Painted Cells = {}".format(len(visitedLocs.keys()))

print "-----------------"
print "---- Part 2------"
print "-----------------"
