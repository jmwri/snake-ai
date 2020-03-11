from __future__ import annotations
from typing import List

import pygame
from pygame.surface import Surface
from pygame.locals import QUIT, KEYDOWN

from game import colour
from game.solvers.abstract import AbstractModel
from game.scores import ScoreLogger
from game.screen_object import SnakeScreenObject, FruitScreenObject, \
    WallScreenObject
from game.vector import Vector
from game.environment.environment import Environment


class Game:
    def __init__(
            self, game_model: AbstractModel, fps: int, horizontal_tiles: int,
            vertical_tiles: int, screen_width: int, screen_height: int,
            score_logger: ScoreLogger, font: str, screen_depth: int
    ):
        self.clock = pygame.time.Clock()
        self.model = game_model
        self.fps = fps
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height,),
            0,
            screen_depth
        )
        self.surface = pygame.Surface(self.screen.get_size())
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self.tile_width = int(screen_width / horizontal_tiles)
        self.tile_height = int(screen_height / vertical_tiles)
        self._score_logger = score_logger
        self._font = font

        self.environment = Environment(
            width=self.horizontal_tiles,
            height=self.vertical_tiles
        )
        self.environment.init_wall()
        self.environment.init_fruit()
        self.environment.init_snake()

        self.screen_objects = []

        normalised_wall_vectors = self._normalise_vectors(
            self.environment.wall.get_vectors()
        )
        self.wall = WallScreenObject(self, normalised_wall_vectors)
        self.screen_objects.append(self.wall)

        normalised_fruit_vectors = self._normalise_vectors(
            self.environment.fruit.get_vectors()
        )
        self.fruit = FruitScreenObject(self, normalised_fruit_vectors)
        self.screen_objects.append(self.fruit)

        normalised_snake_vectors = self._normalise_vectors(
            self.environment.snake.get_vectors()
        )
        self.snake = SnakeScreenObject(self, normalised_snake_vectors)
        self.screen_objects.append(self.snake)

    def tick(self) -> bool:
        continue_game = self._handle_user_input()
        if not continue_game:
            return False
        action = self.model.next_action(self.environment)
        reason = self.environment.step(action)
        if reason:
            print(f'died: {reason.reason}')
            self.snake_died()
        elif self.environment.won():
            print('won')
            self.snake_died()
        self._sync_screen_with_environment()
        self._draw_screen()
        self._display()

        self.clock.tick(self.fps)
        return True

    def snake_died(self):
        self._score_logger.log_score(
            self.model.short_name,
            self.environment.reward()
        )
        self.model.reset()
        self.environment.init_snake()

    def draw_tile(self, surface: Surface, col: colour.Colour, vector: Vector):
        rect = pygame.Rect(
            (vector.x, vector.y),
            (self.tile_width, self.tile_height)
        )
        pygame.draw.rect(surface, col, rect)

    def _draw_screen(self):
        self.surface.fill(colour.WHITE)
        for game_object in self.screen_objects:
            game_object.draw(self.surface)

        font = pygame.font.SysFont(self._font, int(self.tile_height / 1.3))
        score_text = font.render(
            str(self.environment.reward()),
            1,
            colour.WHITE
        )
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (self.screen_width / 2, self.tile_height / 2)
        self.surface.blit(score_text, score_text_rect)

        self.screen.blit(self.surface, (0, 0))

    def _sync_screen_with_environment(self):
        self.fruit.set_vectors(self._normalise_vectors(
            self.environment.fruit.get_vectors()
        ))
        self.snake.set_vectors(self._normalise_vectors(
            self.environment.snake.get_vectors()
        ))

    def _display(self):
        pygame.display.flip()
        pygame.display.update()

    def _normalise_vectors(self, vectors: List[Vector]) -> List[Vector]:
        return list(map(lambda x: self._normalise_vector(x), vectors))

    def _normalise_vector(self, vector: Vector) -> Vector:
        return Vector(
            vector.x * self.tile_width,
            vector.y * self.tile_height
        )

    def _handle_user_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                self.model.user_input(event)
        return True
