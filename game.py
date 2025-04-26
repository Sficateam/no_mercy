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
        self.intro_images = self.intro_images_load()
        self.last_frame = pygame.time.get_ticks()
        self.current_intro_frame = 0
        self.font = pygame.font.Font(None, 36)

    def setup(self):

        self.world = World()
        self.world.process_data()        

        self.hero = character.Player(300, 300, 4)

        self.npc_group = pygame.sprite.Group()
        self.num_of_infected = 0

        for i in range(constants.NUMBER_OF_NPC):
            npc = character.Npc(2, self.world.positions)
            self.npc_group.add(npc)
            if npc.infected:
                self.num_of_infected += 1

        for npc in self.npc_group:
            print(len((npc.animation_list[0])))

        self.screen_scroll = [0, 0]
        self.reset_time()
        character.Npc.count_infected = 0
        character.Npc.count_innocent = 0


    def npc_count(self, num_of_infected):
        all_infected_killed = (num_of_infected == character.Npc.count_infected)
        if num_of_infected == 0:
            all_infected_killed = False
        return character.Npc.count_innocent, all_infected_killed
    
    def reset_time(self):
        self.game_time = pygame.time.get_ticks()

    def intro_images_load(self):
        intro_images = []

        for i in range(5):
            img = pygame.image.load(f'assets/bg/intro/First-comics-00{i + 1}.png').convert_alpha()
            intro_images.append(img)
        return intro_images

    def intro_animation(self):
        now = pygame.time.get_ticks()
        frame_time = 3000

        if now - self.last_frame > frame_time:
            self.last_frame = now
            if self.current_intro_frame < len(self.intro_images) - 1:
                self.current_intro_frame += 1

        img = self.intro_images[self.current_intro_frame]
        text = self.font.render(f'Zde bude text', True, (0, 0, 0))
        self.screen.blit(img.convert_alpha(), (0, 0))
        self.screen.blit(text, ((self.screen.get_width() // 2) - text.get_width(), 600))