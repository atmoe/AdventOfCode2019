#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")

inputsStr = inputFile.readline().rstrip().split(",")
inputsPart1 = [int(i) for i in inputsStr]

inputFile.close()


### Part 1 ###
print inputsPart1

inputsPart1[1] = 12
inputsPart1[2] = 2

pc = 0
terminated = False
while pc < len(inputsPart1) and not terminated:
    op  = inputsPart1[pc]


    if op == 99:
        terminated = True
    else:
        op1 = inputsPart1[pc+1]
        op2 = inputsPart1[pc+2]
        dst = inputsPart1[pc+3]
        print "op = {}  op1 = {}  op2 = {}  dst = {}".format(op, op1, op2, dst)

        if op == 1:
            inputsPart1[dst] = inputsPart1[op1] + inputsPart1[op2]
        elif op == 2:
            inputsPart1[dst] = inputsPart1[op1] * inputsPart1[op2]
        else:
            assert "invalid opcode: {}".format(op)


    pc+=4

print inputsPart1

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "Value0 = {}".format(inputsPart1[0])

### Part 2 ###
comboFound = False

for noun in range(100):
    for verb in range(100):
        print "At {}, {}".format(noun, verb)

        inputsPart2 = [int(i) for i in inputsStr]
        inputsPart2[1] = noun
        inputsPart2[2] = verb

        pc = 0
        terminated = False
        while pc < len(inputsPart2) and not terminated:
            op  = inputsPart2[pc]

            if op == 99:
                terminated = True
            else:
                op1 = inputsPart2[pc+1]
                op2 = inputsPart2[pc+2]
                dst = inputsPart2[pc+3]

                if op == 1:
                    inputsPart2[dst] = inputsPart2[op1] + inputsPart2[op2]
                elif op == 2:
                    inputsPart2[dst] = inputsPart2[op1] * inputsPart2[op2]
                else:
                    assert "invalid opcode: {}".format(op)


                pc+=4

        if inputsPart2[0] == 19690720:
            comboFound = True
            break

    if comboFound:
        break


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
print "Combo = {}".format(noun*100 + verb)
print "ComboFound = {}".format(comboFound)
