from typing import List, Optional

from game.solvers.abstract import AbstractModel
from game.environment import action as act, tile
from game.environment.environment import Environment
from game.solvers.breadth_first_search_shortest import \
    BreadthFirstSearchShortestPath
from game.vector import Vector, to_direction_vectors


class BreadthFirstSearchLongestPath(AbstractModel):
    def __init__(self):
        super().__init__(
            "Breadth First Search Longest",
            "breadth_first_search_longest",
            "bfsl"
        )
        self._bfss = BreadthFirstSearchShortestPath()
        self._next_actions = []

    def next_action(self, environment: Environment) -> act.Action:
        # We don't re-calculate the longest path each tick
        # If we did the snake would never eat the fruit!

        # If we don't know what action to perform next
        if not self._next_actions:
            # Attempt to build the list of next actions
            built = self.build_next_actions(
                environment,
                environment.snake.head(),
                environment.fruit.get_vector()
            )
            if not built:
                # If we're not able to build them, it usually means there
                # is no path to the fruit. Continue straight.
                return environment.snake.action
            self._next_actions = built
        # Return the next action in our list
        return self._next_actions.pop(0)

    def longest_path(self, env: Environment, from_vector: Vector,
                     to_vector: Vector, first_move: Vector
                     ) -> Optional[List[Vector]]:
        # Get the shortest path
        shortest_path = self._bfss.shortest_path(
            env,
            from_vector,
            to_vector,
            first_move
        )
        if not shortest_path:
            return None
        path_len = len(shortest_path)
        # Attempt to make the path longer
        longest_path = self._expand_path(env, shortest_path, to_vector)
        # As long as we are making the path longer, keep doing so
        while len(longest_path) > path_len:
            path_len = len(longest_path)
            longest_path = self._expand_path(env, longest_path, to_vector)
        return longest_path

    def build_next_actions(self, env: Environment, from_vector: Vector,
                           to_vector: Vector) -> Optional[List[act.Action]]:
        longest_path = self.longest_path(
            env,
            from_vector,
            to_vector,
            env.snake.action.vector
        )
        if not longest_path:
            return None

        # Map positional vectors to directional vectors
        next_steps = to_direction_vectors(longest_path)
        # Map directional vectors to their corresponding actions
        return act.vectors_to_action(next_steps)

    def _expand_path(self, env: Environment, path: List[Vector], goal: Vector
                     ) -> List[Vector]:
        # Get a copy of the path
        longest_path = [v for v in path]
        # This HAS to be 0. In the case where the snake hasn't eaten the path
        # is from head to tail.
        i = 0
        while i < len(path) - 1:
            a = longest_path[i]
            b = longest_path[i + 1]
            # Calculate which direction the step is in
            direction = b - a

            dir_action = act.vector_to_action(direction)

            # Rotate the direction, and check if there are 2 spaces clear
            rotated_l = act.action_to_relative_left(dir_action)
            if self._extend_if_possible(
                    env, a, b, rotated_l.vector,
                    longest_path, i, goal):
                break

            # Check the 2 spaces on the opposite side
            rotated_r = act.action_to_relative_left(dir_action)
            if self._extend_if_possible(
                    env, a, b, rotated_r.vector,
                    longest_path, i, goal):
                break
            i += 1
        return longest_path

    def _can_populate_vectors(self, env: Environment, a: Vector, b: Vector,
                              path: List[Vector], goal: Vector) -> bool:
        if not self._can_populate_vector(env, a, path, goal):
            return False
        if not self._can_populate_vector(env, b, path, goal):
            return False
        return True

    def _can_populate_vector(self, env: Environment, vector: Vector,
                             path: List[Vector], goal: Vector) -> bool:
        t = env.tile_at(vector)
        if t == tile.WALL:
            return False
        if t == tile.SNAKE:
            return False
        if vector in path:
            return False
        if vector == goal:
            return False
        return True

    def _extend_if_possible(self, env: Environment, a: Vector, b: Vector,
                            rotation: Vector, path: List[Vector], i: int,
                            goal: Vector) -> bool:
        a_adjacent = a + rotation
        b_adjacent = b + rotation

        if self._can_populate_vectors(env, a_adjacent, b_adjacent,
                                      path, goal):
            path.insert(i + 1, b_adjacent)
            path.insert(i + 1, a_adjacent)
            return True
        return False
