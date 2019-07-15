"""
    Author: Jaakko Huusko
    Date: 30.06.2019

    Description:
    Snake game made using pygame -module
"""
# Import dependencies
import pygame
import numpy as np
import time
from snake import Snake, Candy

# One snake pixel equale pixel_size on screen
pixel_size = 10

# Screen settings
w_pixels = 64
h_pixels = 64

WIDTH = w_pixels * pixel_size
HEIGHT = h_pixels * pixel_size

# Initialize pygame and screen surface
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Snake')

# Create snake instance
snake = Snake(pixel_size, int(w_pixels/2), np.random.randint(0, h_pixels), length=6)


# Create candy
candy = Candy(pixel_size, np.random.randint(w_pixels), np.random.randint(h_pixels))

clock = pygame.time.Clock()
gamestate = np.zeros((w_pixels, h_pixels))
gamestates = []

RUN = True
while snake.alive and RUN:
    gamestate = np.zeros((w_pixels, h_pixels))
    for block in snake.blocks:
        loc = (int(block.y), int(block.x))
        gamestate[loc] = 0.5
    candy_loc = (int(candy.y / pixel_size), int(candy.x / pixel_size))
    gamestate[candy_loc] = 1

    gamestates.append(gamestate)
    # Fill screen with color
    screen.fill((80, 80, 80))

    clock.tick(20)

    # Exit game if exit-button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Check whether arrow keys are pressed and act accordingly
    if keys[pygame.K_UP]:
        if not snake.vy:
            snake.change_direction('UP')

    elif keys[pygame.K_DOWN]:
        if not snake.vy:
            snake.change_direction('DOWN')

    elif keys[pygame.K_LEFT]:
        if not snake.vx:
            snake.change_direction('LEFT')

    elif keys[pygame.K_RIGHT]:
        if not snake.vx:
            snake.change_direction('RIGHT')

    # Move snake
    snake.move()

    # If snake cathes the candy
    if snake.blocks[0].x == candy.x and \
       snake.blocks[0].y == candy.y:
        # Add new block to snake
        snake.add_block()
        # Move candy to a new random location
        candy.x = np.random.randint(0, WIDTH) // pixel_size ** 2 
        candy.y = np.random.randint(0, HEIGHT) // pixel_size ** 2
        # Make sure that the candy is not moved on top of the snake
        while candy.x in [block.x for block in snake.blocks] and \
              candy.y in [block.y for block in snake.blocks]:
            candy.x = np.random.randint(0, WIDTH) // pixel_size ** 2
            candy.y = np.random.randint(0, HEIGHT) // pixel_size ** 2

    # Show snake
    snake.show()
    # Show candy
    candy.show()
    # Update screen
    pygame.display.flip()


import matplotlib.pyplot as plt
for state in gamestates[-4:]:
    plt.matshow(state)
plt.show()
time.sleep(1)

# QUIT pygame
pygame.quit()