from pygame import *
from math import *

init()
screen = display.set_mode((800, 800))


class Particle:
  def __init__(self, pos, vel=None, mass=10):
    self.pos = pos
    self.vel = [0, 0] if vel is None else vel
    self.mass = mass

  def move(self):
    print("vel: "+str(self.vel))
    for i in [0, 1]:
      self.pos[i] += self.vel[i]*dt

  def receive_force(self, f):
    print("force: "+str(f))
    for i in [0, 1]:
      self.vel[i] += f[i]*dt

  def gravitate_towards(self, other):
    r = [other.pos[i]-self.pos[i] for i in [0, 1]]
    r_norm = sqrt(sum([c**2 for c in r]))
    if r_norm > 0.000001:
      self.receive_force([r[i]*other.mass/(r_norm**3) for i in [0, 1]])

parts = [Particle([200, 300], mass=1, vel=[0, 0.5]),
         Particle([300, 300], mass=100)]

dt = 1

quit = False
while not quit:
  for e in event.get():
    if e.type == QUIT:
      quit = True

  for p in parts:
    for q in parts:
      p.gravitate_towards(q)
  for p in parts:
    p.move()

  screen.fill(Color(0, 0, 0))
  for p in parts:
    draw.circle(screen, Color("white"),
      [int(c) for c in p.pos], int(sqrt(p.mass)))

  display.flip()
  if not key.get_pressed()[K_f]:
    time.wait(10)
