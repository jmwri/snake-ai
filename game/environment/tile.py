class Tile:
    def __init__(self, char: str):
        self.char = char


WALL = Tile("#")
SNAKE = Tile("x")
FRUIT = Tile("o")
EMPTY = Tile(" ")
