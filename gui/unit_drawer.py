from gui.components import Drawable
from gui import colors
import pygame
import pygame.gfxdraw


class DefaultDrawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_unit(self, type, active, position, size):
        center = position[0] + size // 2, position[1] + size // 2
        color_table = [[colors.RED, colors.DARK_RED],
                       [colors.GREEN, colors.DARK_GREEN]]
        figure_colour = color_table[type][active]
        pygame.gfxdraw.aacircle(self.screen, center[0], center[1], size // 2 - 4, figure_colour)
        pygame.gfxdraw.filled_circle(self.screen, center[0], center[1], size // 2 - 4, figure_colour)
