from typing import List

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


def vector_to_action(vector: Vector) -> Action:
    for a in ALL:
        if a.vector == vector:
            return a
    raise Exception(f'vector {vector} does not map to an action')


def vectors_to_action(vectors: List[Vector]) -> List[Action]:
    return [vector_to_action(v) for v in vectors]


def action_to_relative_left(a: Action) -> Action:
    if a == RIGHT:
        return UP
    elif a == DOWN:
        return RIGHT
    elif a == LEFT:
        return DOWN
    elif a == UP:
        return LEFT


def action_to_relative_right(a: Action) -> Action:
    if a == UP:
        return RIGHT
    elif a == RIGHT:
        return DOWN
    elif a == DOWN:
        return LEFT
    elif a == LEFT:
        return UP
