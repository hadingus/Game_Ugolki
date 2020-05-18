from abc import ABC
from abc import abstractmethod
import pygame.event


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        ...


class Handler(ABC):
    @abstractmethod
    def handle(self, event: pygame.event):
        ...
