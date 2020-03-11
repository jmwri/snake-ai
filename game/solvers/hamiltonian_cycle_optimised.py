from typing import Optional

from game.solvers.abstract import AbstractModel
from game.environment import action as act, tile
from game.environment.environment import Environment
from game.solvers.hamiltonian_cycle import HamiltonianCycle
from game.vector import to_direction_vectors


class HamiltonianCycleOptimised(AbstractModel):
    """
    https://en.wikipedia.org/wiki/Hamiltonian_path
    """

    def __init__(self):
        super().__init__(
            "Hamiltonian Cycle Optimised",
            "hamiltonian_cycle_optimised",
            "hco"
        )
        self._hc = HamiltonianCycle()
        self._vectors = []
        self._actions = []
        self._i = 0

    def next_action(self, environment: Environment) -> act.Action:
        if not self._actions:
            cycle_vectors = self._hc.build_cycle(environment)
            if not cycle_vectors:
                # If we're not able to build them, it usually means there
                # is no path to the fruit. Continue straight.
                return environment.snake.action
            self._vectors = cycle_vectors
            cycle_action_vectors = to_direction_vectors(cycle_vectors)
            self._actions = act.vectors_to_action(cycle_action_vectors)
            self._i = 0

        # If we find a shortcut, take it!
        shortcut_action = self._find_shortcut(environment)
        if shortcut_action:
            return shortcut_action

        # Otherwise proceed as usual
        next_action = self._actions[self._i]
        self._i += 1
        if self._i == len(self._actions):
            self._i = 0
        return next_action

    def _find_shortcut(self, env: Environment) -> Optional[act.Action]:
        possible_actions = [
            act.action_to_relative_left(env.snake.action),
            env.snake.action,
            act.action_to_relative_right(env.snake.action),
        ]
        possible_vectors = [
            env.snake.head() + a.vector for a in possible_actions
        ]
        possible_vectors = [
            v for v in possible_vectors if env.tile_at(v) == tile.EMPTY
        ]

        possible_vectors.sort(
            key=lambda v: self._vectors.index(v),
            reverse=True
        )

        head_i = self._vectors.index(env.snake.head())
        tail_i = self._vectors.index(env.snake.tail())
        fruit_i = self._vectors.index(env.fruit.get_vector())

        s = self._safety(env.snake.length(), len(self._vectors))
        for v in possible_vectors:
            i = self._vectors.index(v)

            if i == head_i + 1:
                # Is next space
                continue
            # If head_i = 20, tail_i = 10, and i is between 10 to 20
            if head_i >= tail_i and tail_i + s < i <= head_i + 1:
                # Shortcut would hit snake
                continue
            # If head_i = 4, tail_i = 80, and i is between 80+ and 4-
            if head_i < tail_i + s < i:
                # Shortcut would hit snake
                continue
            # If head_i = 40, fruit_i = 50, and i > 50
            if head_i < fruit_i < i:
                # Taking the shortcut would skip ahead of fruit
                continue
            # If head_i = 40, fruit_i = 20, and i > 50
            if head_i > fruit_i and fruit_i < i < head_i:
                # We're already ahead of the fruit
                # Taking the shortcut would go back on ourselves,
                # but after the fruit. Would go in circles.
                continue
            # If head_i = 40, fruit_i = 35, and i > 30
            if i < head_i and fruit_i > i:
                # Shortcut goes back on ourselves. Fruit is in front.
                # Go in circles.
                continue
            self._i = i
            if self._i == len(self._vectors):
                self._i = 0
            return act.vector_to_action(v - env.snake.head())
        return None

    def _safety(self, snake_len: int, path_len: int) -> int:
        x1 = (path_len * .04) / path_len  # Point at which the safety starts
        x2 = (path_len * .8) / path_len  # Point at which to use max safety
        s1 = path_len * .1  # Max safety
        s2 = path_len * .01  # Min safety
        m = (s1 - s2)/(x1 - x2)
        y = snake_len/path_len
        c = (s2*x1 - s1*x2)/(x1-x2)
        s = round(m * y + c)
        return s

    def reset(self):
        super().reset()
        self._hc.reset()
        self._vectors = []
        self._actions = []
        self._i = 0
