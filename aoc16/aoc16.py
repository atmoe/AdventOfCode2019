#!/usr/bin/python

import sys
import math

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"


inputFile = open(sys.argv[1], "r")
signalStr = list(inputFile.readline().rstrip())
signal =  [int(i) for i in signalStr]
inputFile.close()

basePattern = [0, 1, 0, -1]
signalLen = len(signal)

print signal
print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
for phase in range(100):
    print phase
    newSignal = [0] * signalLen
    for i in range(signalLen):
        pattern = []
        for j in range(signalLen):
            pattern.append(basePattern[j/(i+1) % 4])

        pattern = pattern[1:] + [ basePattern[signalLen/(i+1)%4] ]
        #print "pattern = {}".format(pattern)

        for j in range(signalLen):
            newSignal[i] += signal[j] * pattern[j]

        newSignal[i] = abs(newSignal[i])%10

    signal = newSignal

message = signal[0:8]

messageStr =  [str(i) for i in message]
print "Message = {}".format("".join(messageStr))


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"

signal =  [int(i) for i in signalStr] * 10000
signalLen = len(signal)
messageOffset = int(''.join([str(i) for i in signal[0:7]]))
print messageOffset
print signalLen
print messageOffset/float(signalLen)

for phase in range(100):
    newSignal = [0] * signalLen
    print phase
    newSignal[-1] = signal[-1]
    for i in reversed(range(messageOffset, signalLen-1)):
        newSignal[i] = newSignal[i+1] + signal[i]

    for i in range(messageOffset, signalLen):
        newSignal[i] = abs(newSignal[i])%10

    signal = newSignal

message = signal[messageOffset:messageOffset+8]

messageStr =  [str(i) for i in message]
print "Message = {}".format("".join(messageStr))

