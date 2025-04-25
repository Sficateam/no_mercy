import pygame
import character
from world import World
import constants

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("No mercy!")

        self.surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    def setup(self):

        self.hero = character.Player(200, 200, 4)
        self.npc = character.Npc(250, 250, 2)

        self.world = World()
        self.world.process_data()

        self.screen_scroll = [0, 0]
