from abc import ABC, abstractmethod

from pygame.event import Event
from game.environment.environment import Environment
from game.environment import action as act


class AbstractModel(ABC):
    def __init__(self, long_name: str, short_name: str, abbreviation: str):
        self.long_name = long_name
        self.short_name = short_name
        self.abbreviation = abbreviation

    @abstractmethod
    def next_action(self, environment: Environment) -> act.Action:
        """
        Evaluate the current environment and any user input.
        :return: The action to be performed next
        """
        pass

    def after_action(self, environment: Environment, terminal: bool):
        """
        Evaluate the environment after our last action
        """
        pass

    def user_input(self, event: Event):
        """
        Key presses will be detected here.
        Store them in the model for later use.
        """
        pass

    def reset(self):
        """
        Called on snake death.
        """
        pass
