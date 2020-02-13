from __future__ import annotations
from typing import TYPE_CHECKING, List

from pygame.surface import Surface

from game import colour
from game.vector import Vector

if TYPE_CHECKING:
    from game.game import Game


class ScreenObject:
    def __init__(self, game: Game, col: colour.Colour, vectors: List[Vector]):
        self._game = game
        self._col = col
        self._vectors = vectors

    def set_vectors(self, vectors: List[Vector]):
        self._vectors = vectors

    def draw(self, surface: Surface):
        for vector in self._vectors:
            self._game.draw_tile(surface, self._col, vector)


class SnakeScreenObject(ScreenObject):
    def __init__(self, game: Game, vectors: List[Vector]):
        super().__init__(game, colour.GREEN, vectors)


class WallScreenObject(ScreenObject):
    def __init__(self, game: Game, vectors: List[Vector]):
        super().__init__(game, colour.BLACK, vectors)


class FruitScreenObject(ScreenObject):
    def __init__(self, game: Game, vectors: List[Vector]):
        super().__init__(game, colour.RED, vectors)
