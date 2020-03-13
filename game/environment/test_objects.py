from unittest import TestCase
from game.environment import objects
from game.vector import Vector


class TestObject(TestCase):
    def setUp(self) -> None:
        self._vectors = [
            Vector(1, 1),
            Vector(1, 2),
            Vector(1, 3),
        ]
        self._o = objects.Object(self._vectors)

    def test_get_vectors(self):
        self.assertEqual(
            self._o.get_vectors(),
            self._vectors
        )

    def test_at_vector(self):
        self.assertTrue(self._o.at_vector(Vector(1, 1)))
        self.assertTrue(self._o.at_vector(Vector(1, 2)))
        self.assertTrue(self._o.at_vector(Vector(1, 3)))
        self.assertFalse(self._o.at_vector(Vector(1, 4)))


class TestFruit(TestCase):
    def setUp(self) -> None:
        self._vector = Vector(4, 3)
        self._f = objects.Fruit(self._vector)

    def test_get_vector(self):
        self.assertEqual(
            self._f.get_vector(),
            self._vector
        )

    def test_at_vector(self):
        self.assertTrue(self._f.at_vector(Vector(4, 3)))
        self.assertFalse(self._f.at_vector(Vector(1, 2)))
        self.assertFalse(self._f.at_vector(Vector(1, 3)))


class TestSnake(TestCase):
    def setUp(self) -> None:
        ######
        #  TSS
        #HSS S
        #  S S
        #  S S
        #  SSS
        ######
        self._s = objects.Snake([
            Vector(1, 2), Vector(2, 2), Vector(3, 2), Vector(3, 3),
            Vector(3, 4), Vector(3, 5), Vector(4, 5), Vector(5, 5),
            Vector(5, 4), Vector(5, 3), Vector(5, 2), Vector(5, 1),
            Vector(5, 0), Vector(4, 0), Vector(3, 0),
        ])

    def test_head(self):
        self.assertEqual(self._s.head(), Vector(1, 2))

    def test_tail(self):
        self.assertEqual(self._s.tail(), Vector(3, 0))

    def test_len(self):
        self.assertEqual(self._s.length(), 15)
        self.assertEqual(len(self._s), 15)

    def test_move_to_valid_vectors(self):
        valid_vectors = [Vector(4, 5), Vector(5, 4), Vector(5, 6)]
        for v in valid_vectors:
            s = objects.Snake([Vector(5, 5), Vector(6, 5)])
            self.assertTrue(s.move_to(v))
            self.assertEqual(len(s), 3)

    def test_move_to_existing_vector(self):
        invalid_vectors = [Vector(6, 5), Vector(5, 6)]
        for v in invalid_vectors:
            s = objects.Snake([
                Vector(5, 5), Vector(6, 5),
                Vector(6, 6), Vector(5, 6)
            ])
            self.assertFalse(s.move_to(v))
            self.assertEqual(len(s), 4)

    def test_move_to_not_adjacent(self):
        invalid_vectors = [
            Vector(5, 3), Vector(7, 5), Vector(5, 7), Vector(3, 5)
        ]
        for v in invalid_vectors:
            s = objects.Snake([Vector(5, 5)])
            self.assertFalse(s.move_to(v))
            self.assertEqual(len(s), 1)

    def test_remove_tail(self):
        expected_vectors = [v for v in self._s.get_vectors()]
        expected_vectors.reverse()
        for expected_v in expected_vectors:
            old_len = len(self._s)
            v = self._s.remove_tail()
            self.assertEqual(old_len - 1, len(self._s))
            self.assertEqual(expected_v, v)

        self.assertRaises(IndexError, self._s.remove_tail)
