import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
clock = pygame.time.Clock()

# =========================
# CONSTANTS
# =========================
G = 6.67430e-11  # Gravitational constant
SCALE = 6e-11
ZOOM_SCALE = 1e-9
DT = 86400  # 1 day
zoomed = False
paused = False
simulation_time = 0  # in seconds

# Fonts
font = pygame.font.SysFont("Arial", 16)

# Background stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(200)]

# =========================
# BODY CLASS
# =========================
class Body:
    def __init__(self, name, x, y, vx, vy, mass, radius, color):
        self.name = name
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = []

    def update_position(self, bodies):
        fx = fy = 0
        for other in bodies:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx*dx + dy*dy)
                if r > 0:
                    f = G * self.mass * other.mass / (r*r)
                    fx += f * dx / r
                    fy += f * dy / r
        
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT
        
        current_scale = ZOOM_SCALE if zoomed else SCALE
        self.trail.append((int(self.x * current_scale + WIDTH//2),
                           int(self.y * current_scale + HEIGHT//2)))
        if len(self.trail) > 200:
            self.trail.pop(0)

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (80, 80, 80), False, self.trail, 1)
        
        current_scale = ZOOM_SCALE if zoomed else SCALE
        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)

        # Draw body
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

        # Draw name
        label = font.render(self.name, True, (255, 255, 255))
        screen.blit(label, (screen_x + self.radius + 3, screen_y))

# =========================
# PLANETS
# =========================
bodies = [
    Body("Sun", 0, 0, 0, 0, 1.989e30, 12, (255, 255, 0)),
    Body("Mercury", 5.79e10, 0, 0, 47360, 3.301e23, 3, (169, 169, 169)),
    Body("Venus", 1.082e11, 0, 0, 35020, 4.867e24, 4, (255, 165, 0)),
    Body("Earth", 1.496e11, 0, 0, 29780, 5.972e24, 5, (0, 100, 255)),
    Body("Mars", 2.279e11, 0, 0, 24077, 6.39e23, 4, (255, 100, 0)),
    Body("Jupiter", 7.786e11, 0, 0, 13070, 1.898e27, 7, (200, 150, 100)),
    Body("Saturn", 1.432e12, 0, 0, 9680, 5.683e26, 6, (250, 200, 100)),
    Body("Uranus", 2.867e12, 0, 0, 6810, 8.681e25, 5, (100, 200, 255)),
    Body("Neptune", 4.515e12, 0, 0, 5430, 1.024e26, 5, (0, 0, 255)),
    Body("Pluto", 5.906e12, 0, 0, 4670, 1.309e22, 2, (150, 100, 50)),
]

# =========================
# MAIN LOOP
# =========================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:  # zoom toggle
                zoomed = not zoomed
                for body in bodies:
                    body.trail = []

            if event.key == pygame.K_SPACE:  # pause
                paused = not paused

            if event.key == pygame.K_r:  # reset trails
                for body in bodies:
                    body.trail = []

            if event.key == pygame.K_UP:  # speed up
                DT *= 2
            if event.key == pygame.K_DOWN:  # slow down
                DT = max(100, DT // 2)  # prevent zero

    # Draw background (stars)
    screen.fill((0, 0, 0))
    for star in stars:
        screen.set_at(star, (255, 255, 255))

    # Sun glow effect
    pygame.draw.circle(screen, (255, 255, 100, 50), (WIDTH//2, HEIGHT//2), 50)

    if not paused:
        for body in bodies:
            body.update_position(bodies)
        simulation_time += DT

    for body in bodies:
        body.draw(screen)

    # HUD (time, speed, status)
    years = simulation_time / (60*60*24*365)
    hud = font.render(f"Time: {years:.2f} years | DT={DT} sec | {'Paused' if paused else 'Running'}", True, (255,255,255))
    screen.blit(hud, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
