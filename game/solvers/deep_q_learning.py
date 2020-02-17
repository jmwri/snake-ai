import datetime
import os

import numpy as np

from game.agents.deep_q_network import DQNAgent
from game.solvers.abstract import AbstractModel
from game.environment import action as act, tile
from game.environment.environment import Environment
from game.vector import Vector, angle_from_vector, distance_from_vector


class Observation:
    def __init__(self, left_empty: int, front_empty: int, right_empty: int,
                 angle_to_fruit: float, distance_from_fruit: int):
        self.left_empty = left_empty
        self.front_empty = front_empty
        self.right_empty = right_empty
        self.angle_to_fruit = angle_to_fruit
        self.distance_from_fruit = distance_from_fruit

    @staticmethod
    def len():
        return 4

    def __len__(self):
        return self.len()

    def as_list(self):
        return [
            self.left_empty,
            self.front_empty,
            self.right_empty,
            self.angle_to_fruit,
            # self.distance_from_fruit,
        ]


class Stats:
    def __init__(self, episodes: int = 0, moves_without_death: int = 0,
                 moves_with_death: int = 0, moves_to_fruit: int = 0,
                 moves_from_fruit: int = 0, ate_fruit: int = 0,
                 loss: float = 0.0):
        self.episodes = episodes
        self.moves_without_death = moves_without_death
        self.moves_with_death = moves_with_death
        self.moves_to_fruit = moves_to_fruit
        self.moves_from_fruit = moves_from_fruit
        self.ate_fruit = ate_fruit
        self.loss = loss
        self.scores = []

    def render(self):
        now = datetime.datetime.utcnow()
        print(f'''Over {self.episodes} episodes @ {now},
    Moves without death: {self.moves_without_death}
    Moves with death: {self.moves_with_death}
    Moves towards fruit: {self.moves_to_fruit}
    Moves away from fruit: {self.moves_from_fruit}
    Fruit eaten: {self.ate_fruit}
    Mean score: {sum(self.scores) / len(self.scores)}
    Loss: {self.loss}
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


class DeepQLearning(AbstractModel):
    def __init__(self):
        super().__init__(
            "Deep Q Learning",
            "deep_q_learning",
            "dqn"
        )
        self._agent = DQNAgent(Observation.len(), len(act.ALL), 2000)
        if os.path.exists('DRN.hdf5'):
            self._agent.load('DRN.hdf5')
        self._before_state = None
        self._before_action = None
        self._before_reward = None
        self._move_i = 0
        self._replay_counter = 0
        self._stats = Stats()

    def reset(self):
        super().reset()
        self._before_state = None
        self._before_action = None
        self._before_reward = None
        self._move_i = 0

    def next_action(self, environment: Environment) -> act.Action:
        self._before_state = self._observe(environment)
        self._before_action = environment.snake.action
        self._before_reward = environment.reward()
        self._move_i += 1
        self._replay_counter += 1

        action = self._agent.act(
            np.reshape(self._before_state.as_list(),
                       (1, self._before_state.len())), )
        return act.ALL[action]

    def after_action(self, environment: Environment, terminal: bool):
        after_state = self._observe(environment)
        reward = environment.reward() - self._before_reward
        if environment.reward() > self._before_reward:
            self._stats.moves_without_death += 1
            self._stats.ate_fruit += 1
            self._stats.moves_to_fruit += 1
            reward = 4
        elif after_state.distance_from_fruit > self._before_state.distance_from_fruit:
            self._stats.moves_without_death += 1
            self._stats.moves_from_fruit += 1
            reward = -.4
        elif after_state.distance_from_fruit < self._before_state.distance_from_fruit:
            self._stats.moves_without_death += 1
            self._stats.moves_to_fruit += 1
            reward = .1
        elif terminal:
            self._stats.moves_with_death += 1
            self._stats.moves_from_fruit += 1
            reward = -10

        action_index = act.ALL.index(environment.snake.action)

        done = terminal or environment.won()
        shaped_before_state = np.reshape(self._before_state.as_list(),
                                         (1, self._before_state.len()))
        shaped_after_state = np.reshape(after_state.as_list(),
                                        (1, after_state.len()))
        self._agent.memorize(
            shaped_before_state,
            action_index,
            reward,
            shaped_after_state,
            done
        )
        if done:
            self._stats.episodes += 1
            self._stats.scores.append(environment.reward())
            if self._stats.episodes >= 20:
                loss = self._agent.replay(500)
                self._agent.update_target_network()
                self._stats.loss = loss
                self._agent.save('DRN.hdf5')
                self._stats.render()
                self._stats.reset()

    def _observe(self, env: Environment) -> Observation:
        # TODO: Change to:
        # - Relative left is empty
        # - Relative front is empty
        # - Relative right is empty
        # - Relative angle to fruit (-1, 0, 1)

        direction = env.snake.action

        left_action = act.action_to_relative_left(direction)
        front_action = direction
        right_action = act.action_to_relative_right(direction)
        left_clear = int(self._is_vector_empty(
            env, env.snake.head() + left_action.vector
        ))
        front_clear = int(self._is_vector_empty(
            env, env.snake.head() + front_action.vector
        ))
        right_clear = int(self._is_vector_empty(
            env, env.snake.head() + right_action.vector
        ))
        return Observation(
            left_clear,
            front_clear,
            right_clear,
            angle_from_vector(
                env.snake.head(),
                direction.vector,
                env.fruit.get_vector()
            ),
            distance_from_vector(
                env.snake.head(), env.fruit.get_vector()
            ),
        )

    def _is_vector_empty(self, env: Environment, vector: Vector) -> bool:
        t = env.tile_at(vector)
        return t == tile.EMPTY
