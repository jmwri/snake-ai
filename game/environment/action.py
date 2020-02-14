from game.vector import Vector


class Action:
    def __init__(self, vector: Vector, description: str):
        self.vector = vector
        self.description = description

    def __eq__(self, other: 'Action'):
        return self.vector == other.vector


NONE = Action(Vector(0, 0), "none")
LEFT = Action(Vector(-1, 0), "left")
UP = Action(Vector(0, -1), "up")
RIGHT = Action(Vector(1, 0), "right")
DOWN = Action(Vector(0, 1), "down")

ALL = (
    LEFT, UP, RIGHT, DOWN,
)
