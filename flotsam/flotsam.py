import pygame


width = 800
height = 600

screen = pygame.display.set_mode((width, height))

g = 9.81

w = 3
h = 8
m = 15
rho = 1

x = 0
vx = 0
y = 10
vy = 0

dt = 0.02

quit = False
while not quit:
    # events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

    # physics
    immersion_depth = 0
    if y<h/2:
        if y>-h/2:
            immersion_depth = h/2-y
        else:
            immersion_depth = h
    lift = immersion_depth * w * rho * g
    ay = -g + lift/m
    vy += dt * ay
    x += dt * vx
    y += dt * vy

    # draw
    pygame.Surface.fill(screen, (0, 0, 0))
    water_rect = (0, int(height/2), width, int(height/2))
    pygame.draw.rect(screen, (0, 0, 255), water_rect)
    verts = [(x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2)]
    verts = [ (int(a*10+width/2), int(-b*10+height/2)) for (a, b) in verts ]
    pygame.draw.polygon(screen, (200, 200, 0), verts)
    pygame.display.update()


pygame.quit()
