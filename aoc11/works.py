class P:
  def __init__( z, program, init_input, init_ip=0 ):
    z.p = program.copy()
    z.i = init_input
    z.o = None # output
    z.j = init_ip # ip
    z.b = 0 # base for mode 2 addressing
    z.s = 'S' # suspended; other states: 'H' halt, 'O' output, 'W' waiting input

  def address( z, addr, mode ): # get address for 3rd operand
    if mode==1:   return addr
    elif mode==2: return z.b + z.p.get(addr,0)
    else:         return z.p.get(addr,0)

  def run( z ):
    while z.p.get(z.j,0)%100 != 99: # run till halt
      ip = z.j; oop = z.p.get(ip,0); op = oop%100  # original and effective opcode
      z.j += (0,4,4,2,2,3,3,4,4,2)[op]
      if op in (1,2,  4,5,6,7,8,9): v = z.p.get(z.address(ip+1,(oop//100)%10),0)
      if op in (1,2,    5,6,7,8):   w = z.p.get(z.address(ip+2,(oop//1000)%10),0)
      if op in (1,2,        7,8):        dest = z.address(ip+3,(oop//10000)%10)
      if   op==1: z.p[dest] = v + w # add
      elif op==2: z.p[dest] = v * w # mul
      elif op==7: z.p[dest] = int(v <  w) # setl
      elif op==8: z.p[dest] = int(v == w) # sete
      elif op==9: z.b += v # rebase
      elif op==4: z.o = v; z.s = 'O'; return v # O: yielded output
      elif op==3: # in
        if len(z.i)==0: z.j -= 2; z.s = 'W'; return # W: waiting input
        z.p[z.address(ip+1,(oop//100)%10)] = z.i.pop(0)
      elif op==5: # jmpt
        if v != 0: z.j = w
      elif op==6: # jmpf
        if v == 0: z.j = w
      else: raise Exception("wrong opcode %d, %d at %d"%(op,oop,ip))
    z.s = 'H' # H: halt instruction

def solve( pgm, part ):
  panels = {}
  if part==2: panels[(0,0)] = 1 # WHITE
  coords = (0,0) # row, col, rows go down 0, 1, 2, ...
  dir = 0 # 0 up 1 right 2 down 3 left
  painted = set()
  p = P(pgm,[])
  output_color = True # output trigger: once color, once turn
  while p.s != 'H': # whilst from J would be better here
    p.run()
    if p.s=='W':
      p.i.append( panels.get( coords, 0 ) ) # input color (default: black)
    elif p.s=='O':
      if output_color:
        panels[ coords ] = p.o # new color
        painted.add( coords )
      else:
        dir = (dir + 3 - 2*p.o) % 4 # p.o: 0 - turn left, 1 - turn right
        coords = (coords[0]+(-1,0,+1,0)[dir],coords[1]+(0,+1,0,-1)[dir])
      output_color = not output_color
    elif p.s!='H':
      raise Exception( "state {} at {}".format(p.s,coords) )
  if part==1:
    return len(painted)
  else:
    return panels

#with open("11.dat","rt") as f:
with __import__("sys").stdin as f: # for tio.run
  pgm = {a:int(x) for a,x in enumerate(f.read().strip().split(','))}

print( solve( pgm, 1 ) ) # 2469

image= solve( pgm, 2 )
for r in range(6):
  print("".join(".\u2588"[image.get( (r,c), 0 )] for c in range(40)))

