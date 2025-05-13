import pygame
import character
from world import World
import constants
from sounds import Sound

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
        self.time_font = pygame.font.Font(None, constants.TIME_TEXT_FONT_SIZE)
        self.intro_font = pygame.font.Font(None, constants.INTRO_TEXT_FONT_SIZE)
        self.intro_font_outline = pygame.font.Font(None, constants.INTRO_TEXT_FONT_SIZE)

    def setup(self):

        self.world1 = World('Store1')
        self.world1.process_data() 

        self.world2 = World('Store')
        self.world1.process_data() 

        self.sounds = Sound()
        self.sounds.process_data()       

        self.hero = character.Player(300, 300, 4)

        self.npc_group = pygame.sprite.Group()

        for i in range(constants.NUMBER_OF_INFECTED_NPC):
            npc = character.Npc(2, self.world1.positions, 1, True)
            self.npc_group.add(npc)
            npc2 = character.Npc(2, self.world1.positions, 2, True)
            self.npc_group.add(npc2)


        for i in range(constants.NUMBER_OF_HEALTHY_NPC):
            npc = character.Npc(2, self.world1.positions, 1, False)
            self.npc_group.add(npc)
            npc2 = character.Npc(2, self.world1.positions, 2, False)
            self.npc_group.add(npc2)


        self.screen_scroll = [0, 0]
        self.reset_time()
        character.Npc.count_infected = 0
        character.Npc.count_innocent = 0



    def npc_count(self, num_of_infected):
        all_infected_killed = (num_of_infected * 2 == character.Npc.count_infected)
        one_innocent_killed = character.Npc.count_innocent >= 1
        if num_of_infected == 0:
            all_infected_killed = False
        return one_innocent_killed, all_infected_killed
    
    
    def reset_time(self):
        self.game_time = pygame.time.get_ticks()

    def intro_images_load(self):
        intro_images = []

        for i in range(13):
            img = pygame.image.load(f'assets/bg/intro/{i + 1}.png').convert_alpha()
            intro_images.append(img)
        return intro_images

    def intro_animation(self):
        now = pygame.time.get_ticks()
        frame_time = constants.INTRO_ANIMATION_FRAME_TIME

        if now - self.last_frame > frame_time:
            self.last_frame = now
            if self.current_intro_frame < len(self.intro_images) - 1:
                self.current_intro_frame += 1

        img = self.intro_images[self.current_intro_frame]
        text = constants.INTRO_SLIDES_TEXT[self.current_intro_frame]
        main_text = self.intro_font.render(text, True, (255, 255, 255))
        outline = self.intro_font_outline.render(text, True, (0, 0, 0))

        text_x = constants.SCREEN_WIDTH // 2 - main_text.get_width() // 2
        text_y = 600

        self.screen.blit(img.convert_alpha(), (0, 0))

        for dx in [-constants.TEXT_OUTLINE_THICKNESS, 0, constants.TEXT_OUTLINE_THICKNESS]:
            for dy in [-constants.TEXT_OUTLINE_THICKNESS, 0, constants.TEXT_OUTLINE_THICKNESS]:
                self.screen.blit(outline, (text_x + dx, text_y + dy))
        self.screen.blit(main_text, (text_x, text_y))