from typing import List

from game.vector import Vector
from game.environment import action as act


class Object:
    def __init__(self, vectors: List[Vector] = None):
        if vectors is None:
            vectors = []
        self._vectors = vectors

    def at_vector(self, vector: Vector) -> bool:
        return vector in self._vectors

    def get_vectors(self) -> List[Vector]:
        return self._vectors


class Fruit(Object):
    def __init__(self, vector: Vector = None):
        super(Fruit, self).__init__([vector])

    def at_vector(self, vector: Vector) -> bool:
        return vector == self._vectors[0]

    def get_vector(self) -> Vector:
        return self._vectors[0]


class Snake(Object):
    def __init__(self, vectors: List[Vector] = None,
                 action: act.Action = act.NONE):
        super().__init__(vectors)
        self.action = action
        self._length = len(self._vectors)

    def head(self) -> Vector:
        return self._vectors[0]

    def length(self) -> int:
        return len(self._vectors)

    def __len__(self) -> int:
        return self._length

    def move_to(self, vector: Vector):
        self._vectors.insert(0, vector)
        self._length += 1

    def remove_tail(self) -> Vector:
        self._length -= 1
        return self._vectors.pop()
