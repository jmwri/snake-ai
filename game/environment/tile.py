class Tile:
    def __init__(self, char: str, value: float):
        self.char = char
        self.value = value


WALL = Tile("#", 0.66)
SNAKE = Tile("x", 0.33)
FRUIT = Tile("o", 1)
EMPTY = Tile(" ", 0)
