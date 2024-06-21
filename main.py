import pygame
import random
import math

class Noise:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Noise(self.x + other.x, self.y + other.y)
        else:
            return Noise(self.x + other, self.y + other)
        

    def gradient(self, gridpoints):
        gridpointsgradient = []
        theta = random.uniform(0, 2 * math.pi)
        for point in gridpoints:
            gridpointsgradient.append(Noise(math.cos(theta), math.sin(theta)))

        return gridpointsgradient
    

    def gridvectorstopoints(self, gridpoints):
        gridvectorstopoint = []
        for point in gridpoints:
            gridvectorstopoint.append(Noise(self.x - point.x, self.y - point.y))

        return gridvectorstopoint
    
    
    def dotproduct(self, gridpoints):
        gradient = self.gradient(gridpoints)
        gridvectors = self.gridvectorstopoints(gridpoints)
        points = []
        for i, point in enumerate(gridvectors):
            point.append(points.append(Noise(gradient[i].x * point.x, gradient[i].y * point.y)))
        
        return points

def generate_noise(width: int, height: int, scale: int, octave: int):
    grid = []
    for x in range(width):
        for y in range(range):
            grid.append(0) #will finish this method after lerping and smoothing has been implemented.

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