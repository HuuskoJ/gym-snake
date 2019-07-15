import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, ReLU,MaxPooling2D, Flatten, Conv2D, BatchNormalization, Permute
from keras.optimizers import Adam
import keras.backend as K

from rl.core import Processor
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from PIL import Image

ENV_NAME = 'gym_snake:snake-v0'


INPUT_SHAPE = (64, 64)
WINDOW_LENGTH = 4
MODE = "TRAIN"

class CustomProcessor(Processor):
    '''
    acts as a coupling mechanism between the agent and the environment
    '''

    def process_state_batch(self, batch):
        '''
        Given a state batch, I want to remove the second dimension, because it's
        useless and prevents me from feeding the tensor into my CNN
        '''
        return np.squeeze(batch, axis=1)


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

nb_actions = env.action_space.n

model = Sequential()
model.add(Conv2D(8, (5,5), padding='same', activation='relu',
                 input_shape= env.observation_space.shape, data_format='channels_first'))
model.add(BatchNormalization())
model.add(ReLU())
model.add(MaxPooling2D(padding='same', data_format='channels_first'))
model.add(Conv2D(8, (5,5), padding='same',activation='relu', data_format='channels_first'))
model.add(BatchNormalization())
model.add(ReLU())
model.add(MaxPooling2D(padding='same', data_format='channels_first'))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(nb_actions, activation='softmax'))
model.compile(optimizer='adam',
             loss='categorical_crossentropy')
# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
processor = CustomProcessor()
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50,
               target_model_update=1e-2, policy=policy, processor=processor)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

if MODE == "TRAIN":
    try:
        dqn.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))
    except:
        pass
    dqn.fit(env, nb_steps=10000, visualize=False, verbose=2)

    # After training is done, we save the final weights.
    dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
if MODE == "TEST":
    # Finally, evaluate our algorithm for 5 episodes.
    dqn.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))
    dqn.test(env, nb_episodes=10, visualize=True)