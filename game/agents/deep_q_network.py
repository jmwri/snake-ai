import random
from collections import deque
import tensorflow as tf
import numpy as np


class DQNAgent:
    def __init__(self, state_size: int, action_size: int,
                 memory_len: int = 2000):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=memory_len)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01
        self.train_net = self._build_network()
        self.target_net = self._build_network()

    def _build_network(self):
        # Neural Net for Deep-Q learning Model
        network = tf.keras.Sequential()
        network.add(tf.keras.layers.Dense(128, input_dim=self.state_size,
                                        activation='relu'))
        network.add(tf.keras.layers.Dense(64, activation='relu'))
        network.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        network.compile(
            loss='mse',
            optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate)
        )
        return network

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.train_net.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size: int):
        if len(self.memory) < batch_size:
            return
        mini_batch = random.sample(self.memory, batch_size)
        states, targets_f = [], []
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.target_net.predict(next_state)[0]))
            target_f = self.train_net.predict(state)
            target_f[0][action] = target
            # Filtering out states and targets for training
            states.append(state[0])
            targets_f.append(target_f[0])
        history = self.train_net.fit(
            np.array(states), np.array(targets_f), epochs=1, verbose=0
        )
        # Keeping track of loss
        loss = history.history['loss'][0]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return loss

    def update_target_network(self):
        self.target_net.set_weights(self.train_net.get_weights())

    def load(self, name):
        self.train_net.load_weights(name)

    def save(self, name):
        self.train_net.save_weights(name)
