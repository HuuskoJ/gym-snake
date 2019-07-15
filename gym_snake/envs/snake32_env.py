from .snake_env import SnakeEnv


class Snake32(SnakeEnv):
    def __init__(self):
        super().__init__(W=32, H=32)




if __name__ == '__main__':

    env = Snake32()
    env.reset()


    for i in range(50):
        a = env.action_space.sample()
        s, r, d, i = env.step(a)

        if d:
            break
