import pygame
import random
import math

class Noise:
    def __init__(self, x: float, y: float):
        self.x0 = int(x)
        self.y0 = int(y)
        self.x1 = x + 1
        self.y1 = y + 1

        self.sx = x - float(self.x)
        self.sy = y - float(self.y)


    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Noise(self.x + other.x, self.y + other.y)
        else:
            return Noise(self.x + other, self.y + other)
        

    def gradient(self):
        theta = random.uniform(0, 2 * math.pi)

        return (math.cos(theta) * self.x0, math.sin(theta) * self.y0, math.cos(theta) * self.x1, math.sin(theta) * self.y1)
    

    def gridvectorstopoints(self, x: float, y: float):
        return ((x - self.x0, y - self.y0), (x - self.x1, y - self.y1), (x - self.x0, y - self.y1), (x - self.x1, y - self.y0))
    
    
    def dotproduct(self, x: float, y: float):
        gx0, gy0, gx1, gy1 = self.gradient()
        gv = self.gridvectorstopoints(x, y)
        return (gx0 * gv[0][0] + gy0 * gv[0][1])
    

    def interpolate(self, point1, point2, t):
        return (point2-point1) * (3.0 - t * 2.0) * t * t + point1


def generate_noise(width: int, height: int, scale: int, octave: int):
    grid = []
    for x in range(0,width,scale):
        for y in range(range, scale):
            grid.append(Noise(x+random.random()*scale, y+random.randdom()*scale))
    

def run(width, height, scale, octave):
    octave = octave
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    scale = scale

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run(800, 800, 20, 2)