import time

import pygame, sys, player
from level import Level
from os.path import join
from pytmx.util_pygame import load_pygame
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Advetures In The Forest')
        self.load_assets()

        self.load_levels()
        self.current_level = 1
        self.map = self.levels[self.current_level]
        self.level = Level(self.map, self.level_images, self.change_level)


        self.font = pygame.font.Font(join('../..', 'assets', 'fonts', 'Minecraft.ttf'), 20)
        self.message = self.font.render('Press space to start the game', False, (255, 255, 255))
        self.message_rect = self.message.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        self.running = False



        self.clock = pygame.time.Clock()

    def load_assets(self):
        self.level_images = {
            'player': load_subfolders('../..', 'assets', 'images', 'player2', scale=2.5),
            'platforms': load_subfolders('../..', 'assets', 'images', 'platforms', scale=2.5),
            'enemies': load_subfolders('../..', 'assets', 'images', 'enemies', scale=2.5),
            'flags': load_subfolders('../..', 'assets', 'images', 'flags', scale=1.5),
            'clouds': load_folder_dict('../..', 'assets', 'images', 'backgrounds', scale=2.5),
            'hearts': load_image('../..', 'assets', 'images', 'hearts', 'heart', scale=2),
            'vegetation': load_folder_dict('../..', 'assets', 'images', 'vegetation', scale=1)
        }

    def load_levels(self):
        self.levels = {
            1: load_pygame(join('../..', 'assets', 'levels', '01.tmx')),
            2: load_pygame(join('../..', 'assets', 'levels', '02.tmx'))
        }

    def change_level(self):
        time.sleep(3)
        self.current_level += 1
        self.level = Level(self.levels[self.current_level], self.level_images, self.change_level)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.running:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.running = True

            if self.running:
                self.level.run(dt)
            else:
                self.screen.fill('#42f5e9')
                self.screen.blit(self.message, self.message_rect)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
