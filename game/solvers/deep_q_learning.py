import numpy as np

from game.agents.deep_q_network import DQNAgent
from game.solvers.abstract import AbstractModel
from game.environment import action as act
from game.environment.environment import Environment


class DeepQLearning(AbstractModel):
    def __init__(self, state_size: int):
        super().__init__(
            "Deep Q Learning",
            "deep_q_learning",
            "dqn"
        )
        self._agent = DQNAgent(state_size, 3, 1)
        self._agent.load('DRN')
        self._frames_shape = (4, state_size)
        self._frames = np.zeros(self._frames_shape, float)

    def reset(self):
        super().reset()

    def next_action(self, environment: Environment) -> act.Action:
        possible_actions = [
            act.action_to_relative_left(environment.snake.action),
            environment.snake.action,
            act.action_to_relative_right(environment.snake.action),
        ]

        action = self._agent.act(self._frames)
        return possible_actions[action]

    def train_after_action(self, environment: Environment, terminal: bool):
        current_frame = [environment.observe()]
        self._frames = np.delete(self._frames, 0, axis=0)
        self._frames = np.append(self._frames, current_frame, axis=0)
