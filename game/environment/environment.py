import random
from typing import Optional, List
from game.environment import action as act, tile
from game.environment.objects import Snake, Fruit, Object
from game.vector import Vector, within_distance, is_diagonal


class Environment:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._tiles = []
        self.fruit = Fruit()
        self.wall = Object()
        self.snake = Snake()

        self._build_tiles()

    def _build_tiles(self):
        # Build 2d list of empty tiles
        for y in range(0, self._height):
            self._tiles.append([])
            for x in range(0, self._width):
                self._tiles[y].append(tile.EMPTY)

    def step(self, action: act.Action) -> bool:
        """
        :param action: The action for the snake to perform
        :return: False if the move resulted in death, otherwise True
        """
        # Eliminate illegal moves
        if self.snake.action.vector.is_reverse(action.vector):
            # Snake's head can't go backwards
            return False
        if not within_distance(action.vector, 1):
            # Attempted action is > 1 tile away
            return False
        if is_diagonal(action.vector):
            # Our snake can only move on 1 axis at a time
            return False

        # Specified action is a legal move, but can still kill the snake
        head = self.snake.head()
        new = act.Vector(
            head.x + action.vector.x,
            head.y + action.vector.y,
        )

        if self.snake.at_vector(new):
            # New position is populated by snake
            return False
        if self.wall.at_vector(new):
            # New position is populated by wall
            return False

        # Nothing bad ahead, move the head of the snake
        self.snake.action = action
        self.snake.move_to(new)
        self._tiles[new.y][new.x] = tile.SNAKE

        # If the new vector is at fruit, we can eat it
        can_eat = self._can_eat_fruit()
        if can_eat:
            if not self.won():
                self.init_fruit()
            return True

        # There was no fruit, so remove 1 tile from the tail
        tail = self.snake.remove_tail()
        self._tiles[tail.y][tail.x] = tile.EMPTY
        return True

    def reward(self) -> int:
        return len(self.snake)

    def _can_eat_fruit(self) -> bool:
        return self.snake.head() == self.fruit.get_vector()

    def init_wall(self):
        self._clear_tiles(tile.WALL)
        # Build walls on the left and right
        for y in range(0, self._height):
            left_x = 0
            right_x = self._width - 1
            self._tiles[y][left_x] = tile.WALL
            self._tiles[y][right_x] = tile.WALL

        # Build walls at top and bottom
        for x in range(1, self._width-1):
            top_y = 0
            bottom_y = self._height - 1
            self._tiles[top_y][x] = tile.WALL
            self._tiles[bottom_y][x] = tile.WALL
        self.wall = Object(self._vectors_of(tile.WALL))

    def init_fruit(self):
        # Place a new fruit at a random position
        self._clear_tiles(tile.FRUIT)
        random_position = self._random_available_position()
        self._tiles[random_position.x][random_position.y] = tile.FRUIT
        self.fruit = Fruit(self._vector_of(tile.FRUIT))

    def init_snake(self):
        # Place a new snake at a random position
        self._clear_tiles(tile.SNAKE)
        random_position = self._random_available_position()
        self._tiles[random_position.x][random_position.y] = tile.SNAKE
        self.snake = Snake([self._vector_of(tile.SNAKE)])
        self.snake.action = random.choice(act.ALL)

    def _vectors_of(self, t: tile.Tile) -> List[Vector]:
        vectors = []
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self._tiles[y][x] == t:
                    vectors.append(Vector(x, y))
        return vectors

    def _vector_of(self, t: tile.Tile) -> Optional[Vector]:
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self._tiles[y][x] == t:
                    return Vector(x, y)
        return None

    def _clear_tiles(self, t: tile.Tile):
        vectors_to_clear = self._vectors_of(t)
        for vector in vectors_to_clear:
            self._tiles[vector.y][vector.x] = tile.EMPTY

    def _random_available_position(self) -> Vector:
        t = None
        rand_x, rand_y = 0, 0
        while t is None or t is not tile.EMPTY:
            rand_x = random.randint(1, self._height - 1)
            rand_y = random.randint(1, self._width - 1)
            t = self._tiles[rand_x][rand_y]
        return Vector(rand_x, rand_y)

    def available_tiles_count(self) -> int:
        return (self._width - 2) * (self._height - 2)

    def won(self) -> bool:
        return self.reward() == self.available_tiles_count()

    def tile_at(self, vector: Vector) -> Optional[tile.Tile]:
        if 0 <= vector.y < self._height and 0 <= vector.x < self._width:
            return self._tiles[vector.y][vector.x]
        return None
