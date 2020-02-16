from game.models.abstract import AbstractModel
from game.environment import action as act
from game.environment.environment import Environment
from game.models.breadth_first_search_longest import \
    BreadthFirstSearchLongestPath
from game.vector import Vector


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

    def next_action(self, environment: Environment) -> act.Action:
        # We calculate the cycle one and iterate over it
        if not self._actions:
            # Attempt to build the list of next actions
            head = environment.snake.head()
            tail = environment.snake.tail()
            adjustment = None
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

            built = self._bfsl.build_next_actions(
                environment,
                head,
                tail
            )
            if not built:
                # If we're not able to build them, it usually means there
                # is no path to the fruit. Continue straight.
                return environment.snake.action
            self._actions = built
            self._i = 0
            if adjustment:
                # If we made an adjustment, we need to add an action to ensure
                # we get back to the original starting point.
                self._actions.append(
                    act.vector_to_action(adjustment.reverse())
                )

        # Keep looping over our list of actions
        next_action = self._actions[self._i]
        self._i += 1
        if self._i == len(self._actions):
            self._i = 0
        return next_action
