import pygame
import math

from graphics.utils import *
from graphics.settings import *

from engine.game import *
from graphics.graphics import *

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hex")

game = Game()
interface = GraphicsGame(game, screen)

interface.mainloop()

pygame.quit()
