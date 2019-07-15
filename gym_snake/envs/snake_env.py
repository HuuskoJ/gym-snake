# Import dependencies
import pygame
import numpy as np
import time
from .snake import Snake, Candy
# Gym related dependencies
import gym
from gym import error, spaces, utils
from gym.utils import seeding

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, W, H):
        
         # Screen settings
        self.w_pixels = W
        self.h_pixels = H

        self.observation_space = spaces.Box(low=0, high=1, shape=(1, W, H), dtype=np.int32)
        self.action_space = spaces.Discrete(4)

        self.pixel_size = 10
        self.snake = None
        self.candy = None
        self.gamestate = np.zeros((self.w_pixels, self.h_pixels))
        self._render = False


    @property
    def state(self):
        return self.gamestate

    def step(self, action):
        if action == 0:
            if not self.snake.vy:
                self.snake.change_direction('UP')

        elif action == 1:
            if not self.snake.vy:
                self.snake.change_direction('DOWN')

        elif action == 2:
            if not self.snake.vx:
                self.snake.change_direction('LEFT')

        elif action == 3:
            if not self.snake.vx:
                self.snake.change_direction('RIGHT')

        reward = self.snake.move(self.candy) # returns 1 if candy is eaten, else 0
        if not reward: reward = -1e5
        self.gamestate *= 0
        for block in self.snake.blocks:
            loc = (int(block.y), int(block.x))
            self.gamestate[loc] = 0.5 # 'Color' for snake
        candy_loc = (int(self.candy.y), int(self.candy.x))
        self.gamestate[candy_loc] = 0.75 # 'Color' for candy
            
        if self.snake.alive:
            reward *= 1000
        else:
            reward = -100

        return self.state, reward, not self.snake.alive, {"info": "INFO"}
        

    def reset(self):
        # Create snake instance
        self.snake = Snake(self.pixel_size,
                            int(self.w_pixels/2 - 3),
                            np.random.randint(1, self.h_pixels-1),
                            length=6,
                            width=self.w_pixels,
                            height=self.h_pixels)
        # Create candy
        self.candy = Candy(self.pixel_size,
                            np.random.randint(self.w_pixels-1),
                            np.random.randint(self.h_pixels-1))
        self.gamestates = []
        self.gamestate *= 0
        for block in self.snake.blocks:
            loc = (int(block.y), int(block.x))
            self.gamestate[loc] = 0.5
        candy_loc = (int(self.candy.y), int(self.candy.x))
        self.gamestate[candy_loc] = 1
        
        return self.state

    def render(self, mode='human', close=False):
        if not self._render:
            # One snake pixel equale pixel_size on screen

            WIDTH = self.w_pixels * self.pixel_size
            HEIGHT = self.h_pixels * self.pixel_size

            # Initialize pygame and screen surface
            pygame.init()
            self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
            pygame.display.set_caption('Snake-v0')

            self.clock = pygame.time.Clock()

            self._render = True
        if self._render:
            # Fill screen with color
            self.screen.fill((80, 80, 80))
            # Choose tick rate
            self.clock.tick(100)
            # Exit game if exit-button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
            # Show snake
            self.snake.show()
            # Show candy
            self.candy.show()
            # Update screen
            pygame.display.flip()
        else:
            # QUIT pygame
            pygame.quit()


class SnakeEnv32(SnakeEnv):
    def __init__(self):
        super().__init__(W=32, H=32)


if __name__ == '__main__':

    env = SnakeEnv()
    env.reset()
    for i in range(100):
        env.render()
        a = env.action_space.sample()
        s, r, d, _ = env.step(a)

        if d:
            print("Snake died")
            break
