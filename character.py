import pygame
from abc import ABC, abstractmethod
import constants

class Character(ABC):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
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
        Character.__init__(self, x, y, speed)
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f'assets/character/melon.png').convert_alpha()
        self.direction = pygame.Vector2(0, 0)
        self.flip = False
        self.rect = self.img.get_rect()
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
    
    def move(self, obstacle_list):
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
    
    def update(self, keys, obstacle_list, events):
        self.input_keys(keys)

        for event in events:
            self.input_event(event)

        new_scroll = None


        if new_scroll:
            return new_scroll
        return self.move(obstacle_list)



class Npc(Character, pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        Character.__init__(self, x, y, speed)
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f'assets/character/melon.png').convert_alpha()
        self.flip = False
        self.direction = pygame.Vector2(0, 0)
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def move(self):
        pass

    def update(self):
        pass