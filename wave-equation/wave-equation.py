import pygame
import numpy as np
import sys

np.tau = 2 * np.pi

N  = 300
s  = 2  # Kachelgröße
dt = 0.002

x = np.random.rand(N,N)**2*10
v = np.zeros((N,N))
k = 1
h = 1 / N

pygame.init()
screen       = pygame.display.set_mode((N*s, N*s))
small_screen = pygame.Surface((N,N))
clock        = pygame.time.Clock()

userTime      = 0
simulatedTime = 0
FPS           = 100
speedup       = 0.1

slow = False

r = 4
if False:
    for i in range(int(N/2)-r,int(N/2)+r+1):
        for j in range(int(N/2)-r,int(N/2)+r+1):
            x[i,j] = (1 - np.sqrt((i-int(N/2))**2 + (j-int(N/2))**2) / (np.sqrt(2) * r)) * 100

while True:
    userTime = userTime + clock.tick(FPS) / 1000 * speedup

    a = 0
    while simulatedTime < userTime:
        a += 1

        if slow:
            z = np.zeros((N,N))
            for i in range(1,N-1):
                for j in range(1,N-1):
                    v[i,j] = v[i,j] + dt * k * (x[i+1,j] + x[i,j+1] + x[i-1,j] + x[i,j-1] - 4 * x[i,j]) / h**2
                    z[i,j] = x[i,j] + dt * v[i,j]
            x = z
        else:
            x += dt * v
            v[1:N-1, 1:N-1] += (dt * k / h**2) * (x[2:N, 1:N-1] + x[0:N-2, 1:N-1] + x[1:N-1, 0:N-2] + x[1:N-1, 2:N] - 4*x[1:N-1, 1:N-1])
            v *= 0.995

        if False:
            i = int(N/2)*0
            ω = 40
            if True:
                for j in range(int(N/2)-r*10,int(N/2)+r*10+1):
                    x[j-int(N/2)+r*10,j-int(N/4)] = np.sin(np.tau * simulatedTime*ω) * 10
                    v[j-int(N/2)+r*10,j-int(N/4)] = np.cos(np.tau * simulatedTime*ω) * 10 * ω

        ω = 20
        x[0,int(3*N/8)] = np.sin(np.tau * simulatedTime * ω) * 100
        x[0,int(5*N/8)] = np.sin(np.tau * simulatedTime * ω) * 100

        simulatedTime = simulatedTime + dt
    print(a)

    screen.fill((255,255,255))
    pygame.surfarray.blit_array(small_screen, np.minimum(np.maximum((x*10+128).astype(int),0),255) * 0x10000)
    pygame.transform.scale(small_screen, (N*s,N*s), screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Aufgetretene Fehler:
# * Vorzeichen in der Wellenungleichung
# * Falsche Updatereihenfolge
# * Metallplatte außerhalb der Physik-for-Schleife
# * Größe von dt
