from pygame import *
from math import *
import random

init()
screen = display.set_mode((800, 800))


class Particle:
  def __init__(self, pos, vel=None, mass=10):
    self.pos = pos
    self.vel = [0, 0] if vel is None else vel
    self.mass = mass
    self.delete = False

  def move(self):
    for i in [0, 1]:
      self.pos[i] += self.vel[i]*dt

  def receive_force(self, f):
    for i in [0, 1]:
      self.vel[i] += f[i]/self.mass*dt

  def gravitate_towards(self, other):
    r = [other.pos[i]-self.pos[i] for i in [0, 1]]
    r_norm = sqrt(sum([c**2 for c in r]))
    if r_norm > 0.000001:
      self.receive_force([r[i]*self.mass*other.mass/(r_norm**3)
                          for i in [0, 1]])

  def radius(self):
    return pow(self.mass, 1/3)

  def check_collision_with(self, other):
    if self.delete:
      return
    r = [other.pos[i]-self.pos[i] for i in [0, 1]]
    r_norm = sqrt(sum([c**2 for c in r]))
    if r_norm < self.radius() + other.radius():
      self.merge_into(other)

  def merge_into(self, other):
    mass = self.mass + other.mass
    other.pos = [(other.pos[i]*other.mass+self.pos[i]*self.mass)/mass
                 for i in [0, 1]]
    other.vel = [(other.vel[i]*other.mass+self.vel[i]*self.mass)/mass
                 for i in [0, 1]]
    other.mass = mass
    self.delete = True


#parts = ([ Particle([200, 300+i*40], mass=20, vel=[0, 0.5])
#          for i in range(5) ]
#         + [Particle([300, 300], mass=200)])

def random_particle():
  mean_mass = 2
  sigma_v = 0.5
  sigma_pos = 180
  rotation = 0

  mass = random.expovariate(1/mean_mass)
  pos = [random.gauss(0, sigma_pos) for i in [0, 1]]
  pos_norm = sqrt(sum([c**2 for c in pos]))
  vel = [random.gauss(0, sigma_v) for i in [0, 1]]
  vel[0] += pos[1]*rotation
  vel[1] -= pos[0]*rotation
  return Particle([400+c for c in pos], vel=vel, mass=mass)

parts = [random_particle() for _ in range(150)]

dt = 1


def handle_keydown(key):
  if key==K_LEFT:
    for p in parts:
      p.pos[0]+=100
  if key==K_RIGHT:
    for p in parts:
      p.pos[0]-=100
  if key==K_UP:
    for p in parts:
      p.pos[1]+=100
  if key==K_DOWN:
    for p in parts:
      p.pos[1]-=100

quit = False
while not quit:
  for e in event.get():
    if e.type == QUIT:
      quit = True
    if e.type == KEYDOWN:
      handle_keydown(e.key)

  for (i, p) in enumerate(parts):
    for q in parts[i+1:]:
      p.check_collision_with(q)
  parts = [p for p in parts if not p.delete]
  for p in parts:
    for q in parts:
      p.gravitate_towards(q)
  for p in parts:
    p.move()

  screen.fill(Color(0, 0, 0))
  for p in parts:
    draw.circle(screen, Color("white"),
      [int(c) for c in p.pos], int(p.radius()))

  display.flip()
  if not key.get_pressed()[K_f]:
    time.wait(20)
