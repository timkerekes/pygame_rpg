import pygame
import sys
from config import *
from sprites import *
from player import *
from enemy import *
from block import *
from ground import *
from button import *
from attack import *
from fireball import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Roboto-Bold.ttf', 32)
        self.running = True
        self.lvl_complete = False

        self.character_spritesheet = SpriteSheet('img/character.png')
        self.terrain_spritesheet = SpriteSheet('img/terrain.png')
        self.enemy_spritesheet = SpriteSheet('img/enemy.png')
        self.attack_spritesheet = SpriteSheet('img/attack.png')
        self.fireball_spritesheet = SpriteSheet('img/All_Fire_Bullet_Pixel.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    self.enemy = Enemy(self, j, i, 100)
                if column == 'P':
                    self.player = Player(self, j, i, 100)

    def new(self):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        # Attack(self, self.player.rect.x,
                        #        self.player.rect.y - TILESIZE)
                        Fireball(self, self.player.rect.x,
                               self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        # Attack(self, self.player.rect.x,
                        #        self.player.rect.y + TILESIZE)
                        Fireball(self, self.player.rect.x,
                               self.player.rect.y + TILESIZE * 2)
                    if self.player.facing == 'left':
                        # Attack(self, self.player.rect.x -
                        #        TILESIZE, self.player.rect.y)
                        Fireball(self, self.player.rect.x - TILESIZE,
                               self.player.rect.y)
                    if self.player.facing == 'right':
                        # Attack(self, self.player.rect.x +
                        #        TILESIZE, self.player.rect.y)
                        Fireball(self, self.player.rect.x + TILESIZE,
                               self.player.rect.y)

    def update(self):
        # game loop updates
        self.all_sprites.update()

        if len(self.enemies.sprites()) == 0:
                self.lvl_complete = True
                self.playing = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.player.draw_health_bar(self.screen)
        for enemy in self.enemies:
            if enemy.hp > 0:
                enemy.draw_health_bar(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        title = self.font.render('GAME OVER!', True, WHITE)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, (WIN_HEIGHT/2)-100))

        restart_button = Button((WIN_WIDTH/2)-225, (WIN_HEIGHT/2)+100,
                                150, 50, BLACK, WHITE, 'Restart', 32)

        quit_button = Button((WIN_WIDTH/2)+75, (WIN_HEIGHT/2)+100,
                             150, 50, BLACK, WHITE, 'Quit', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('PYGAME RPG', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2-100))

        play_button = Button((WIN_WIDTH/2)-50, (WIN_HEIGHT/2)+100,
                             100, 50, BLACK, WHITE, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        intro = False
                        self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def win_screen(self):
        title = self.font.render('LEVEL COMPLETE!', True, WHITE)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, (WIN_HEIGHT/2)-100))

        restart_button = Button((WIN_WIDTH/2)-225, (WIN_HEIGHT/2)+100,
                                150, 50, BLACK, WHITE, 'Restart', 32)
        
        next_button = Button((WIN_WIDTH/2)+50, (WIN_HEIGHT/2)+100,
                             200, 50, BLACK, WHITE, 'Next Level', 32)
        
        for sprite in self.all_sprites:
            sprite.kill()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(next_button.image, next_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    if g.lvl_complete == True:
        g.win_screen()
    else:
        g.game_over()

pygame.quit()
sys.exit()
