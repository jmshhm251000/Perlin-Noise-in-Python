import pygame
import random
import math
import numpy as np


def generate_gradients(width, height):
    gradients = {}
    for x in range(width + 1):
        for y in range(height + 1):
            angle = random.uniform(0, 2 * math.pi)
            gradients[(x, y)] = (math.cos(angle), math.sin(angle))
    return gradients


def dot_product(x, y, ix, iy, gradients):
    dx = x - ix
    dy = y - iy
    gradient = gradients[(ix, iy)]
    return dx * gradient[0] + dy * gradient[1]


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a, b, t):
    return a + t * (b - a)


def noise(x, y, gradients):
    x0 = int(x)
    y0 = int(y)
    x1 = x0 + 1
    y1 = y0 + 1

    dx = fade(x - x0)
    dy = fade(y - y0)

    #dot product of bottom two grid points
    dp0 = dot_product(x, y, x0, y0, gradients)
    dp1 = dot_product(x, y, x1, y0, gradients)
    #interpolation of bottom two grid points
    id0 = lerp(dp0, dp1, dx)

    #dot product of top two grid points
    dp0 = dot_product(x, y, x0, y1, gradients)
    dp1 = dot_product(x, y, x1, y1, gradients)
    #interpolation of top two grid points
    id1 = lerp(dp0, dp1, dx)

    return lerp(id0, id1, dy)


def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    gradients = generate_gradients(width, height)
    x_cord = np.arange(width) / scale
    y_cord = np.arange(width) / scale
    xv, yv = np.meshgrid(x_cord, y_cord)

    noise_array = np.zeros((width, height))

    for octave in range(octaves):
        frequency = lacunarity ** octave
        amplitude = persistence ** octave
        for x in range(width):
            for y in range(height):
                noise_value = noise(xv[y, x] * frequency, yv[y, x] * frequency, gradients) * amplitude
                noise_array[x, y] += noise_value
    
    noise_array -= noise_array.min()
    noise_array /= noise_array.max()

    return noise_array


def noise_to_grayscale(noise_array):
    arr = np.uint8(noise_array * 255)
    grayscale = np.stack((arr,) * 3, axis=-1)
    return grayscale


def run(width, height, scale, octaves, persistence, lacunarity):

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Perlin Fractal Noise")

    noise_array = generate_perlin_noise(SCREEN_WIDTH, SCREEN_HEIGHT, scale, octaves, persistence, lacunarity)
    grayscale = noise_to_grayscale(noise_array)
    surface = pygame.surfarray.make_surface(grayscale)
    print("Noise Calculation Finished")

    # Main loop
    run = True
    noise_drawn = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        screen.blit(surface, (0, 0))
        pygame.display.update()

        if not noise_drawn:
            print("Noise has been drawn to the Pygame window.")
            noise_drawn = True

    pygame.quit()

if __name__ == "__main__":
    scale = 100.0
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0

    WIDTH = 800
    HEIGHT = 600

    run(WIDTH, HEIGHT, scale, octaves, persistence, lacunarity)