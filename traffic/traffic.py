from pygame import *
import random


init()
screen = display.set_mode((1200, 600))

def target_velocity(distance):
  return (distance-10)*0.02

site_start = 600
site_end = 750

sleepiness = 100

cars = []
next_car = 0

dt = 1

quit = False

while not quit:
  for e in event.get():
    if e.type == QUIT:
      quit = True

  # spawn new car?
  next_car -= dt
  if next_car <= 0:
    next_car += random.randint(40, 120)
    cars.append({'x':0, 'v':2, 'tv':2, 'dist':1000, 'next_alert':0})

  # calculate distances to preciding car (for all but first car)
  for i in range(1, len(cars)):
    cars[i]['dist'] = cars[i-1]['x'] - cars[i]['x']

  for c in cars:
    # is driver alert?
    if c['dist'] > 25:
      c['next_alert'] -= dt
    else:
      c['next_alert'] = 0
    if c['next_alert'] <= 0:
      c['alert'] = True
      c['next_alert'] += random.randint(1, sleepiness)

      # update target velocity
      c['tv'] = target_velocity(c['dist'])
      c['tv'] = max(0, c['tv'])

      # respect allowed velocity
      c['tv'] = min(c['tv'], 2)
      if c['x'] >= site_start and c['x'] <= site_end:
        c['tv'] = min(c['tv'], 0.5)
    else:
      c['alert'] = False

  for c in cars:
    # accelerate or brake
    if c['v'] < c['tv']:
      c['v'] += 0.01
    if c['v'] > c['tv']:
      c['v'] -= 0.1

    c['x'] += c['v']

  # draw

  screen.fill(Color(0, 0, 0))

  screen.fill(Color(150, 0, 0), Rect(site_start, 80, site_end-site_start, 40))

  r = Rect(0, 0, 10, 10)
  for c in cars:
    r.center = (c['x'], 100)
    col = Color(255, 0, 0)
    if c['alert']>0:
      col = Color(255, 255, 255)
    screen.fill(col, r)

  display.flip()
  # time.wait(5)
