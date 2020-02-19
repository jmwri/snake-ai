from __future__ import annotations

import pygame
from pygame.locals import QUIT, KEYDOWN

from game.solvers.abstract import AbstractModel
from game.scores import ScoreLogger
from game.environment.environment import Environment


class Trainer:
    def __init__(
            self, game_model: AbstractModel, horizontal_tiles: int,
            vertical_tiles: int, score_logger: ScoreLogger):
        self.model = game_model
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self._score_logger = score_logger

        self.environment = Environment(
            width=self.horizontal_tiles,
            height=self.vertical_tiles
        )
        self.environment.init_wall()
        self.environment.init_fruit()
        self.environment.init_snake()

    def run_batch(self, batch_size: int):
        game_i = 0
        while game_i < batch_size:
            if not self.tick():
                game_i += 1

    def tick(self) -> bool:
        action = self.model.next_action(self.environment)
        terminal = not self.environment.step(action)
        self.model.train_after_action(self.environment, terminal)
        if terminal or self.environment.won():
            self.snake_died()
            return False

        return True

    def snake_died(self):
        self._score_logger.log_score(
            self.model.short_name,
            self.environment.reward()
        )
        self.model.reset()
        self.environment.init_snake()

    def _handle_user_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                self.model.user_input(event)
        return True
