import argparse
import random

import pygame

from game.game import Game
from game import constants
from game.solvers.breadth_first_search_longest import \
    BreadthFirstSearchLongestPath
from game.solvers.breadth_first_search_shortest import \
    BreadthFirstSearchShortestPath
from game.solvers.deep_q_learning import DeepQLearning
from game.solvers.hamiltonian_cycle import HamiltonianCycle
from game.solvers.human import HumanSolver
from game.scores import ScoreLogger
from game.trainer import Trainer

models = [
    HumanSolver(),
    BreadthFirstSearchShortestPath(),
    BreadthFirstSearchLongestPath(),
    HamiltonianCycle(),
    DeepQLearning(),
]


def args():
    parser = argparse.ArgumentParser()
    for model in models:
        parser.add_argument(
            "-" + model.abbreviation,
            "--" + model.short_name,
            help=model.long_name,
            action="store_true"
        )

    parser.add_argument("-fps", "--fps", type=int, default=constants.FPS,
                        help="Frames per second")

    parser.add_argument("-t", "--train",
                        help="Train the model", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(constants.NAME)

    args = args()

    selected_game_model = random.choice(models)
    for game_model in models:
        if game_model.short_name in args and vars(args)[game_model.short_name]:
            selected_game_model = game_model

    score_logger = ScoreLogger(constants.SCORES_PATH)

    if args.train:
        g = Trainer(
            selected_game_model,
            constants.HORZ_TILES,
            constants.VERT_TILES,
            score_logger
        )
    else:
        g = Game(
            game_model=selected_game_model,
            fps=args.fps,
            horizontal_tiles=constants.HORZ_TILES,
            vertical_tiles=constants.VERT_TILES,
            screen_width=constants.SCREEN_WIDTH,
            screen_height=constants.SCREEN_HEIGHT,
            score_logger=score_logger,
            font=constants.FONT,
            screen_depth=constants.SCREEN_DEPTH
        )

    play_game = True
    while play_game:
        play_game = g.tick()
    pygame.quit()
