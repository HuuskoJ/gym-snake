import pygame
import numpy as np

class Block:

    def __init__(self,pixel_size, x, y, color=(0, 255, 0)):
        
        self.x = x
        self.y = y
        self.size = pixel_size
        self.color = color
        self.screen = None


    def show(self):
        if not self.screen:
            self.screen = pygame.display.get_surface()
        pygame.draw.rect(self.screen,
                         self.color,
                         [self.x * self.size, self.y * self.size,
                          self.size, self.size]) 

        

class Candy(Block):

    def __init__(self, pixel_size, x, y, color=(255, 0, 0)):
        super().__init__(pixel_size, x, y, color)

class Snake:

    def __init__(self, pixel_size,  x, y, length=5, width=64, height=64):
        self.screen = pygame.display.get_surface()
        self.pixel_size = pixel_size
        self.blocks = [Block(pixel_size, x, y)] # Head block
        self.vx = 1
        self.vy = 0
        self.alive = True
        self.width = width
        self.height = height

        for i in range(length):
            self.add_block()

    @property
    def x(self):
        return self.blocks[0].x

    @property
    def y(self):
        return self.blocks[0].y

    def add_block(self):
        
        # Get coordinates of the last block
        x, y = [self.blocks[-1].x, self.blocks[-1].y]
        # If snake is moving in x-direction
        if not self.vy:
            x -= self.vx
        # elif in y-direction
        else:
            y -= self.vy

        # Add new block to blocks
        self.blocks.append(Block(self.pixel_size, x, y))
        

    def change_direction(self, direction):
        
        if direction == 'UP':
            self.vx = 0
            self.vy = -1
            
        elif direction == 'DOWN':
            self.vx = 0
            self.vy = 1
            
        elif direction == 'LEFT':
            self.vx = -1
            self.vy = 0
            
        elif direction == 'RIGHT':
            self.vx = 1
            self.vy = 0

    def move(self, candies):

        reward = 0
        if not self.width:
            self.width, self.height = np.asarray(self.screen.get_size()) / self.pixel_size

        if not 0 < self.x < self.width - self.vx or \
           not 0 < self.y < self.height - self.vy or \
           (self.x + self.vx, self.y + self.vy) in [(block.x, block.y) for block in self.blocks] :
            self.alive = False
            for block in self.blocks:
                block.color = (255, 255, 255)
            
        else:
   
            for i, block in enumerate(reversed(self.blocks[1:])):
                block.x = self.blocks[self.blocks.index(block) - 1].x
                block.y = self.blocks[self.blocks.index(block) - 1].y


        
            self.blocks[0].x += self.vx
            self.blocks[0].y += self.vy


        # If snake cathes the candy
        for candy in candies:
            if self.x == candy.x and \
                self.y == candy.y:
                reward = 1
                # Add new block to snake
                self.add_block()
                # Move candy to a new random location
                candy.x = np.random.randint(0, self.width)
                candy.y = np.random.randint(0, self.height)
                # Make sure that the candy is not moved on top of the snake
                while candy.x in [block.x for block in self.blocks] and \
                    candy.y in [block.y for block in self.blocks]:
                    candy.x = np.random.randint(0, self.width)
                    candy.y = np.random.randint(0, self.height)


        return reward

        

    def show(self):
        for block in self.blocks:
            block.show()
