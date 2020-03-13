from typing import Optional, List

from game.solvers.abstract import AbstractModel
from game.environment import action as act, tile
from game.environment.environment import Environment
from game.solvers.breadth_first_search_longest import \
    BreadthFirstSearchLongestPath
from game.vector import Vector, to_direction_vectors


class HamiltonianCycle(AbstractModel):
    """
    https://en.wikipedia.org/wiki/Hamiltonian_path
    """
    def __init__(self):
        super().__init__(
            "Hamiltonian Cycle",
            "hamiltonian_cycle",
            "hc"
        )
        self._bfsl = BreadthFirstSearchLongestPath()
        self._actions = []
        self._i = 0

    def build_cycle(self, env: Environment) -> Optional[List[Vector]]:
        # Attempt to build the list of next actions
        head = env.snake.head()
        tail = env.snake.tail()
        # We build a cycle by building the longest path from the snakes
        # head to it's tail. If the snake is only 1 tile long, then we
        # make an 'adjustment' and choose a tile next to the head
        # as the target, essentially faking a tail.
        # This is necessary as our algorithm won't return any actions
        # if the from tile is the same as the target tile.
        if head == tail:
            if tail.x > 1:
                adjustment = Vector(-1, 0)
            else:
                adjustment = Vector(1, 0)
            tail = tail + adjustment
        built = self._bfsl.longest_path(
            env,
            head,
            tail,
            env.snake.action.vector
        )
        if built is None:
            return None

        # We've built the longest path from head to tail, but we need to
        # check that it covers all vectors.
        if len(built) != env.available_tiles_count():
            return None
        built.append(head)
        return built

    def next_action(self, environment: Environment) -> act.Action:
        # We calculate the cycle one and iterate over it
        if not self._actions:
            cycle_vectors = self.build_cycle(environment)
            if not cycle_vectors:
                # If we're not able to build them, it usually means there
                # is no path to the fruit. Continue to any available position.
                if environment.tile_at(environment.snake.head() + environment.snake.action.vector) != tile.EMPTY:
                    return environment.random_action()
                return environment.snake.action
            cycle_action_vectors = to_direction_vectors(cycle_vectors)
            self._actions = act.vectors_to_action(cycle_action_vectors)
            self._i = 0

        # Keep looping over our list of actions
        next_action = self._actions[self._i]
        self._i += 1
        if self._i == len(self._actions):
            self._i = 0
        return next_action

    def reset(self):
        self._bfsl.reset()
        self._actions = []
        self._i = 0
