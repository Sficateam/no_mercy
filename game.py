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
        self.game_time = pygame.time.get_ticks()

    def setup(self):

        self.world = World()
        self.world.process_data()        

        self.hero = character.Player(300, 300, 4)

        self.npc_group = pygame.sprite.Group()
        self.num_of_infected = 1

        start_npc = character.Npc(2, self.world.positions)
        start_npc.infected = True
        self.npc_group.add(start_npc)

        for i in range(constants.NUMBER_OF_NPC):
            npc = character.Npc(2, self.world.positions)
            self.npc_group.add(npc)
            if npc.infected:
                self.num_of_infected += 1

        self.screen_scroll = [0, 0]
        self.reset_time()
        character.Npc.count_infected = 0
        character.Npc.count_innocent = 0


    def npc_count(self, num_of_infected):
        all_infected_killed = (num_of_infected == character.Npc.count_infected)
        return character.Npc.count_innocent, all_infected_killed
    
    def reset_time(self):
        self.game_time = pygame.time.get_ticks()