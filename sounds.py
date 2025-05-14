import pygame
from pygame import mixer
import constants
import random

class Sound():
    def __init__(self):
        self.anouc = pygame.mixer.Sound("assets/audio/backround/anouc.mp3")
        self.attack = pygame.mixer.Sound("assets/audio/attack.mp3")
        self.win = pygame.mixer.Sound("assets/audio/endings/you_win.mp3")
        self.loose = pygame.mixer.Sound("assets/audio/endings/you_loose.wav")
        self.escape = pygame.mixer.Sound("assets/audio/endings/they_escape.mp3")
        self.eating = pygame.mixer.Sound(f"assets/audio/eating/eating.mp3")
        self.happy = []
        self.cough = []
        self.dying = []
        self.time = pygame.time.get_ticks()
        self.npc_sound_time = pygame.time.get_ticks()
        self.eat_time = pygame.time.get_ticks()
        self.unplayed = True
        self.annouc_cooldown = 0
        self.channel_anouc = pygame.mixer.Channel(0)
        self.channel_eating = pygame.mixer.Channel(1)
        self.channel_cough = pygame.mixer.Channel(2)
        self.channel_attack = pygame.mixer.Channel(3)
        self.channel_win = pygame.mixer.Channel(5)
        self.channel_loose = pygame.mixer.Channel(5)
        self.channel_esc = pygame.mixer.Channel(5)
        self.mixer = pygame.mixer.init()        

    def process_data(self):

        for i in range(4):
          sound = pygame.mixer.Sound(f"assets/audio/cough/{i+1}.wav")
          self.cough.append(sound)
          sound.set_volume(constants.COUCHE)

        for i in range(2):
          sound = pygame.mixer.Sound(f"assets/audio/dying/{i+1}.mp3")
          self.dying.append(sound)
          sound.set_volume(constants.DYING)

        
        self.attack.set_volume(constants.ATTACK)
        self.escape.set_volume(constants.ESCAPE)
        self.win.set_volume(constants.WIN)
        self.loose.set_volume(constants.LOOSE)


    def play_backround(self):
        pygame.mixer.music.load("assets/audio/backround/backround.mp3")
        pygame.mixer.music.set_volume(constants.BACKROUND)
        pygame.mixer.music.play(-1, 0.0, 5000)
        pygame.mixer.Channel(4)


    def play_anouc(self):
        now = pygame.time.get_ticks()
        if now - self.time > self.annouc_cooldown and not self.channel_anouc.get_busy():
            self.time = now
            self.anouc.set_volume(constants.ANOUC)
            self.anouc.play()
        self.annouc_cooldown = constants.ANOUC_COOLDOWN

    def play_final_sound(self, sound):
        if self.unplayed and not self.channel_win.get_busy():
            sound.play()
            self.unplayed = False

    def play_cough_sounds(self):
        now = pygame.time.get_ticks()
        if now - self.npc_sound_time > random.randint(100, 700) and not self.channel_cough.get_busy():
            self.npc_sound_time = now
            random_i = random.randint(0, len(self.cough) - 1)
            self.cough[random_i].play()


    def play_eat_sound(self):
        now = pygame.time.get_ticks()
        if now - self.eat_time > random.randint(100, 700) and not self.channel_eating.get_busy():
            self.eat_time = now
            self.eating.play()

    def stop_music(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
