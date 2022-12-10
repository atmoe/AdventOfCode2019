#!/usr/bin/python
import copy

class Intcode:
    def __init__(self, program, inputs):
        self.pc       = 0
        self.program  = copy.deepcopy(program)
        self.inputs   = copy.deepcopy(inputs)
        self.halt     = False

    def add(self, s0, s1, d):
        self.program[d] = self.program[s0] + self.program[s1]

    def mul(self, s0, s1, d):
        self.program[d] = self.program[s0] * self.program[s1]

    def step(self):
        pc  = self.pc
        prg = self.program
        inst = prg[pc]

        if inst == 1: 
            self.add(prg[pc+1], prg[pc+2], prg[pc+3])
            self.pc+=4

        elif inst == 2: 
            self.mul(prg[pc+1], prg[pc+2], prg[pc+3])
            self.pc+=4

        elif inst == 99: 
            self.halt = True
            self.pc+=1

    def exec(self):
        while not self.halt:
            self.step()

        
