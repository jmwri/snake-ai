import datetime

from game.agents.deep_q_network import DQNAgent
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


class DeepQLearning(AbstractModel):
    def __init__(self, state_size: int):
        super().__init__(
            "Deep Q Learning",
            "deep_q_learning",
            "dqn"
        )
        self._agent = DQNAgent(state_size, 3, 5000)
        self._agent.load('DRN')
        self._before_state = None
        self._before_action = None
        self._before_reward = None
        self._before_distance = None
        self._replay_counter = 0
        self._stats = Stats()
        self._batch_size = 50
        self._replay_batch_size = 500

    def reset(self):
        super().reset()
        self._before_state = None
        self._before_action = None
        self._before_reward = None
        self._before_distance = None

    def next_action(self, environment: Environment) -> act.Action:
        self._before_state = environment.observe()
        self._before_action = environment.snake.action
        self._before_reward = environment.reward()
        self._before_distance = distance_from_vector(
            environment.snake.head(),
            environment.fruit.get_vector()
        )
        self._replay_counter += 1

        possible_actions = [
            act.action_to_relative_left(self._before_action),
            self._before_action,
            act.action_to_relative_right(self._before_action),
        ]

        action = self._agent.act(self._before_state)

        return possible_actions[action]

    def after_action(self, environment: Environment, terminal: bool):
        possible_actions = [
            act.action_to_relative_left(self._before_action),
            self._before_action,
            act.action_to_relative_right(self._before_action),
        ]
        after_state = environment.observe()

        reward = self._get_reward(environment, terminal)

        action_index = possible_actions.index(environment.snake.action)

        done = terminal or environment.won()
        self._agent.memorize(
            self._before_state,
            action_index,
            reward,
            after_state,
            done
        )
        if done:
            self._stats.episodes += 1
            self._stats.scores.append(environment.reward())
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
            self._stats.moves_without_death += 1
            self._stats.moves_from_fruit += 1
            return -.2
        # Snake got closer to fruit
        if after_distance < self._before_distance:
            self._stats.moves_without_death += 1
            self._stats.moves_to_fruit += 1
            return .1

        self._stats.moves_without_death += 1
        return 0
