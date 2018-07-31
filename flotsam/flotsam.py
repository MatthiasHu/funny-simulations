import pygame

from polygons import *


width = 800
height = 600

screen = pygame.display.set_mode((width, height))


### shape and initial position of flotsam

# shape = [(3, 0), (6, 0), (10, 6), (-3, 5), (1, 1)]
shape = [(0, 0), (6, 0), (6, 16), (3, 6), (0, 6)]
rho_flotsam = 0.4
rotational_inertia = 100000

x = 0
y = 5
alpha = 0.1
vx = 0
vy = 0
omega = 0


### physical constants

rho_water = 1
g = 9.81


### time increment

dt = 0.02


shape = centered_polygon(shape)
m = polygon_area(shape)*rho_flotsam

def physics_to_screen(p):
    (x, y) = p
    return (int(x*10+width/2), int(-y*10+height/2))


quit = False
while not quit:
    # events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

    # physics
    positioned_shape = translated_polygon((x, y),
            rotated_polygon(alpha, shape) )
    immersed = cut_polygon(positioned_shape)
    (immersed_area, point_of_origin) = polygon_centroid(immersed)
    lift = g * rho_water * immersed_area
    ay = -g + lift/m
    omega += point_of_origin[0] * lift / rotational_inertia
    vy += dt * ay
    alpha += omega
    x += dt * vx
    y += dt * vy

    # draw
    pygame.Surface.fill(screen, (0, 0, 0))
    water_rect = (0, int(height/2), width, int(height/2))
    pygame.draw.rect(screen, (0, 0, 255), water_rect)
    verts = list(map(physics_to_screen, positioned_shape))
    pygame.draw.polygon(screen, (200, 200, 0), verts)
    verts = list(map(physics_to_screen, immersed))
    if len(verts) > 2:
        pygame.draw.polygon(screen, (150, 150, 250), verts)
    pygame.display.update()

#    pygame.time.wait(100)

pygame.quit()
