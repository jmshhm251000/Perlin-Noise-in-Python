import sys
import pygame
import random
import math
import numpy as np
import glm


# Generate gradients(a unit vector) for each grid points
def generate_gradients(width, height):
    gradients = {}
    for x in range(width + 1):
        for y in range(height + 1):
            random.seed(x + y * 57)
            angle = random.uniform(0, 2 * math.pi)
            # Store each gradient of length 1 in R^2, cos^2 + sin^2 = 1
            gradients[(x, y)] = glm.vec2(math.cos(angle), math.sin(angle))
    return gradients


# Dot product of the gradient and the distance vector
def dot_product(x, y, ix, iy, gradients):
    dx = x - ix
    dy = y - iy
    gradient = gradients[(ix, iy)]
    distance = glm.vec2(dx, dy)
    return glm.dot(distance, gradient)
    #return dx * gradient[0] + dy * gradient[1]


# Smooth interpolation between grid points
def smoothstep(t):
    return (3.0 * t * t) - (2.0 * t * t * t)


# Linear interpolation between two points
def lerp(a, b, t):
    return a + t * (b - a)


# Noise in a grid
def noise(x, y, gradients):
    x0 = int(x)
    y0 = int(y)
    x1 = x0 + 1
    y1 = y0 + 1

    #fade function for smooth interpolation
    dx = smoothstep(x - x0)
    dy = smoothstep(y - y0)

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


# generate perlin noise and assign it to a 2D array
def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    gradients = generate_gradients(width, height)
    x_cord = np.arange(width) / scale
    y_cord = np.arange(height) / scale
    xv, yv = np.meshgrid(x_cord, y_cord)

    noise_array = np.zeros((width, height))

    for octave in range(octaves):
        frequency = lacunarity ** octave
        amplitude = persistence ** octave
        xvf = xv * frequency
        yvf = yv * frequency

        for x in range(width):
            for y in range(height):
                noise_value = noise(xvf[y, x], yvf[y, x], gradients) * amplitude
                noise_array[x, y] += noise_value
    
    # Normalize the noise array from [-1,1] to [0,1]
    noise_array = (noise_array + 1) / 2

    return noise_array


# Convert the noise array to grayscale
def noise_to_grayscale(noise_array):
    clamped_noise = noise_array
    #clamped_noise = np.where(noise_array < 0.3, 0, noise_array)
    arr = np.uint8(clamped_noise * 255)
    grayscale = np.stack((arr,) * 3, axis=-1)
    return grayscale


# pygame loops and main function
def run(width, height, scale, octaves, persistence, lacunarity):

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Perlin Fractal Noise")

    start_ticks = pygame.time.get_ticks()

    noise_array = generate_perlin_noise(SCREEN_WIDTH, SCREEN_HEIGHT, scale, octaves, persistence, lacunarity)
    grayscale = noise_to_grayscale(noise_array)
    surface = pygame.surfarray.make_surface(grayscale)

    end_ticks = pygame.time.get_ticks()
    elapsed_time = (end_ticks - start_ticks)
    print(f"Noise Calculation Finished in {elapsed_time} ms.")

    # Main loop for pygame window
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
    sys.exit()

if __name__ == "__main__":
    
    # Parameters for noise generation
    scale = 100.0
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0

    # Pygame window parameters
    WIDTH = 800
    HEIGHT = 600

    run(WIDTH, HEIGHT, scale, octaves, persistence, lacunarity)