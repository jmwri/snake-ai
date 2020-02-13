from game.vector import Vector


class Action:
    def __init__(self, vector: Vector):
        self.vector = vector

    def __eq__(self, other: 'Action'):
        return self.vector == other.vector


NONE = Action(Vector(0, 0))
LEFT = Action(Vector(-1, 0))
UP = Action(Vector(0, -1))
RIGHT = Action(Vector(1, 0))
DOWN = Action(Vector(0, 1))

ALL = (
    LEFT, UP, RIGHT, DOWN,
)
