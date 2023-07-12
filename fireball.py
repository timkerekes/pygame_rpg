import pygame
import math

from config import *


class Fireball(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.fireball_distance = 0

        self.image = self.game.fireball_spritesheet.get_sprite(
            0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.fireball_spritesheet.get_sprite(448, 208, self.width, self.height),
                                 self.game.fireball_spritesheet.get_sprite(
            448, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            448, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            448, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(448, 100, self.width, self.height)]

        self.down_animations = [self.game.fireball_spritesheet.get_sprite(448, 192, self.width, self.height),
                                self.game.fireball_spritesheet.get_sprite(
            456, 192, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            464, 192, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            472, 192, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(480, 192, self.width, self.height)]

        self.left_animations = [self.game.fireball_spritesheet.get_sprite(26, 616, self.width, self.height),
                                self.game.fireball_spritesheet.get_sprite(
            620, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            624, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            628, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(632, 100, self.width, self.height)]

        self.up_animations = [self.game.fireball_spritesheet.get_sprite(26, 616, self.width, self.height),
                              self.game.fireball_spritesheet.get_sprite(
            620, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            624, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(
            628, 100, self.width, self.height),
            self.game.fireball_spritesheet.get_sprite(632, 100, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.animation_loop = 0
                self.fireball_distance += 1
                if self.fireball_distance >= 8:
                    self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()