import pygame
from pygame.locals import *
from math import *

pygame.init()
screen = pygame.display.set_mode((1000, 1000))


bx = 50
by = 50
bvx = 0
bvy = 0

ax = 50
ay = 50
avx = 0
avy = 0

# strngth of springs
pull_m_b = 0.001
pull_b_a = 0.001
# masses of b and a
bm = 2
am = 1

quit = False
while not quit:
  for e in pygame.event.get():
    if e.type==QUIT:
      quit = True
  
  (mx, my) = pygame.mouse.get_pos()
  bvx += (mx-bx)/bm*pull_m_b
  bvy += (my-by)/bm*pull_m_b
  bvx += (ax-bx)/bm*pull_b_a
  bvy += (ay-by)/bm*pull_b_a
  bx += bvx
  by += bvy

  avx += (bx-ax)/am*pull_b_a
  avy += (by-ay)/am*pull_b_a
  ax += avx
  ay += avy
  if pygame.key.get_pressed()[K_r]:
    bvx *= 0.99
    bvy *= 0.99
    avx *= 0.99
    avy *= 0.99

  if not pygame.key.get_pressed()[K_SPACE]:
    screen.fill(Color(0, 0, 0))
  pygame.draw.circle(screen, Color(255, 0, 0), (int(bx), int(by)), 10)
  pygame.draw.circle(screen, Color(0, 0, 255), (int(ax), int(ay)), 10)
  pygame.draw.circle(screen, Color(0, 255, 0), (mx, my), 10)
  
  pygame.display.flip()
  if not pygame.key.get_pressed()[K_f]:
    pygame.time.wait(10)
