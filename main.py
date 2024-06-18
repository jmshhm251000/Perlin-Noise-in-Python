import pygame
import random
import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other, self.y + other)
    def gradient(self):
        theta = random.uniform(0, 2 * math.pi)
        gx = math.cos(theta)
        gy = math.sin(theta)
        return Vector(gx, gy)

grid = Vector(380, 280)
print(grid)
print(grid.gradient())

grid = pygame.Rect(380, 280, 40, 40)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


run = True
while run:

    pygame.draw.rect(screen, (0, 0, 255, 255), grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()