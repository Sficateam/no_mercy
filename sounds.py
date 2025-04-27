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
        self.cooldown = constants.ANOUC
        self.sound_list = []

    def process_data(self):
        mixer.init()

        for i in range(4):
          sound = pygame.mixer.Sound(f"assets/audio/cough/{i+1}.wav")
          self.cough.append(sound)
          sound.set_volume(0.3)

        for i in range(2):
          sound = pygame.mixer.Sound(f"assets/audio/dying/{i+1}.mp3")
          self.dying.append(sound)
          sound.set_volume(0.3)

          self.attack.set_volume(0.3)
          self.escape.set_volume(0.3)
          self.win.set_volume(0.3)
          self.loose.set_volume(0.3)

          self.sound_list.append(self.cough)
          self.sound_list.append(self.eating)


    def play(self):
        pygame.mixer.music.load("assets/audio/backround/backround.mp3")
        pygame.mixer.music.play(-1, 0.0, 5000)

        now = pygame.time.get_ticks()
        if now - self.time > self.cooldown:
          self.time = pygame.time.get_ticks()
          pygame.mixer.music.load("assets/audio/backround/anouc.mp3")
          pygame.mixer.music.play(-1, 0.0, 5000)