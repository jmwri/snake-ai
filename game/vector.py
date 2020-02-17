import math


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

    def rotate(self) -> 'Vector':
        """
        Rotate clockwise
        """
        return Vector(-self.y, self.x)

    def is_reverse(self, other: 'Vector') -> bool:
        return self.reverse() == other

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector'):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'x: {self.x} y: {self.y}'


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


def angle_from_vector(from_vector: Vector, direction: Vector, to_vector: Vector) -> float:
    radians = math.atan2(to_vector.y - from_vector.y, to_vector.x - from_vector.x)

    if direction == Vector(0, -1):
        adjustment = math.pi / 2, math.pi * 3 / 2
    elif direction == Vector(-1, 0):
        adjustment = math.pi, math.pi
    elif direction == Vector(0, 1):
        adjustment = math.pi * 3 / 2, math.pi / 2
    else:
        adjustment = 0, 0

    adjusted_angle_cw = radians + adjustment[0]
    adjusted_angle_ccw = radians - adjustment[1]
    if abs(adjusted_angle_cw) < abs(adjusted_angle_ccw):
        return adjusted_angle_cw
    else:
        return adjusted_angle_ccw


def distance_from_vector(from_vector: Vector, to_vector: Vector) -> int:
    diff = to_vector - from_vector
    x_diff = abs(diff.x)
    y_diff = abs(diff.y)
    return x_diff + y_diff
