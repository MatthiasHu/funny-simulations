from pygame import *
from math import *

init()
screen = display.set_mode((1000, 1000))


width = 40
height = 20

pos = [[[100+x*20, 100+y*20+sin(x*0.2)*40]
        for x in range(width)] for y in range(height)]
vel = [[[0, 0] for x in range(width)] for y in range(height)]

strength = 0.01

for y in range(1, height-1):
  vel[y][1] = [2, 2]

grabbed = None

quit = False
while not quit:
  for e in event.get():
    if e.type==QUIT:
      quit = True
  
  strong_friction = False
  if key.get_pressed()[K_r]:
    strong_friction = True

  for y in range(1, height-1):
    for x in range(1, width-1):
      for i in range(2):
        acc = 0
        for (dx, dy) in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
          acc += (pos[y+dy][x+dx][i]-pos[y][x][i])*strength
        vel[y][x][i] = (vel[y][x][i] + acc) * (
          0.95 if strong_friction else 0.999 )
  for y in range(1, height-1):
    for x in range(1, width-1):
      for i in range(2):
        pos[y][x][i] = pos[y][x][i] + vel[y][x][i]

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
