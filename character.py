import pygame
from abc import ABC, abstractmethod
import constants
import random
import os
import threading
import math

class Character(ABC):
    def __init__(self, speed):

        self.speed = speed

    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def update(self):
        pass

    def in_collision(self, object):
        self.rect.x += constants.X_SHIFT
        self.rect.width -= constants.WIDTH_SCALE
        temp = self.rect.colliderect(object)
        self.rect.x -= constants.X_SHIFT
        self.rect.width += constants.WIDTH_SCALE

        return temp
    
    def animation_load(self, list, path):
        i = 1
        while True:
            filename = f'{path}{i}.png'
            if os.path.exists(filename):
                img = pygame.image.load(filename).convert_alpha()
                list.append(img)
                i += 1
            else:
                break
        return list
    
    def do_animation(self, animation_list, cooldown):
        now = pygame.time.get_ticks()
        if now - self.last_animation > cooldown:
            self.last_animation = pygame.time.get_ticks()
            if self.frame >= len(animation_list):
                self.frame = 0
            self.img = animation_list[self.frame]
            self.frame += 1

    def do_animation_once(self, animation_list, cooldown):
        now = pygame.time.get_ticks()
        if now - self.last_animation > cooldown:
            self.last_animation = pygame.time.get_ticks()
            if self.frame >= len(animation_list):
                self.frame = len(animation_list) - 1
            self.img = animation_list[self.frame]
            self.frame += 1


class Player(Character, pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        Character.__init__(self, speed)
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.img = pygame.image.load(f'assets/character/idle/wiggling1.png').convert_alpha()
        self.direction = pygame.Vector2(0, 0)
        self.attacking = False
        self.flip = False
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.idle = self.animation_load([], path = 'assets/character/idle/wiggling')
        self.walk = self.animation_load([], path = 'assets/character/walk/Walking')
        self.fight = self.animation_load([], path = 'assets/character/attack/')
        self.last_animation = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.frame = 0
        self.walking = False
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)


    def input_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attacking = True
            if event.key == pygame.K_a:
                self.moving_left = True
                self.flip = True 
            if event.key == pygame.K_d:
                self.moving_right = True
                self.flip = False
            if event.key == pygame.K_s:
                self.moving_down = True
            if event.key == pygame.K_w:
                self.moving_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.attacking = False
            if event.key == pygame.K_a:
                self.moving_left = False
            if event.key == pygame.K_d:
                self.moving_right = False
            if event.key == pygame.K_s:
                self.moving_down = False
            if event.key == pygame.K_w:
                self.moving_up = False


    def update_direction(self):
        self.direction = pygame.Vector2(0, 0)

        if self.moving_up:
            self.direction.y = -1
        if self.moving_down:
            self.direction.y = 1
        if self.moving_left:
            self.direction.x = -1
        if self.moving_right:
            self.direction.x = 1
    
    def move(self, obstacle_list):

        self.update_direction()
            
        screen_scroll = [0, 0]
        self.walking = False

        prev_x = self.x
        prev_y = self.y

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.x += self.direction.x * self.speed
        self.rect.centerx = int(self.x)
        for tile in obstacle_list:
            if self.in_collision(tile):
                self.x = prev_x
                self.rect.centerx = int(self.x)


        self.y += self.direction.y * self.speed
        self.rect.centery = int(self.y)
        for tile in obstacle_list:
            if self.in_collision(tile):
                self.y = prev_y
                self.rect.centery = int(self.y)

        if self.direction.length_squared() > 0:
            self.walking = True
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = -self.speed
                self.x -= self.speed
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = self.speed
                self.x += self.speed

            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = -self.speed
                self.y -= self.speed
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = self.speed
                self.y += self.speed

        return screen_scroll
    
    def update_animations(self):

        if self.attacking:
            self.do_animation(self.fight, constants.ATTACK_COOLDOWN)

        if self.walking:
            self.do_animation(self.walk, constants.MOVE_COOLDOWN)

        self.do_animation(self.idle, constants.IDDLE_COOLDOWN)

    
    def update(self, obstacle_list, events, npc):

        self.update_animations()

        for event in events:
            self.input_event(event)

        new_scroll = None
        

        if new_scroll:
            return new_scroll
        return self.move(obstacle_list)
    
    def attack(self, npc_group, sound):
        for npc in npc_group:
            dist = math.sqrt(((self.rect.centerx - npc.rect.centerx) ** 2) + ((self.rect.centery - npc.rect.centery) ** 2))
            if self.attacking and self.in_collision(npc.rect) and dist < 80:
                if True:
                    self.last_attack = pygame.time.get_ticks()
                    sound.play()
                    if npc.infected and not npc.is_dead:
                        Npc.count_infected += 1
                    elif not npc.infected and not npc.is_dead:
                        Npc.count_innocent += 1           
                    npc.is_dead = True
                if self.flip and self.rect.left < npc.rect.right and self.rect.centerx > npc.rect.centerx:
                    self.last_attack = pygame.time.get_ticks()
                    sound.play()
                    if npc.infected and not npc.is_dead:
                        Npc.count_infected += 1
                    elif not npc.infected and not npc.is_dead:
                        Npc.count_innocent += 1           
                    npc.is_dead = True

