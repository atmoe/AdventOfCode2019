#!/usr/bin/python
import copy

class Intcode:
    def __init__(self, program, inputs):
        self.pc        = 0
        self.iptr      = 0
        self.program   = copy.deepcopy(program)
        self.inputs    = copy.deepcopy(inputs)
        self.outputs   = []
        self.terminated = False

    # op 1
    def add(self, s0, s1, d):
        self.program[d] = s0 + s1
        self.pc += 4

    # op 2
    def mul(self, s0, s1, d):
        self.program[d] = s0 * s1
        self.pc += 4

    # op 3
    def inp(self, d):
        self.program[d] = self.inputs[self.iptr]
        self.pc += 2
        self.iptr += 1

    # op 4
    def out(self, x):
        self.outputs.append(x)
        self.pc += 2

    # op 5
    def jit(self, check, newPC):
        if check != 0:
            self.pc = newPC
        else:
            self.pc += 3

    # op 6
    def jif(self, check, newPC):
        if check == 0:
            self.pc = newPC
        else:
            self.pc += 3

    # op 7
    def lt(self, a, b, d):
        if a < b:
            self.program[d] = 1
        else:
            self.program[d] = 0

        self.pc += 4

    # op 8
    def eq(self, a, b, d):
        if a == b:
            self.program[d] = 1
        else:
            self.program[d] = 0

        self.pc += 4

    def halt(self):
        self.terminated = True
        self.pc+=1

    def getWrParam(self, op):
        if   op == 1: return  2
        if   op == 2: return  2
        elif op == 3: return  0
        elif op == 4: return -1
        elif op == 5: return -1
        elif op == 6: return -1
        elif op == 7: return  2
        elif op == 8: return  2
        else:         return -1

    def getNumParams(self, op):
        if   op == 1: return 3
        elif op == 2: return 3
        elif op == 3: return 1
        elif op == 4: return 1
        elif op == 5: return 2
        elif op == 6: return 2
        elif op == 7: return 3
        elif op == 8: return 3
        else:         return -1

    def step(self):
        pc  = self.pc
        prg = self.program
        op  = prg[pc] % 100

        # Operand Mode
        mode = [0,0,0]
        mode[0] = int(prg[pc] / 100)   % 10
        mode[1] = int(prg[pc] / 1000)  % 10
        mode[2] = int(prg[pc] / 10000) % 10
        assert (op != 1 and op != 2) or mode[2] == 0, 'invalid add/mul destination mode'
        assert (op != 3            ) or mode[0] == 0, 'invalid inp destination mode'

        # Operand Resolution
        params = [0,0,0]
        numParams = self.getNumParams(op)
        wrParam   = self.getWrParam(op) # destination is always passed to op as an index
        for i in range(numParams):
            if i == wrParam:   params[i] = prg[pc+i+1]
            elif mode[i] == 0: params[i] = prg[prg[pc+i+1]]
            elif mode[i] == 1: params[i] = prg[pc+i+1]

        if   op == 1:  self.add(params[0], params[1], params[2])
        elif op == 2:  self.mul(params[0], params[1], params[2])
        elif op == 3:  self.inp(params[0])
        elif op == 4:  self.out(params[0])
        elif op == 5:  self.jit(params[0], params[1])
        elif op == 6:  self.jif(params[0], params[1])
        elif op == 7:  self.lt(params[0], params[1], params[2])
        elif op == 8:  self.eq(params[0], params[1], params[2])
        elif op == 99: self.halt()


    def exec(self):
        while not self.terminated:
            self.step()

        
