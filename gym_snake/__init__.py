from gym.envs.registration import register

register(
	id='snake64-v0',
	entry_point='gym_snake.envs:SnakeEnv',
	)

register(
	id='snake32-v0',
	entry_point='gym_snake.envs:SnakeEnv32',
	)