#!/usr/bin/python

import sys
import math
import itertools
import copy

def runProgram(program, initPC, phase, signal, returnOnOutput, phaseSet):
    print "pc = {}, signal = {}".format(initPC, signal)
    outputVal = -1
    numInputsSeen = 0

    pc = initPC
    terminated = False
    while pc < len(program) and not terminated:
        opRaw  = program[pc]

        op    = opRaw % 100
        pmode = [(opRaw / 100) % 10, (opRaw / 1000) % 10, (opRaw / 10000) % 10]

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
        else:
            assert "invalid op"

        # increment to params
        pc += 1

        params = []
        for i in range(num_params):
            if i == dst_param or pmode[i] == 1:
                params.append(program[pc+i])
            if pmode[i] == 0:
                params.append(program[program[pc+i]])
            else:
                assert "invalid pmode"

        jumpPtr = -1
        if op == 1:
            program[params[dst_param]] = params[0] + params[1]
        elif op == 2:
            program[params[dst_param]] = params[0] * params[1]
        elif op == 3:
            numInputsSeen+=1
            if numInputsSeen == 1 and not phaseSet:
                program[params[dst_param]] = phase
            else:
                program[params[dst_param]] = signal

            #print "INPUT[{},{}]: {} <= {}".format(op, program[pc], params[dst_param], program[params[dst_param]])
        elif op == 4:
            outputVal = params[0]

        elif op == 5:
            if params[0] != 0:
                jumpPtr = params[1]
            else:
                jumpPtr = pc + num_params
        elif op == 6:
            if params[0] == 0:
                jumpPtr = params[1]
            else:
                jumpPtr = pc + num_params
        elif op == 7:
            if params[0] < params[1]:
                program[params[dst_param]] = 1
            else:
                program[params[dst_param]] = 0
        elif op == 8:
            if params[0] == params[1]:
                program[params[dst_param]] = 1
            else:
                program[params[dst_param]] = 0
        else:
            assert "invalid opcode: {}".format(op)

        if opIsJump:
            pc = jumpPtr
        else:
            pc += num_params

        if returnOnOutput and op==4:
            return (outputVal, pc, False)

    return (outputVal, pc, True)

### Main Program

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputsStr = inputFile.readline().rstrip().split(",")
prog = [int(i) for i in inputsStr]

inputFile.close()


### Part 1 ###
maxOutput = 0
for permutation in list(itertools.permutations([0,1,2,3,4])):
    lastOut = (0, 0)
    for phase in permutation:
        thisProg = copy.deepcopy(prog)
        lastOut = runProgram(thisProg, 0, phase, lastOut[0], False, False)

    if lastOut[0] > maxOutput:
        maxOutput = lastOut[0]

print "-----------------"
print "---- Part 1------"
print "-----------------"
print "Max = {}".format(maxOutput)




### Part 2 ###

maxOutput = 0
for permutation in list(itertools.permutations([5,6,7,8,9])):

    ampProgs = []
    ampPC    = []
    ampTerm  = []
    for i in range(5):
        ampProgs.append( copy.deepcopy(prog) )
        ampPC.append(0)
        ampTerm.append(False)

    lastOut = (0, 0, False)
    phaseHasBeenSet = False
    lastNonTermOutput = 0
    while not ampTerm[4]:
        for i in range(5):
            lastOut = runProgram(ampProgs[i], ampPC[i], permutation[i], lastOut[0], True, phaseHasBeenSet)
            ampPC[i] = lastOut[1]
            ampTerm[i] = lastOut[2]
            if not ampTerm[i]:
                lastNonTermOutput = lastOut[0]
            print "{} = {}".format(i, lastOut)

        phaseHasBeenSet = True

    if lastNonTermOutput > maxOutput:
        maxOutput = lastNonTermOutput

print "-----------------"
print "---- Part 2------"
print "-----------------"
print "Max = {}".format(maxOutput)
