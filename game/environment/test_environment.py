from unittest import TestCase
from game.environment import objects, environment, tile
from game.vector import Vector


class TestEnvironment(TestCase):
    def test_reward(self):
        e = environment.Environment(10, 10)
        self.assertEqual(
            e.reward(),
            0
        )
        e.init_snake()
        self.assertEqual(
            e.reward(),
            1
        )

    def test_init_wall(self):
        e = environment.Environment(10, 10)
        e.init_wall()
        for x in range(0, 10):
            for y in range(0, 10):
                t = e.tile_at(Vector(x, y))
                if (x == 0 or x == 9) or (y == 0 or y == 9):
                    self.assertEqual(t, tile.WALL)
                else:
                    self.assertEqual(t, tile.EMPTY)

    def test_init_fruit(self):
        e = environment.Environment(10, 10)
        e.init_fruit()
        f = e.fruit.get_vector()
        for x in range(0, 10):
            for y in range(0, 10):
                t = e.tile_at(Vector(x, y))
                if x == f.x and y == f.y:
                    self.assertEqual(t, tile.FRUIT)
                else:
                    self.assertEqual(t, tile.EMPTY)

    def test_init_snake(self):
        e = environment.Environment(10, 10)
        e.init_snake()
        for x in range(0, 10):
            for y in range(0, 10):
                v = Vector(x, y)
                t = e.tile_at(v)
                if e.snake.at_vector(v):
                    self.assertEqual(t, tile.SNAKE)
                else:
                    self.assertEqual(t, tile.EMPTY)

    def test_random_action(self):
        pass

    def test_available_tiles_count(self):
        pass

    def test_won(self):
        pass

    def test_tile_at(self):
        pass
