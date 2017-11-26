from pygame import *
from math import *

init()
screen = display.set_mode((500, 500))


class Ball:
  def __init__(self, pos, vel=[0, 0], radius=30,
               color=Color(255, 0, 0), mass=1):
    self.pos = pos
    self.vel = vel
    self.radius = radius
    self.color = color
    self.mass = mass

  def move(self):
    for i in [0, 1]:
      self.pos[i] += self.vel[i]*dt

  def apply_gravity(self):
    self.vel[1] += gravity*dt

  def bump_from_wall(self, i, c, s):
    c -= s*self.radius
    if s*self.pos[i]>s*c:
      self.vel[i] *= (-1)
      self.pos[i] -= 2*(self.pos[i]-c)

  def predict_position(self, t):
    x = self.pos[0] + t*self.vel[0]
    y = self.pos[1] + t*self.vel[1] + 0.5*(t**2)*gravity
    return [x, y]

# calculate time of next collision,
# return None if no collision is found
def find_collision(b1, b2):
  p = [b1.pos[i]-b2.pos[i] for i in [0, 1]]
  v = [b1.vel[i]-b2.vel[i] for i in [0, 1]]
  r = b1.radius + b2.radius
  a = v[0]**2 + v[1]**2
  b = 2*(p[0]*v[0] + p[1]*v[1])
  c = p[0]**2 + p[1]**2 - r**2
  ts = solve_quadratic_equation(a, b, c)
  ts = [t for t in ts if t>0]
  if len(ts)>0:
    return min(ts)
  else:
    return None

# return list of solutions of a*x**2 + b*x + c = 0
def solve_quadratic_equation(a, b, c):
  d = b**2 - 4*a*c
  if d<0:
    return []
  elif d==0:
    return [-b/(2*a)]
  else:
    sd = sqrt(d)
    return [(-b+sd)/(2*a), (-b-sd)/(2*a)]

# (imprecise) collisions of balls
def handle_collision(b1, b2):
  bs = [b1, b2]
  d = [b2.pos[i]-b1.pos[i] for i in [0,1]]
  d_norm = sqrt(sum([c**2 for c in d]))
  if d_norm > b1.radius+b2.radius or d_norm < 0.001:
    return
  # normalized difference vector
  dn = [c/d_norm for c in d]
  # flip velocities outwards
  mass = sum([b.mass for b in bs])
  vel = [sum([b.vel[i]*b.mass for b in bs])/mass for i in [0, 1]]
  for b in [b1, b2]:
    s = sum([(b.vel[i]-vel[i])*dn[i] for i in [0, 1]])
    for i in [0, 1]:
      b.vel[i] -= 2*s*dn[i]
  # flip positions outward (preserving center of mass)
  overlap = b1.radius+b2.radius - d_norm
  for (b, sign) in [(b1, -1), (b2, 1)]:
    for i in [0, 1]:
      b.pos[i] += sign*dn[i]*overlap*b.mass/mass


balls = [ Ball([100, 200], vel=[5, 5], mass=4, radius=60)
        , Ball([100, 50], vel=[2.5, 0], color=Color(0, 255, 255))]
gravity = 0.2

dt = 1

quit = False
while not quit:
  for e in event.get():
    if e.type == QUIT:
      quit = True

  for b in balls:
    b.apply_gravity()
    b.move()
    b.bump_from_wall(1, 500, 1)
    b.bump_from_wall(1, 0, -1)
    b.bump_from_wall(0, 500, 1)
    b.bump_from_wall(0, 0, -1)
  handle_collision(balls[0], balls[1])

  screen.fill(Color(0, 0, 0))
  for b in balls:
    draw.circle(screen, b.color, [int(c) for c in b.pos], b.radius)
  collision = find_collision(balls[0], balls[1])
  if not collision==None:
    t = collision
    for b in balls[:2]:
      p = b.predict_position(t)
      draw.circle(screen, b.color, [int(c) for c in p], b.radius, 1)


  display.flip()
  if not key.get_pressed()[K_f]:
    time.wait(20)
