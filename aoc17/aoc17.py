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

    def getHashStr(self):
        return "{}_{}".format(self.x, self.y)

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
                assert False, "invalid op"

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
                    assert False, "invalid pmode"

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
                assert False, "invalid opcode: {}".format(op)

            if opIsJump:
                pc = jumpPtr
            else:
                pc += num_params

            if enableDebug: print "=================================================================================================="

        assert False, "reached end of program without hitting term instruction"

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
nextInput=-1
setNextInput=False

grid    = []
gridRow = []
height = 0
width  = 0

start = Point(0,0)
end   = Point(0,0)

while not term:
    (pc, outputVal, returnMode) = myProgram.runProgram(pc, nextInput, setNextInput)
    setNextInput=False

    if returnMode == 0:
        term = True
        continue

    elif returnMode == 1:
        if outputVal==10:
            if len(gridRow) > 0:
                grid.append(gridRow)
            gridRow=[]
        elif outputVal <= 127:
            gridRow.append(chr(outputVal))

        else:
            assert False, "unexpected output value! {}".format(outputVal)


    elif returnMode == 2:
        assert False, "input not expected!"

    else:
        assert False, "invalid return value"

height = len(grid)
width  = len(grid[0])
print "WxH={}x{}".format(width,height)

alignmentParamSum = 0
for y,row in enumerate(grid):
    for x,col in enumerate(row):

        # cannot have a cross on an edge
        if y==0 or x==0 or y==(len(grid)-1) or x==(len(row)-1): continue

        if y == 40:
            print "{} {}".format(x,y)

        cent  = grid[y][x]=="#"
        up    = grid[y-1][x]=="#"
        down  = grid[y+1][x]=="#"
        left  = grid[y][x-1]=="#"
        right = grid[y][x+1]=="#"

        if cent and up and down and left and right: 
            alignmentParamSum += (x*y)

for g in grid:
    print "".join(g)

print "Alignment Params = {}".format(alignmentParamSum)


print "-----------------"
print "---- Part 2------"
print "-----------------"
prog[0] = 2
myProgram = Program(prog)
term = False
pc = 0
nextInput=-1
setNextInput=False

totalDust = 0

#grid = []

# 0 - main program
# 1 - Function A
# 2 - Function B
# 3 - Function C
# 4 - Continuous output

inputMode = 0
inputPtr  = 0

outputRow = []

mainRoutine = 'A,B,A,C,B,C,A,B,A,C\n'
routineA    = 'R,6,L,10,R,8,R,8\n'
routineB    = 'R,12,L,8,L,10\n'
routineC    = 'R,12,L,10,R,6,L,10\n'
contOutput  = 'n\n'

while not term:
    (pc, outputVal, returnMode) = myProgram.runProgram(pc, nextInput, setNextInput)
    setNextInput=False

    if returnMode == 0:
        term = True
        continue

    elif returnMode == 1:
        if outputVal==10:
            print "".join(outputRow)
            outputRow=[]
        elif outputVal <= 127:
            outputRow.append(chr(outputVal))

        elif outputVal > 127:
            print "Found Drone, Dust={}".format(outputVal)
            totalDust += outputVal

    elif returnMode == 2:
        #for g in grid:
        #    print "".join(g)

        if   inputMode == 0: nextInput = ord(mainRoutine[inputPtr])
        elif inputMode == 1: nextInput = ord(routineA[inputPtr])
        elif inputMode == 2: nextInput = ord(routineB[inputPtr])
        elif inputMode == 3: nextInput = ord(routineC[inputPtr])
        elif inputMode == 4: nextInput = ord(contOutput[inputPtr])

        setNextInput = True
        if nextInput == 10:
            print
            inputMode+=1
            inputPtr=0
        else:
            print chr(nextInput),
            inputPtr+=1

    else:
        assert False, "invalid return value"


print "totalDust = {}".format(totalDust)