class Npc(Character, pygame.sprite.Sprite):

    count_innocent = 0
    count_infected = 0

    def __init__(self, speed, position_list, type, infected):
        Character.__init__(self, speed)
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.img = pygame.image.load(f'assets/character/npc/{self.type}/Walking1.png').convert_alpha()
        self.walk_animation_list = self.animation_load([], path = f'assets/character/npc/{self.type}/Walking')
        self.flip = False
        self.direction = pygame.Vector2(0, 0)
        self.rect_for_position = self.get_random_rect(position_list)
        self.rect = self.img.get_rect()
        self.x = self.rect_for_position.x
        self.y = self.rect_for_position.y
        self.is_dead = False
        self.infected = infected
        self.death = self.death_animation_load()
        self.death_sound_unplayed = True
        self.last_move = pygame.time.get_ticks()
        self.frame = 0
        self.last_animation = pygame.time.get_ticks()
        self.animation_list = self.load_animation_list()
        self.actual_list = self.animation_list[1][1]
        self.random_cooldown = 0
        self.last_sound = pygame.time.get_ticks()


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

    def move(self, obstacle_list):
        self.now = pygame.time.get_ticks()

        if self.now - self.last_move > self.random_cooldown:
            self.last_move = pygame.time.get_ticks()

            self.direction = pygame.Vector2(0, 0)
            self.direction.x = random.randint(-1, 1)
            self.direction.y = random.randint(-1, 1)
            if self.direction.x == -1:
                self.flip = True
            elif self.direction.x == 1:
                self.flip = False

            self.random_cooldown = random.randint(constants.ANIMATION_MIN_TIME, constants.ANIMATION_MAX_TIME)
            
        prev_x = self.x
        prev_y = self.y

        self.x += self.direction.x * self.speed
        self.rect.centerx = int(self.x)

        for tile in obstacle_list:
            if self.in_collision(tile):
                self.x = prev_x
                self.rect.centerx = int(self.x)
                self.direction.x = 0
                self.direction.y = 0
                self.random_cooldown = random.randint(0,2000)

        self.y += self.direction.y * self.speed
        self.rect.centery = int(self.y)

        for tile in obstacle_list:
            if self.in_collision(tile):
                self.y = prev_y
                self.rect.centery = int(self.y)
                self.direction.x = 0
                self.direction.y = 0
                self.random_cooldown = random.randint(0,2000)

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()


    def update(self, obstacles, screen_scroll, death_sound_list):
        if self.is_dead:
            self.do_animation_once(self.death, constants.DEATH_COOLDOWN)
            self.flip = False
            if self.death_sound_unplayed:
                sound = death_sound_list[random.randint(0, len(death_sound_list) -1)]
                threading.Timer(0.3, sound.play).start()
                self.death_sound_unplayed = False
        else:
            k = random.random()
            if k < constants.MOVE_COEFICIENT:
                self.move(obstacles)
                if self.direction.x == 0:
                    self.flip = False
                now = pygame.time.get_ticks()
                if self.direction.length_squared() > 0:
                    if now - self.last_animation > 150:    
                        self.last_animation = pygame.time.get_ticks()
                        if self.frame >= len(self.walk_animation_list):
                            self.frame = 0
                        self.img = self.walk_animation_list[self.frame]
                        self.frame += 1
            else:
                self.get_animation()



        self.x += screen_scroll[0]
        self.y += screen_scroll[1]
        self.rect.center = (int(self.x), int(self.y))

    
    def get_random_rect(self, position_list):
        index = random.randint(0, len(position_list) - 1)
        return position_list[index].copy()
    
        
    def death_animation_load(self):
        if self.infected:
            return self.animation_load([], path = f'assets/character/npc/{self.type}/death/infected/')
        else:
            return self.animation_load([], path = f'assets/character/npc/{self.type}/death/healthy/')
    
    def load_animation_list(self):
        animation_list = []

        folder_names = ['infected', 'healthy']

        for name in folder_names:
            folders_no = 0
            folder = []

            for entry in os.scandir(f'assets/character/npc/{self.type}/{name}'):
                if entry.is_dir():
                    folders_no += 1
        
            for i in range(folders_no):
                list = self.animation_load([], f'assets/character/npc/{self.type}/{name}/{i+1}/')
                folder.append(list)

            animation_list.append(folder)

        return animation_list

        
    def get_animation(self):

        index = -1

        a = random.random()
        index = 0
        if self.infected and a < constants.INCECTED_ANIMATION_COEFICIENT:
            index = random.randint(0, len(self.animation_list[0]) - 1)
            self.actual_list = self.animation_list[0][index]
        else:
            index = random.randint(0, len(self.animation_list[1]) - 1)
            self.actual_list = self.animation_list[1][index]

        now = pygame.time.get_ticks()
        if now - self.last_animation > 200:
            self.last_animation = pygame.time.get_ticks()
            if self.frame >= len(self.actual_list):
                self.frame = 0
            self.img = self.actual_list[self.frame]
            self.frame += 1
