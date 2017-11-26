from pygame import *
from math import *

init()
screen = display.set_mode((1000, 1000))


class Particle:
  def __init__(self, pos, vel=[0, 0], mass=1,
               friction=0.998, gravity=0.01, pinned=False):
    self.pos =  pos
    self.vel = vel
    self.mass = mass
    self.friction = friction
    self.gravity = gravity
    self.pinned = pinned

  def move(self):
    if self.pinned: return
    for i in range(2):
      self.pos[i] += self.vel[i]

  def receive_force(self, f):
    for i in range(2):
      self.vel[i] += f[i]/self.mass

  def apply_friction(self, friction=None):
    if friction == None:
      friction = self.friction
    self.vel = [self.vel[i]*friction for i in [0, 1]]

  def apply_gravity(self, gravity=None):
    if gravity == None:
      gravity = self.gravity
    self.receive_force([0, gravity*self.mass])

class Spring:
  def __init__(self, ends, rate=0.01, equi_length=0):
    self.ends = [ends[0], ends[1]]
    self.rate = rate
    self.equi_length = equi_length

  def apply_force_to_ends(self):
    a = self.ends[0].pos
    b = self.ends[1].pos
    d = spring_deflection(a, b, self.equi_length)
    f = [d[i]*self.rate for i in [0, 1]]
    self.ends[0].receive_force([-f[i] for i in [0, 1]])
    self.ends[1].receive_force(f)

def spring_deflection(a, b, equi_length):
  r = [a[0]-b[0], a[1]-b[1]]
  r_norm = sqrt(r[0]*r[0] + r[1]*r[1])
  d_norm = r_norm-equi_length
  if r_norm>0.001:
    d = [r[0]/r_norm*d_norm, r[1]/r_norm*d_norm]
  else:
    d = [0, 0]
  return d


def string_of_springs():
  length = 30
  ps = [Particle([100+20*i, 100], mass=0.2) for i in range(length+1)]
  ps[0].pinned = True
  ps[-1].pinned = True
  ss = [Spring([ps[i], ps[i+1]], equi_length=10) for i in range(length)]
  return (ps, ss)

def squares_tower():
  height = 8
  width = 2
  l = 40
  ps = [[Particle([200+x*l, 500-y*l], mass=0.2) for x in range(width+1)]
        for y in range(height+1)]
  for p in ps[0]:
    p.pinned = True
  for p in ps[-1]:
    p.vel[0] = 0.1
  ss = []
  ss += [Spring([ps[y][x], ps[y][x+1]], equi_length=l)
         for y in range(height+1) for x in range(width)]
  ss += [Spring([ps[y][x], ps[y+1][x]], equi_length=l)
         for y in range(height) for x in range(width+1)]
  ss += [Spring([ps[y][x], ps[y+1][x+1]], equi_length=l*sqrt(2))
         for y in range(height) for x in range(width)]
  ss += [Spring([ps[y][x+1], ps[y+1][x]], equi_length=l*sqrt(2))
         for y in range(height) for x in range(width)]
  ps = [p for ps1 in ps for p in ps1]
  return (ps, ss)

(particles, springs) = squares_tower()


grabbed = None

quit = False
while not quit:
  for e in event.get():
    if e.type==QUIT:
      quit = True
  
  for s in springs:
    s.apply_force_to_ends()
  for p in particles:
    p.apply_gravity()
    p.apply_friction()
    if key.get_pressed()[K_r]:
      p.apply_friction(0.95)
    p.move()

  mpos = mouse.get_pos()
  if mouse.get_pressed()[0]:
    if grabbed==None:
      nearest = None
      bestDistQ = float("inf")
      for p in particles:
        distQ = (mpos[0]-p.pos[0])**2 + (mpos[1]-p.pos[1])**2
        if distQ < bestDistQ:
          nearest = p
          bestDistQ = distQ
      grabbed = nearest
    grabbed.pos = [mpos[0], mpos[1]]
    grabbed.vel = [0, 0]
  else:
    grabbed = None
  
  screen.fill(Color(0, 0, 0))
  for p in particles:
    draw.circle(screen, Color(255, 255, 255),
      (int(p.pos[0]), int(p.pos[1])), 5)
  for s in springs:
    vertices = [[int(s.ends[i].pos[j]) for j in [0, 1]] for i in [0, 1]]
    draw.line(screen, Color(255, 255, 255),
      vertices[0], vertices[1])
  
  display.flip()
  if not key.get_pressed()[K_f]:
    time.wait(10)
