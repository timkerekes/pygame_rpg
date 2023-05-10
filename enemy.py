import pygame
import math
import random

from config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, hp):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.hp = hp
        self.hp_rect = pygame.Rect(self.x, self.y - 10, self.width, 5)
        self.hp_bar_rect = pygame.Rect(self.x, self.y - 10, self.width, 5)

        self.last_hit_time = 0

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(
            3, 2, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(
            35, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(
            35, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_attack()

        self.hp_rect.width = self.rect.width * self.hp / 100
        self.hp_bar_rect.left = self.rect.left
        self.hp_bar_rect.top = self.rect.top - 10
        self.hp_rect.left = self.rect.left
        self.hp_rect.top = self.rect.top - 10

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

        if self.hp <=0:
            self.kill()

    def collide_attack(self):
        hits = pygame.sprite.spritecollide(self, self.game.attacks, False)
        if hits:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= 250:
                if self.hp > 0:
                    self.hp = self.hp - 50
                    self.last_hit_time = current_time
                else:
                    self.kill()

    def draw_health_bar(self, surface):
        pygame.draw.rect(surface, RED, self.hp_bar_rect)
        pygame.draw.rect(surface, GREEN, self.hp_rect)

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1