from game.models.abstract import AbstractModel
from game.environment import action as act
from game.environment.environment import Environment
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.event import Event


class HumanSolver(AbstractModel):
    def __init__(self):
        super().__init__("Human", "human", "hu")
        self._action = act.NONE

    def next_action(self, environment: Environment) -> act.Action:
        # If there was no user input, return the current action of the snake
        if self._action is act.NONE:
            return environment.snake.action
        # If the user tried to go backwards, ignore it
        backward_action = self._action.vector.is_reverse(
            environment.snake.action.vector
        )
        return environment.snake.action if backward_action else self._action

    def user_input(self, event: Event):
        if event.key == K_UP:
            self._action = act.UP
        elif event.key == K_DOWN:
            self._action = act.DOWN
        elif event.key == K_LEFT:
            self._action = act.LEFT
        elif event.key == K_RIGHT:
            self._action = act.RIGHT
        else:
            self._action = act.NONE

    def reset(self):
        self._action = act.NONE
