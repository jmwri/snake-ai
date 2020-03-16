from unittest import TestCase
from game.environment import objects, environment, tile, action
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
        e = environment.Environment(5, 5)
        test_cases = [
            {
                'desc': 'Top right to top left',
                'vectors': [Vector(1, 1), Vector(2, 1), Vector(3, 1)],
                'snake_action': action.LEFT,
                'valid_actions': [action.DOWN],
            }, {
                'desc': 'Top left to bottom left',
                'vectors': [Vector(1, 3), Vector(1, 2), Vector(1, 1)],
                'snake_action': action.DOWN,
                'valid_actions': [action.RIGHT],
            }, {
                'desc': 'Bottom left to bottom right',
                'vectors': [Vector(3, 3), Vector(2, 3), Vector(1, 3)],
                'snake_action': action.RIGHT,
                'valid_actions': [action.UP],
            }, {
                'desc': 'Bottom right to top right',
                'vectors': [Vector(3, 1), Vector(3, 2), Vector(3, 3)],
                'snake_action': action.UP,
                'valid_actions': [action.LEFT],
            }, {
                'desc': 'Bottom middle to middle',
                'vectors': [Vector(2, 2), Vector(2, 3)],
                'snake_action': action.UP,
                'valid_actions': [action.LEFT, action.UP, action.RIGHT],
            }, {
                'desc': 'Left middle to middle',
                'vectors': [Vector(2, 2), Vector(1, 2)],
                'snake_action': action.RIGHT,
                'valid_actions': [action.DOWN, action.UP, action.RIGHT],
            }, {
                'desc': 'Top middle to middle',
                'vectors': [Vector(2, 2), Vector(2, 1)],
                'snake_action': action.DOWN,
                'valid_actions': [action.DOWN, action.LEFT, action.RIGHT],
            }, {
                'desc': 'Right middle to middle',
                'vectors': [Vector(2, 2), Vector(3, 2)],
                'snake_action': action.LEFT,
                'valid_actions': [action.DOWN, action.LEFT, action.UP],
            },
        ]
        e.init_wall()
        for test_case in test_cases:
            e.init_snake(test_case['vectors'], test_case['snake_action'])
            valid_act_descs = [
                a.description for a in test_case['valid_actions']
            ]
            seen_actions = []

            # For each test case assert that all of our valid actions
            # are selected at least once
            for i in range(20):
                rand_act = e.random_action()
                if rand_act.description not in seen_actions:
                    seen_actions.append(rand_act.description)
                self.assertIn(rand_act.description, valid_act_descs)
            self.assertEqual(len(seen_actions), len(valid_act_descs))

    def test_available_tiles_count(self):
        pass

    def test_won(self):
        pass

    def test_tile_at(self):
        pass
