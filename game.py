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

        self.world = World()
        self.world.process_data()        

        self.hero = character.Player(300, 300, 4)

        self.npc_group = pygame.sprite.Group()
        self.num_of_infected = 0
        for i in range(constants.NUMBER_OF_NPC):
            npc = character.Npc(2, self.world.positions)
            self.npc_group.add(npc)
            print(npc.infected)
            if npc.infected:
                self.num_of_infected += 1

        print(self.num_of_infected)
        self.screen_scroll = [0, 0]

    def npc_count(self, num_of_infected):
        all_infected_killed = (num_of_infected == character.Npc.count_infected)
        return character.Npc.count_innocent, all_infected_killed