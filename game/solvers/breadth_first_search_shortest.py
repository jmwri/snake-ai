from typing import List, Optional

from game.solvers.abstract import AbstractModel
from game.environment import action as act, tile
from game.environment.environment import Environment
from game.vector import Vector, to_direction_vectors


class OwnedVector(Vector):
    def __init__(self, x: int, y: int, owner: Vector):
        super(OwnedVector, self).__init__(x, y)
        self.owner = owner


class BreadthFirstSearchShortestPath(AbstractModel):
    """
    https://en.wikipedia.org/wiki/Breadth-first_search
    """

    def __init__(self):
        super().__init__(
            "Breadth First Search Shortest",
            "breadth_first_search_shortest",
            "bfss"
        )

    def next_action(self, environment: Environment) -> act.Action:
        next_vectors = self.shortest_path(
            environment,
            environment.snake.head(),
            environment.fruit.get_vector(),
            environment.snake.action.vector
        )
        if not next_vectors:
            # If we didn't find the fruit, continue straight in hopes a path
            # will be available next tick
            return environment.snake.action
        next_steps = to_direction_vectors(next_vectors)
        next_step = next_steps[0]
        # We have the next vector we want to move into
        # Map it to the appropriate action for the snake
        return act.vector_to_action(next_step)

    def shortest_path(self, environment: Environment, from_vector: Vector,
                      to_vector: Vector, first_move: Vector
                      ) -> Optional[List[Vector]]:
        # Search for path for fruit. Returned vector has the next vector.
        fruit_vector = self._search_from(
            environment,
            from_vector,
            to_vector,
            first_move
        )
        if fruit_vector is None:
            return None
        vector_steps = []

        # Traverse backwards from the fruit towards to snake
        current_step = fruit_vector
        while True:
            vector_steps.append(Vector(current_step.x, current_step.y))
            if isinstance(current_step, OwnedVector):
                current_step = current_step.owner
            else:
                break

        # We traversed from fruit to snake, so reverse the list
        vector_steps.reverse()
        return vector_steps

    def _search_from(self, env: Environment, start_vector: Vector,
                     end_vector: Vector, first_move: Vector
                     ) -> Optional[OwnedVector]:
        seen_vectors = [start_vector]  # Don't process more than once
        queue = [start_vector]  # First-in-first-out queue

        while queue:
            # Get the first vector from the queue
            vector = queue.pop(0)
            # Check if the tile at the vector is the goal
            if vector == end_vector:
                return vector
            # Get adjacent vectors that we haven't seen yet
            adjacent_vectors = self._unseen_adjacent_vectors(
                env,
                vector,
                seen_vectors
            )
            # Add each adjacent vector to the queue
            for v in adjacent_vectors:
                if vector == start_vector:
                    dir_vec = v - vector
                    if first_move.is_reverse(dir_vec):
                        continue
                queue.append(OwnedVector(v.x, v.y, vector))
                seen_vectors.append(v)

    def _unseen_adjacent_vectors(self, env: Environment, vector: Vector,
                                 seen_vectors: List[Vector]) -> List[Vector]:
        adjacent_vectors = [
            Vector(vector.x-1, vector.y,),
            Vector(vector.x, vector.y-1,),
            Vector(vector.x+1, vector.y,),
            Vector(vector.x, vector.y+1,),
        ]
        searchable_vectors = []
        for v in adjacent_vectors:
            if v in seen_vectors:
                continue
            if self._should_search_vector(env, v):
                searchable_vectors.append(v)
        return searchable_vectors

    def _should_search_vector(self, env: Environment, vector: Vector):
        t = env.tile_at(vector)
        # Snake can't move to a vector that would kill it
        if t == tile.WALL:
            return False
        if t == tile.SNAKE:
            return False
        return True
