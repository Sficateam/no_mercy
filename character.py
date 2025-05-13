import pygame
from abc import ABC, abstractmethod
import constants
import random
import os
import threading

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
    
    def move(self, obstacle_list, npc_group):

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
        return self.move(obstacle_list, npc)
    
    def attack(self, npc_group, sound):
        for npc in npc_group:
            if self.attacking and self.in_collision(npc.bigger_rect):
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
        self.walk = self.animation_load([], path = f'assets/character/npc/{self.type}/Walking')
        self.flip = False
        self.direction = pygame.Vector2(0, 0)
        self.rect = self.get_random_rect(position_list)
        self.bigger_rect = self.rect
        self.x = self.bigger_rect.x
        self.y = self.bigger_rect.y
        self.is_dead = False
        self.movement = False
        self.infected = infected
        self.death = self.death_animation_load()
        self.death_sound_unplayed = True
        self.last_move = pygame.time.get_ticks()
        self.frame = 0
        self.last_animation = pygame.time.get_ticks()
        self.animation_list = self.load_animation_list()
        self.random_cooldown = random.randint(constants.ANIMATION_MIN_TIME, constants.ANIMATION_MAX_TIME)
        self.actual_list = self.animation_list[1][1]
        self.animation_time = True


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.bigger_rect)

    def move(self, obstacle_list, screen_scroll):
        self.now = pygame.time.get_ticks()

        if self.now - self.last_move > random.randint(constants.ANIMATION_MIN_TIME, constants.ANIMATION_MAX_TIME):
            self.last_move = pygame.time.get_ticks()

            random_move = random.randint(0, 10)
            if self.is_dead:
                self.movement = False
            else:
                self.movement = random_move == 0

            self.direction = pygame.Vector2(0, 0)
            if random.randint(0, 1):
                self.direction.x = random.choice([-1, 1])
                if self.direction.x == -1:
                    self.flip = True
                elif self.direction.x == 1:
                    self.flip = False
            if random.randint(0, 1):
                self.direction.y = random.choice([-1, 1])

        if self.movement:
            prev_x = self.x
            prev_y = self.y

            self.x += self.direction.x * self.speed
            self.bigger_rect.centerx = int(self.x)
            self.rect.centerx = int(self.x)

            for tile in obstacle_list:
                if self.in_collision(tile):
                    self.x = prev_x
                    self.bigger_rect.centerx = int(self.x)
                    self.rect.centerx = int(self.x)

            self.y += self.direction.y * self.speed
            self.bigger_rect.centery = int(self.y)
            self.rect.centery = int(self.y)

            for tile in obstacle_list:
                if self.in_collision(tile):
                    self.y = prev_y
                    self.bigger_rect.centery = int(self.y)
                    self.rect.centery = int(self.y)

            if self.direction.length_squared() > 0:
                self.direction = self.direction.normalize()

        self.x += screen_scroll[0]
        self.y += screen_scroll[1]
        self.bigger_rect.center = (int(self.x), int(self.y))
        self.rect.center = (int(self.x), int(self.y))


    def update(self, obstacles, screen_scroll, sound_list, death_sound_list):
        self.move(obstacles, screen_scroll)
        self.get_animation(sound_list)
        now = pygame.time.get_ticks()
        if self.movement:
            if now - self.last_animation > 150:    
                self.last_animation = pygame.time.get_ticks()
                if self.frame >= len(self.walk):
                    self.frame = 0
                self.img = self.walk[self.frame]
                self.frame += 1
        if self.is_dead:
            self.do_animation_once(self.death, constants.DEATH_COOLDOWN)
            self.flip = False
            if self.death_sound_unplayed:
                sound = death_sound_list[random.randint(0, len(death_sound_list) -1)]
                threading.Timer(0.3, sound.play).start()
                self.death_sound_unplayed = False

    def get_postion(self, position_list):
        i = random.randint(0, len(position_list) - 1)
        return position_list[i]
    
    def get_random_rect(self, position_list):
        index = random.randint(0, len(position_list) - 1)
        return position_list[index].copy()
    
    def get_virus(self):
        i = random.randint(0, 1)
        if i == 0:
            return True
        else:
            return False
        
    def death_animation_load(self):
        if self.infected:
            return self.animation_load([], path = f'assets/character/npc/{self.type}/death/infected/')
        else:
            return self.animation_load([], path = f'assets/character/npc/{self.type}/death/healthy/')
    
    def load_animation_list(self):
        infected = []
        healthy = []
        animation_list = []

        folders_healthy = 0
        folders_infected = 0

        for entry in os.scandir(f'assets/character/npc/{self.type}/healthy'):
            if entry.is_dir():
                folders_healthy += 1
        
        for entry in os.scandir(f'assets/character/npc/{self.type}/infected'):
            if entry.is_dir():
                folders_infected += 1

        for i in range(folders_healthy):
            list = self.animation_load([], f'assets/character/npc/{self.type}/healthy/{i+1}/')
            healthy.append(list)


        for i in range(folders_infected):
            list = self.animation_load([], f'assets/character/npc/{self.type}/infected/{i+1}/')
            infected.append(list)

        animation_list.append(infected)
        animation_list.append(healthy)

        return animation_list

        
    def get_animation(self, sound_list):

        index = -1

        if self.animation_time:
            a = random.randint(0, 10)
            index = 0
            if self.infected and a > constants.INFECTED_COEFICIENT:
                index = random.randint(0, len(self.animation_list[0]) - 1)
                self.actual_list = self.animation_list[0][index]
            else:
                index = random.randint(0, len(self.animation_list[1]) - 1)
                self.actual_list = self.animation_list[1][index]
            self.animation_time = False


        if len(sound_list[index+1]) > 0:
            if index == 1 or index == 2:
                random_i = random.randint(0, len(sound_list[index]) - 1)
                sound = sound_list[index][random_i]
                sound.play()

        now = pygame.time.get_ticks()
        if now - self.last_animation > 200:
            self.last_animation = pygame.time.get_ticks()
            if self.frame >= len(self.actual_list):
                self.frame = 0
                self.animation_time = True
                self.movement = True
            self.img = self.actual_list[self.frame]
            self.frame += 1
