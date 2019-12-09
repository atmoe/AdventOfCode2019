#!/usr/bin/python

import sys
import math
import itertools
import copy

enableDebug = False

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

def runProgram(program, initPC, inputVal):
    outputVal = -1
    numInputsSeen = 0

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
            break

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
            program[params[dst_param]] = inputVal 
            if enableDebug: print "\tINPUT: {}".format(inputVal)
        elif op == 4:
            # Output
            outputVal = params[0]
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

        if op==4:
            print "OUTPUT: {}".format(outputVal)

        if enableDebug: print "=================================================================================================="


    return (outputVal, pc, True)

### Main Program

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputsStr = inputFile.readline().rstrip().split(",")
prog = [int(i) for i in inputsStr]
inputFile.close()


print "-----------------"
print "---- Part 1------"
print "-----------------"

runProgram(prog, 0, 1)

print "-----------------"
print "---- Part 2------"
print "-----------------"
runProgram(prog, 0, 2)
