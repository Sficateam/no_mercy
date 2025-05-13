import pygame
from pygame import mixer
import constants

class Sound():
    def __init__(self):
        self.anouc = pygame.mixer.Sound("assets/audio/backround/anouc.mp3")
        self.attack = pygame.mixer.Sound("assets/audio/attack.mp3")
        self.win = pygame.mixer.Sound("assets/audio/endings/you_win.mp3")
        self.loose = pygame.mixer.Sound("assets/audio/endings/you_loose.wav")
        self.escape = pygame.mixer.Sound("assets/audio/endings/they_escape.mp3")
        self.eating = [pygame.mixer.Sound(f"assets/audio/eating/eating.mp3")]
        self.happy = []
        self.cough = []
        self.dying = []
        self.time = pygame.time.get_ticks()
        self.cooldown = constants.ANOUC_COOLDOWN
        self.sound_list = []
        self.unplayed = True

    def process_data(self):
        pygame.mixer.init()

        self.eating[0].set_volume(constants.EAT)

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

          self.sound_list.append(self.cough)
          self.sound_list.append(self.eating)

    def play_backround(self):
        pygame.mixer.music.load("assets/audio/backround/backround.mp3")
        pygame.mixer.music.set_volume(constants.BACKROUND)
        pygame.mixer.music.play(-1, 0.0, 5000)


    def play_anouc(self):
        now = pygame.time.get_ticks()
        # pokud cooldown uplynul a zvuk nehraje
        if now - self.time > self.cooldown and self.anouc.get_num_channels() == 0:
            self.time = now
            self.anouc.set_volume(constants.ANOUC)
            self.anouc.play()

    def play_sound(self, sound):
        if self.unplayed:
            sound.play()
            self.unplayed = False