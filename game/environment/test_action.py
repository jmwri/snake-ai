from unittest import TestCase
from game.environment import action
from game.vector import Vector


class TestAction(TestCase):
    def test_equality(self):
        self.assertEqual(action.NONE, action.NONE)
        self.assertIs(action.NONE, action.NONE)
        for a in action.ALL:
            self.assertEqual(a, a)
            self.assertIs(a, a)

    def test_vector_to_action(self):
        self.assertEqual(action.vector_to_action(Vector(-1, 0)), action.LEFT)
        self.assertEqual(action.vector_to_action(Vector(1, 0)), action.RIGHT)
        self.assertEqual(action.vector_to_action(Vector(0, -1)), action.UP)
        self.assertEqual(action.vector_to_action(Vector(0, 1)), action.DOWN)

    def test_vectors_to_action(self):
        vectors = [Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1)]
        self.assertEqual(
            action.vectors_to_action(vectors),
            [action.LEFT, action.RIGHT, action.UP, action.DOWN]
        )

    def test_action_to_relative_left(self):
        self.assertEqual(
            action.action_to_relative_left(action.LEFT),
            action.DOWN
        )
        self.assertEqual(
            action.action_to_relative_left(action.UP),
            action.LEFT
        )
        self.assertEqual(
            action.action_to_relative_left(action.RIGHT),
            action.UP
        )
        self.assertEqual(
            action.action_to_relative_left(action.DOWN),
            action.RIGHT
        )

    def test_action_to_relative_right(self):
        self.assertEqual(
            action.action_to_relative_right(action.LEFT),
            action.UP
        )
        self.assertEqual(
            action.action_to_relative_right(action.UP),
            action.RIGHT
        )
        self.assertEqual(
            action.action_to_relative_right(action.RIGHT),
            action.DOWN
        )
        self.assertEqual(
            action.action_to_relative_right(action.DOWN),
            action.LEFT
        )
