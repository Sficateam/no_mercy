import pygame
from abc import ABC, abstractmethod
import constants
import random

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


class Player(Character, pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        Character.__init__(self, speed)
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.img = pygame.image.load(f'assets/character/melon.png').convert_alpha()
        self.direction = pygame.Vector2(0, 0)
        self.attacking = False
        self.flip = False
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE, constants.TILE_SIZE)
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def input_keys(self, keys):
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:
                self.direction.x = -1
                self.flip = False
        if keys[pygame.K_d]:
                self.direction.x = 1
                self.flip = True
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

    def in_collision(self, object):
        self.rect.x += 40
        self.rect.width -= 80
        temp = self.rect.colliderect(object)
        self.rect.x -= 40
        self.rect.width += 80

        return temp
    
    def move(self, obstacle_list, npc_group):
        screen_scroll = [0, 0]

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        # Move in x direction
        self.x += self.direction.x * self.speed
        self.rect.centerx = int(self.x)
        for tile in obstacle_list:
            if self.in_collision(tile):
                if self.direction.x > 0:
                    self.rect.right = tile.left + 40
                elif self.direction.x < 0:
                    self.rect.left = tile.right - 40
                self.x = self.rect.centerx
        for npc in npc_group:
            if self.in_collision(npc):
                if self.direction.x > 0:
                    self.rect.right = npc.rect.left
                elif self.direction.x < 0:
                    self.rect.left = npc.rect.right
                self.x = self.rect.centerx

        # Move in y direction
        self.y += self.direction.y * self.speed
        self.rect.centery = int(self.y)
        for tile in obstacle_list:
            if self.in_collision(tile):
                if self.direction.y > 0:
                    self.rect.bottom = tile.top
                elif self.direction.y < 0:
                    self.rect.top = tile.bottom
                self.y = self.rect.centery
        for npc in npc_group:
            if self.in_collision(npc):
                if self.direction.y > 0:
                    self.rect.bottom = npc.rect.top
                elif self.direction.y < 0:
                    self.rect.top = npc.rect.bottom
                self.y = self.rect.centery
            
        #update scroll based on player position
        #move camera left and right
        if self.direction.length_squared() > 0:
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = -self.speed
                self.x -= self.speed
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = self.speed
                self.x += self.speed

            #move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = -self.speed
                self.y -= self.speed
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = self.speed
                self.y += self.speed
                    
        return screen_scroll
    
    def update(self, keys, obstacle_list, events, npc):
        self.input_keys(keys)

        for event in events:
            self.input_event(event)

        new_scroll = None
        

        if new_scroll:
            return new_scroll
        return self.move(obstacle_list, npc)
    
    def attack(self, npc_group):
        for npc in npc_group:
            if self.attacking and self.rect.colliderect(npc.rect):
                if npc.infected:
                    Npc.count_infected += 1
                    print('killed infected')
                else:
                    Npc.count_innocent += 1 
                    print('killed innocent')             
                npc.is_dead = True


class Npc(Character, pygame.sprite.Sprite):

    count_innocent = 0
    count_infected = 0

    def __init__(self, speed, position_list):
        Character.__init__(self, speed)
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f'assets/character/jaymeng.png').convert_alpha()
        self.img_death = pygame.image.load(f'assets/world/shroom1.png').convert_alpha()
        self.flip = False
        self.direction = pygame.Vector2(0, 0)
        self.rect = self.get_random_rect(position_list)
        self.x = self.rect.x
        self.y = self.rect.y
        self.is_dead = False
        self.movement = True
        self.infected = self.get_virus()
        self.last_move = pygame.time.get_ticks()

        self.last_frame = pygame.time.get_ticks()
        self.frame = 0
        self.last_animation = pygame.time.get_ticks()
        self.animation_list = self.load_animation_list()
        self.animation_unfinished = False
        self.random_cooldown = random.randint(2000, 10000)

    def in_collision(self, object):
        self.rect.x += 40
        self.rect.width -= 80
        temp = self.rect.colliderect(object)
        self.rect.x -= 40
        self.rect.width += 80

        return temp

    def draw(self, screen):
        if self.is_dead:
            screen.blit(pygame.transform.flip(self.img_death, False, False), self.rect)
            self.kill()
        else:
            screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def move(self, obstacle_list, screen_scroll):
        self.now = pygame.time.get_ticks()
        random_move_list = [0, 0, 0, 0]
        
        if self.now - self.last_move > random.randint(500, 5000):
            self.last_move = pygame.time.get_ticks()

            random_move = random.randint(0,1)
            if random_move == 0:
                self.movement = True
            else:
                self.movement = False

            
            for i in range(4):
                random_move_list[i] = random.randint(0,1)


        if self.movement:
            
            if random_move_list[0] == 1:
                    self.direction.x = -1
                    self.flip = False
            if random_move_list[1] == 1:
                    self.direction.x = 1
                    self.flip = True
            if random_move_list[2] == 1:
                    self.direction.y = 1
            if random_move_list[3] == 1:
                    self.direction.y = -1

            # Move in x direction        
            self.x += self.direction.x * self.speed
            
            self.rect.centerx = int(self.x)
            for tile in obstacle_list:
                if self.rect.colliderect(tile):
                    if self.direction.x > 0:
                        self.rect.right = tile.left
                    elif self.direction.x < 0:
                        self.rect.left = tile.right
                    self.x = self.rect.centerx


            # Move in y direction
            self.y += self.direction.y * self.speed
            
            self.rect.centery = int(self.y)
            for tile in obstacle_list:
                if self.rect.colliderect(tile):
                    if self.direction.y > 0:
                        self.rect.bottom = tile.top
                    elif self.direction.y < 0:
                        self.rect.top = tile.bottom
                    self.y = self.rect.centery

            if self.direction.length_squared() > 0:
                self.direction = self.direction.normalize()
    
        self.x += screen_scroll[0]
        self.y += screen_scroll[1]

    def update(self):
        pass

    def get_postion(self, position_list):
        i = random.randint(0, len(position_list) - 1)
        return position_list[i]
    
    def get_random_rect(self, position_list):
        index = random.randint(0, len(position_list) - 1)
        return position_list[index].copy()
    
    def get_virus(self):
        i = random.randint(0,1)
        if i == 0:
            return True
        else:
            return False
        
    def load_animation_list(self):
        infected = []
        faked = []
        for i in range(2):
            for j in range(2):
                faked.append(pygame.image.load(f'assets/character/faked/{j}/jaymeng{i}.png').convert_alpha())
                infected.append(pygame.image.load(f'assets/character/infected/{j}/jaymeng{i}.png').convert_alpha())
        animation_list = []
        animation_list.append(infected)
        animation_list.append(faked)

        return animation_list

        
    def get_animation(self):
        self.now = pygame.time.get_ticks()
        
        if self.now - self.last_animation > self.random_cooldown:
            self.last_animation = self.now
            self.last_frame = self.now
            self.animation_unfinished = True

            self.actual_list = self.animation_list[1]
            if self.infected and random.randint(0, 1) == 0:
                self.actual_list = self.animation_list[0]

            self.frame = 0

        if self.animation_unfinished:
            if self.now - self.last_frame > 200:
                self.last_frame = self.now

                self.img = self.actual_list[self.frame]
                self.frame += 1

                if self.frame >= len(self.actual_list):
                    self.animation_unfinished = False
                    self.img = pygame.image.load(f'assets/character/jaymeng.png').convert_alpha()
                    self.random_cooldown = random.randint(2000, 10000)

        