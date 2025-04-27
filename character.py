import pygame
from abc import ABC, abstractmethod
import constants
import random
import os

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
        self.fight = self.animation_load([], path = 'assets/character/attack/Killing2-export')
        self.last_animation = pygame.time.get_ticks()
        self.frame = 0
        self.walking = False

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def input_keys(self, keys):
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:
                self.direction.x = -1
                self.flip = True
        if keys[pygame.K_d]:
                self.direction.x = 1
                self.flip = False
        if keys[pygame.K_s]:
                self.direction.y = 1
        if keys[pygame.K_w]:
                self.direction.y = -1

    def input_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attacking = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.attacking = False

    
    def move(self, obstacle_list, npc_group):
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

        for npc in npc_group:
            if self.in_collision(npc):
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
        now = pygame.time.get_ticks()

        if self.attacking:
            self.do_animation(self.fight, constants.ATTACK_COOLDOWN)

        if self.walking:
            self.do_animation(self.walk, constants.MOVE_COOLDOWN)

        self.do_animation(self.idle, constants.IDDLE_COOLDOWN)

    
    def update(self, keys, obstacle_list, events, npc):

        self.update_animations()
        self.input_keys(keys)

        for event in events:
            self.input_event(event)

        new_scroll = None
        

        if new_scroll:
            return new_scroll
        return self.move(obstacle_list, npc)
    
    def attack(self, npc_group, sound):
        for npc in npc_group:
            if self.attacking and self.in_collision(npc.bigger_rect):

                sound.play()
                if npc.infected and not npc.is_dead:
                    Npc.count_infected += 1
                    print('infected kill +1')
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
        # self.img_death = pygame.image.load(f'assets/world/shroom1.png').convert_alpha()
        self.walk = self.animation_load([], path = f'assets/character/npc/{self.type}/Walking')
        self.death = self.animation_load([], path = f'assets/character/npc/{self.type}/death/healthy/')
        self.flip = False
        self.direction = pygame.Vector2(0, 0)
        self.rect = self.get_random_rect(position_list)
        self.bigger_rect = self.rect.inflate(92, 92)
        self.x = self.bigger_rect.x
        self.y = self.bigger_rect.y
        self.is_dead = False
        self.movement = False
        self.infected = infected
        self.last_move = pygame.time.get_ticks()
        self.frame = 0
        self.last_animation = pygame.time.get_ticks()
        self.animation_list = self.load_animation_list()
        self.random_cooldown = random.randint(constants.ANIMATION_MIN_TIME, constants.ANIMATION_MAX_TIME)
        self.actual_list = self.animation_list[1][1]
        self.animation_time = True


    def draw(self, screen):
        # if self.is_dead:
        #     self.do_animation()
        # else:
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.bigger_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.bigger_rect, 2)

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


    def update(self, obstacles, screen_scroll):
        self.move(obstacles, screen_scroll)
        self.get_animation()
        now = pygame.time.get_ticks()
        if self.movement:
            if now - self.last_animation > 150:    
                self.last_animation = pygame.time.get_ticks()
                if self.frame >= len(self.walk):
                    self.frame = 0
                self.img = self.walk[self.frame]
                self.frame += 1
        if self.is_dead:
            self.do_animation_once(self.death, constants.NPC_ANIMATION)
            self.flip = False

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

        
    def get_animation(self):

        #if self.movement == False:

        if self.animation_time:
            a = random.randint(0, 10)
            if self.infected and a > constants.INFECTED_COEFICIENT:
                self.actual_list = self.animation_list[0][random.randint(0, len(self.animation_list[0]) - 1)]
            else:
                self.actual_list = self.animation_list[1][random.randint(0, len(self.animation_list[1]) - 1)]
            self.animation_time = False

        now = pygame.time.get_ticks()
        if now - self.last_animation > 200:
            self.last_animation = pygame.time.get_ticks()
            if self.frame >= len(self.actual_list):
                self.frame = 0
                self.animation_time = True
                self.movement = True
            self.img = self.actual_list[self.frame]
            self.frame += 1
