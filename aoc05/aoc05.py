#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputsStr = inputFile.readline().rstrip().split(",")
inputs = [int(i) for i in inputsStr]

inputFile.close()


### Part 1 ###
print inputs

manualInput = 1

pc = 0
terminated = False
while pc < len(inputs) and not terminated:
    opRaw  = inputs[pc]

    op     = opRaw % 100
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
            params.append(inputs[pc+i])
        if pmode[i] == 0:
            params.append(inputs[inputs[pc+i]])
        else:
            assert "invalid pmode"


    #print "pmodes = {}".format(pmode)
    #print "params = {}".format(params)
    jumpPtr = -1
    if op == 1:
        #print "ADD[{},{},{},{}]:".format(opRaw, inputs[pc], inputs[pc+1], inputs[pc+2])
        #print "    {} = {} + {}".format(params[dst_param], params[0], params[1])
        inputs[params[dst_param]] = params[0] + params[1]
    elif op == 2:
        #print "MUL[{},{},{},{}]:".format(opRaw, inputs[pc], inputs[pc+1], inputs[pc+2])
        #print "    {} = {} * {}".format(params[dst_param], params[0], params[1])
        inputs[params[dst_param]] = params[0] * params[1]
    elif op == 3:
        manualInput = int(input("INPUT: "))
        print "INPUT[{},{}]: {} <= {}".format(op, inputs[pc], params[dst_param], manualInput)
        inputs[params[dst_param]] = manualInput
    elif op == 4:
        print "OUTPUT[{},{}]:         ".format(op, inputs[pc])
        print "               => {}".format(params[0])
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
            inputs[params[dst_param]] = 1
        else:
            inputs[params[dst_param]] = 0
    elif op == 8:
        if params[0] == params[1]:
            inputs[params[dst_param]] = 1
        else:
            inputs[params[dst_param]] = 0
    else:
        assert "invalid opcode: {}".format(op)

    if opIsJump:
        pc = jumpPtr
    else:
        pc += num_params


