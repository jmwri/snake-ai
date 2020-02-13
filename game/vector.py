class Vector:
    """
    Used as both positional and directional vector
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Vector') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self.x) + str(self.y))

    def reverse(self) -> 'Vector':
        return Vector(-self.x, -self.y)

    def is_reverse(self, other: 'Vector') -> bool:
        return self.reverse() == other


def within_distance(vector: Vector, distance: int) -> bool:
    """
    Calculates if a directional vector is within a certain distance.

          3
      2 2 2 2 2
      2 1 1 1 2
    3 2 1 0 1 2 3
      2 1 1 1 2
      1 2 2 2 2
          3
    """
    return (
            -distance <= vector.x <= distance and
            -distance <= vector.y <= distance
    )


def is_diagonal(vector: Vector) -> bool:
    """
    Return true if a directional vector points diagonally.
    Snake can only move on 1 axis at a time.
    """
    return vector.x != 0 and vector.y != 0
