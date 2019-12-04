#!/usr/bin/python

import sys
import math

numPasswordsPart1 = 0
numPasswordsPart2 = 0

for num in range(234208, 765869+1):
    digits = []
    numTmp = num
    for i in range(6):
        digits.append(numTmp % 10)
        numTmp /= 10

    increments = True
    for i in range(5):
        if digits[i] < digits[i+1]:
            increments = False

    hasDouble = False
    for i in range(5):
        if digits[i] == digits[i+1]:
            hasDouble = True

    hasDouble = False
    hasStrictDouble = False
    for i in range(5):
        if digits[i] == digits[i+1]:
            hasDouble = True

            hasStrictDouble = True
            if i != 0 and digits[i-1] == digits[i]:
                hasStrictDouble = False
            if i != 4 and digits[i+2] == digits[i]:
                hasStrictDouble = False
                
            if hasStrictDouble:
                break


    if hasDouble and increments:
        numPasswordsPart1 += 1

    if hasStrictDouble and increments:
        numPasswordsPart2 += 1
        print num

    if hasDouble and not hasStrictDouble and increments:
        print "{} <<<<<".format(num)


print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "numPasswords = {}".format(numPasswordsPart1)

print "----------------------"
print "---- Part 2 ----------"
print "----------------------"
print "numPasswords = {}".format(numPasswordsPart2)
