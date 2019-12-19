#!/usr/bin/python

term = False
i=0
while not term:
    i+=1

    term = i > 4700000000

    if i%1000000==0:
        print "{:,}".format(i)
