import os
import random
from collections import deque
import tensorflow as tf
import numpy as np


class DQNAgent:
    def __init__(self, state_size: int, action_size: int,
                 learning_rate: float = .1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.target_net = self._build_network()

    def _build_network(self) -> tf.keras.Sequential:
        # Neural Net for Deep-Q learning Model
        network = tf.keras.Sequential()
        network.add(tf.keras.layers.Dense(
            100,
            input_dim=self.state_size,
            activation='relu')
        )
        network.add(tf.keras.layers.Dense(
            50,
            input_dim=self.state_size,
            activation='relu')
        )
        network.add(tf.keras.layers.Dense(
            20,
            input_dim=self.state_size,
            activation='relu')
        )
        network.add(tf.keras.layers.Dense(
            10,
            input_dim=self.state_size,
            activation='relu')
        )
        network.add(tf.keras.layers.Dense(
            self.action_size,
            activation='linear'
        ))
        network.compile(
            loss='mse',
            optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate)
        )
        return network

    def act(self, state: np.ndarray):
        act_values = self.target_net.predict(state)
        return np.argmax(act_values[0])

    def load(self, name: str):
        target_network_file = f'{name}.target.h5'
        if os.path.exists(target_network_file):
            self.target_net.load_weights(target_network_file)

    def save(self, name: str):
        self.target_net.save_weights(f'{name}.target.h5')


class DQNTrainingAgent(DQNAgent):
    def __init__(self, state_size: int, action_size: int,
                 memory_len: int = 2000, gamma: float = .95,
                 epsilon: float = .5, epsilon_min: float = .25,
                 epsilon_decay: float = .995, learning_rate: float = .1):
        super().__init__(state_size, action_size, learning_rate)
        self.memory_len = memory_len
        self.memory = deque(maxlen=self.memory_len)
        self.gamma = gamma  # discount rate
        self.epsilon = epsilon  # exploration rate
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.train_net = self._build_network()
        self._refractory_steps = 0

    def set_refractory_period(self, snake_len: int):
        s = self.state_size ** .5 / 2
        p = .4
        q = 2
        k = ((s-q)/p)

        if snake_len < k:
            self._refractory_steps = s
        else:
            self._refractory_steps = p * snake_len * q

    def memorize(self, state: np.ndarray, action: int, reward: float,
                 next_state: np.ndarray, done: int):
        if self._refractory_steps == 0:
            self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray):
        if self._refractory_steps > 0:
            self._refractory_steps -= 1
        r = np.random.rand()
        if r <= self.epsilon:
            return random.randrange(self.action_size)
        return super().act(state)

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
            np.array(states),
            np.array(targets_f),
            epochs=1,
            verbose=0
        )
        # Keeping track of loss
        loss = history.history['loss'][0]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return loss

    def update_target_network(self):
        self.target_net.set_weights(self.train_net.get_weights())

    def load(self, name: str):
        super().load(name)
        train_network_file = f'{name}.train.h5'
        if os.path.exists(train_network_file):
            self.train_net.load_weights(train_network_file)

    def save(self, name: str):
        super().save(name)
        self.train_net.save_weights(f'{name}.train.h5')
