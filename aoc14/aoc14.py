#!/usr/bin/python

import sys
import math

def oreNeeded(fuelAmt):
    oreCnt = 0
    chemicalsToResolve = {}
    chemicalsToResolve['FUEL'] = fuelAmt
    extraChemicals = {}
    while chemicalsToResolve:
        # remove extra
        for e in extraChemicals.keys():
            if e in chemicalsToResolve:
                if extraChemicals[e] > chemicalsToResolve[e]:
                    extraChemicals[e] -= chemicalsToResolve[e]
                    chemicalsToResolve.pop(e)
                else:
                    chemicalsToResolve[e] -= extraChemicals[e]
                    extraChemicals.pop(e)

        chemical = chemicalsToResolve.keys()[-1]
        amount   = chemicalsToResolve[chemical]

        for r in reactions:
            result = r[0][0]
            if result == chemical:
                amtGenerated = r[0][1]

                reactionsNeeded = int(math.ceil(amount/float(amtGenerated)))

                for i in r[1]:
                    inputChem = i[0]
                    inputAmt  = i[1]

                    if inputChem == 'ORE':
                        oreCnt += inputAmt*reactionsNeeded
                    else:
                        if not inputChem in chemicalsToResolve:
                            chemicalsToResolve[inputChem] = inputAmt * reactionsNeeded
                        else:
                            chemicalsToResolve[inputChem] += inputAmt * reactionsNeeded

                # Do you ever need to track generating more than amount?
                if amtGenerated*reactionsNeeded - amount > 0:
                    extraChemicals[chemical] = amtGenerated*reactionsNeeded - amount

                chemicalsToResolve.pop(chemical)

                continue

    return oreCnt


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

reactions = []
for line in inputFile.readlines():
    print line.rstrip()
    r = line.rstrip().split(" => ")
    result = (r[1].split()[1], int(r[1].split()[0]))
    inputs = r[0].split(", ")
    reaction = (result, [])
    for inp in inputs:
        reaction[1].append((inp.split()[1], int(inp.split()[0])))

    reactions.append(reaction)

inputFile.close()

print "----------------------"
print "---- Part 1 ----------"
print "----------------------"
print "Ore Needed = {}".format(oreNeeded(1))


print "----------------------"
print "---- Part 2 ----------"
print "----------------------"

currentMaxFuel=1 # max fuel that uses less than 1T ore
currentMaxOre =oreNeeded(1)
increment=1

terminated = False
while not terminated:
#for i in range(300):
    #print "ore {} => fuel {}".format(oreNeeded(currentMaxFuel), currentMaxFuel)
    if oreNeeded(currentMaxFuel+increment) <= 1000000000000:
        currentMaxFuel+=increment
        increment*=2
    else:
        increment=1

    terminated = (oreNeeded(currentMaxFuel) <= 1000000000000) and (oreNeeded(currentMaxFuel+1) > 1000000000000)

print "Max Fuel Produced = {}".format(currentMaxFuel)



