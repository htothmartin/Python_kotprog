import time
import sys
from os.path import join
import os
import pygame
from .level import Level
from .utils import SCREEN_WIDTH, SCREEN_HEIGHT
from .data import Data

base_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(base_dir)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Sky block parkour adventure game')
        self.font = pygame.font.Font(join('..', 'assets', 'fonts', 'Minecraft.ttf'), 20)
        self.data = Data()
        self.level = Level(self.data.map, self.data.level_images, self.change_level)
        self.running = False
        self.clock = pygame.time.Clock()

    # Pálya váltás
    def change_level(self):
        self.screen.fill('#42f5e9')
        if self.data.current_level == 3:
            self.end_game()
        self.data.current_level += 1
        next_level_msg = self.font.render('Level ' + str(self.data.current_level), False, (255, 255, 255))
        next_level_rect = next_level_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(next_level_msg, next_level_rect)
        pygame.display.update()
        time.sleep(2)

        self.level = Level(self.data.levels[self.data.current_level], self.data.level_images, self.change_level)

    # Játék vége
    def end_game(self):
        end_msg = self.font.render('End', False, (255, 255, 255))
        end_rect = end_msg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(end_msg, end_rect)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Játék futása
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
                message = self.font.render('Press space to start the game', False, (255, 255, 255))
                message_rect = message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                self.screen.blit(message, message_rect)

            pygame.display.update()

def start():
    game = Game()
    game.run()


if __name__ == '__main__':
    start()

