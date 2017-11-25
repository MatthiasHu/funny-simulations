from pygame import *
from math import *

init()
screen = display.set_mode((1000, 1000))


width  = 8
height = 8
equi_dist = 20

pos = [[[100 + x*equi_dist, 100 + y*equi_dist + sin(x*0.2)*40]
        for x in range(width)] for y in range(height)]
vel = [[[0, 0] for x in range(width)] for y in range(height)]

strength = 0.01

gravity = 0.01

grabbed = None

def spring_force(a, b):
  r = [a[0]-b[0], a[1]-b[1]]
  r_norm = sqrt(r[0]*r[0] + r[1]*r[1])
  d = r_norm-equi_dist
  if r_norm>0.001:
    f = [r[0]/r_norm*d, r[1]/r_norm*d]
  else:
    f = [0, 0]
  return f

quit = False
while not quit:
  for e in event.get():
    if e.type==QUIT:
      quit = True
  
  strong_friction = False
  if key.get_pressed()[K_r]:
    strong_friction = True

  for y in range(height):
    for x in range(width):
      acc = [0, 0]
      for (dx, dy) in [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, 1], [1, -1]]:
        xx = x+dx
        yy = y+dy
        if xx>=0 and xx<width and yy>=0 and yy<height:
          f = spring_force(pos[yy][xx], pos[y][x])
          for i in range(2):
            acc[i] += f[i]*strength
      for i in range(2):
        vel[y][x][i] = (vel[y][x][i] + acc[i]) * (
          0.95 if strong_friction else 0.998 )
  for y in range(height):
    for x in range(width):
      for i in range(2):
        pos[y][x][i] = pos[y][x][i] + vel[y][x][i]

  for x in range(width):
    vel[0][x][1] -= gravity
    vel[height-1][x][1] += gravity

  mpos = mouse.get_pos()
  if mouse.get_pressed()[0]:
    if grabbed==None:
      nearest = None
      bestDistQ = float("inf")
      for y in range(height):
        for x in range(width):
          distQ = (mpos[0]-pos[y][x][0])**2 + (mpos[1]-pos[y][x][1])**2
          if distQ < bestDistQ:
            nearest = [x, y]
            bestDistQ = distQ
      grabbed = nearest
    pos[grabbed[1]][grabbed[0]] = [mpos[0], mpos[1]]
    vel[grabbed[1]][grabbed[0]] = [0, 0]
  else:
    grabbed = None
  
  screen.fill(Color(0, 0, 0))
  for y in range(height):
    for x in range(width):
      draw.circle(screen, Color(255, 255, 255),
        (int(pos[y][x][0]), int(pos[y][x][1])), 5)
  
  display.flip()
  if not key.get_pressed()[K_f]:
    time.wait(10)
