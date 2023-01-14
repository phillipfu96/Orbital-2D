import pygame
import random
from pygame import gfxdraw

screen_width = 1300
screen_height = 1300
scx = screen_width/2
scy = screen_height/2
win = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
pygame.init()
clock = pygame.time.Clock()
G = .1
# pygame.transform.smoothscale(win, (3000, 3000))
#pygame.transform.smoothscale(win, (2, 2))
class Planet:
    def __init__(self, location, radius, mass):
        self.center = pygame.Vector2(location)
        self.radius = radius
        self.mass = mass

    def influence_to_body(self, body):
        self.range_vector = pygame.Vector2(self.center - body.center)
        self.r_squared = self.range_vector.magnitude_squared()
        self.acceleration = (G * self.mass) / self.r_squared
        self.a_vec = self.range_vector
        self.a_vec.scale_to_length(self.acceleration)
        return self.a_vec


class Body:
    def __init__(self, distance, angle, velocity, starttime):
        self.center = pygame.Vector2((1, 0))
        self.center.from_polar((distance, angle))
        self.center += pygame.Vector2((scx, scy))
        self.born = starttime
        self.velocity = pygame.Vector2((-velocity, 0)).rotate(angle+90)
        self.resting = False
        self.thrust = pygame.Vector2(self.velocity)
        self.thrust.scale_to_length(.05)
        self.history = []
        self.color = random.choices(range(255), k=3)

    def update(self):
        if not self.resting:
            self.velocity += earth.influence_to_body(self)
            self.center = self.center + self.velocity
            self.history.append([self.center[0], self.center[1],self.color, self.born])


earth = Planet((screen_width/2, screen_height/2), 30, 2 * 10e2)

bodies = []
for i in range(22):
    y = earth.radius + 90+ i*7
    v = ((G * earth.mass) / y) ** .5+random.randint(-33, 33)/100
    bodies.append(Body(y, random.randint(0, 30), v, 0))

run = True
refill = 1
ttime = 0
while run:
    clock.tick(90)
    ttime += 1
    pygame.display.set_caption("FPS: " + str(round(clock.get_fps())) + "|" + str(ttime))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        refill -= 1
        refill = abs(refill)

    for b in bodies:
        b.update()
        # pygame.gfxdraw.pixel(win, round(b.center[0]), round(b.center[1]), b.color)
        for h in b.history:
            h[3] += 1
            if h[3] > 235:
                b.history.remove(h)
            pygame.gfxdraw.filled_circle(win, round(h[0]), round(h[1]), 1, (h[2][0], h[2][1], h[2][2], 255-h[3]))
        # pygame.gfxdraw.circle(win, round(b.center[0]), round(b.center[1]), 1, b.color)

        # pygame.draw.aaline(win, (255, 0, 0),(round(b.center[0]), round(b.center[1])), b.center+earth.influence_to_body(b)*500, blend=100)
        # pygame.draw.aaline(win, (255, 0, 0), (round(b.center[0]), round(b.center[1])),
        #                  b.center + earth.influence_to_body(b) * 500, blend=100)
        # pygame.draw.aaline(win, (60, 10, 10), b.center, b.center+b.velocity*5, 4)
        # pygame.draw.aaline(win, (10, 100, 10), earth.center, b.center, 3)

    pygame.draw.circle(win, (0, 0, 255), earth.center, earth.radius)
    # pygame.draw.circle(win, (255, 0, 0), player.center, 2)
    # pygame.draw.aaline(win, (255, 255, 255), player.center, player.center+player.velocity*100, 2)
    # pygame.draw.aaline(win, (255, 255, 0), player.center, player.center+player.thrust*150, 4)

    pygame.display.update()
    if refill:
        win.fill('black')
