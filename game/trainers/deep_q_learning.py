import datetime
import math

import numpy as np

from game.agents.deep_q_network import DQNTrainingAgent
from game.solvers.abstract import AbstractModel
from game.environment import action as act
from game.environment.environment import Environment
from game.vector import distance_from_vector


class Stats:
    def __init__(self, episodes: int = 0, moves_without_death: int = 0,
                 moves_with_death: int = 0, moves_to_fruit: int = 0,
                 moves_from_fruit: int = 0, ate_fruit: int = 0,
                 loss: float = 0.0, epsilon: float = 0.0):
        self.episodes = episodes
        self.moves_without_death = moves_without_death
        self.moves_with_death = moves_with_death
        self.moves_to_fruit = moves_to_fruit
        self.moves_from_fruit = moves_from_fruit
        self.ate_fruit = ate_fruit
        self.loss = loss
        self.epsilon = epsilon
        self.scores = []
        self.rewards = []

    def render(self):
        now = datetime.datetime.utcnow()
        mean_score = 0
        if len(self.scores):
            mean_score = sum(self.scores) / len(self.scores)
        print(f'''Over {self.episodes} episodes @ {now},
    Moves without death: {self.moves_without_death}
    Moves with death: {self.moves_with_death}
    Moves towards fruit: {self.moves_to_fruit}
    Moves away from fruit: {self.moves_from_fruit}
    Fruit eaten: {self.ate_fruit}
    Mean score: {mean_score}
    Rewards: {sum(self.rewards)}
    Loss: {self.loss}
    Epsilon: {self.epsilon}
        ''')

    def reset(self):
        self.episodes = 0
        self.moves_without_death = 0
        self.moves_with_death = 0
        self.moves_to_fruit = 0
        self.moves_from_fruit = 0
        self.ate_fruit = 0
        self.scores = []
        self.loss = 0.0
        self.epsilon = 0.0
        self.rewards = []


class DeepQLearningTrainer(AbstractModel):
    def __init__(self, state_size: int, batch_size: int):
        super().__init__(
            "Deep Q Learning",
            "deep_q_learning",
            "dqn"
        )
        self._agent = DQNTrainingAgent(
            state_size,
            3,
            5000,
            .95,
            .5,
            .25,
            .995,
            .1
        )
        self._agent.load('DRN')
        self._agent.set_refractory_period(1)
        self._before_frames = None
        self._before_action = None
        self._before_reward = None
        self._before_distance = None
        self._stats = Stats()
        self._batch_amount = batch_size
        self._batch_size = batch_size
        self._replay_batch_size = batch_size * 10
        self._frames_shape = (4, state_size)
        self._frames = np.zeros(self._frames_shape, float)
        self._before_possible_actions = None

    def reset(self):
        super().reset()
        self._agent.set_refractory_period(1)
        self._before_frames = None
        self._before_action = None
        self._before_reward = None
        self._before_distance = None
        self._before_possible_actions = None

    def next_action(self, environment: Environment) -> act.Action:
        self._before_frames = np.copy(self._frames)
        self._before_action = environment.snake.action
        self._before_reward = environment.reward()
        self._before_distance = distance_from_vector(
            environment.snake.head(),
            environment.fruit.get_vector()
        )

        self._before_possible_actions = [
            act.action_to_relative_left(self._before_action),
            self._before_action,
            act.action_to_relative_right(self._before_action),
        ]

        action = self._agent.act(self._frames)

        return self._before_possible_actions[action]

    def train_after_action(self, environment: Environment, terminal: bool):
        current_frame = [environment.observe()]
        self._frames = np.delete(self._frames, 0, axis=0)
        self._frames = np.append(self._frames, current_frame, axis=0)

        reward = self._get_reward(environment, terminal)
        self._stats.rewards.append(reward)

        action_index = self._before_possible_actions.index(
            environment.snake.action
        )

        done = terminal or environment.won()
        self._agent.memorize(
            self._before_frames,
            action_index,
            reward,
            np.copy(self._frames),
            done
        )
        if done or environment.reward() > self._before_reward:
            self._agent.set_refractory_period(environment.snake.length())
        if done:
            self._stats.episodes += 1
            if self._stats.episodes >= self._batch_size:
                loss = self._agent.replay(self._replay_batch_size)
                self._agent.update_target_network()
                self._stats.loss = loss
                self._stats.epsilon = self._agent.epsilon
                self._agent.save('DRN')
                self._stats.render()
                self._stats.reset()

    def _get_reward(self, env: Environment, terminal: bool) -> float:
        after_distance = distance_from_vector(
            env.snake.head(),
            env.fruit.get_vector()
        )
        # Snake got longer
        if env.reward() > self._before_reward:
            self._stats.ate_fruit += 1
            self._stats.moves_to_fruit += 1
            return 1
        # Snake died
        if terminal:
            self._stats.moves_with_death += 1
            self._stats.moves_from_fruit += 1
            return -1
        # Snake got further from fruit
        if after_distance > self._before_distance:
            self._stats.moves_from_fruit += 1
        # Snake got closer to fruit
        if after_distance < self._before_distance:
            self._stats.moves_to_fruit += 1

        self._stats.moves_without_death += 1

        distance_reward = self._distance_reward(
            env.snake.length(),
            self._before_distance,
            after_distance
        )
        return 0 + distance_reward

    def _distance_reward(self, l: int, bd: int, ad: int) -> float:
        l = 2 if l < 2 else l
        return math.log((l + bd) / (l + ad)) / math.log(l)
