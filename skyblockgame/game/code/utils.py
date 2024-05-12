import os
from os.path import join
from os import walk
import pygame
from pytmx.util_pygame import load_pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ANIMATION_SPEED = 10
TILE_SIZE = 32
PIG_HEALTH = 3
PLAYER = {
    'health': 5,
    'speed': 200,
    'jump_height': 500,
    'gravity': 1200,
}

Z_LAYERS = {
    'bg': 0,
    'vegetation': 1,
    'main': 2,
    'castle': 3,
    'player': 4,
    'ui': 5
}


def load_image(*path, alpha=True, format='png', scale=1):
    full_path = join(*path) + f'.{format}'
    image = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    image = pygame.transform.scale_by(image, scale)
    return image


def load_folder(*path, scale=1):
    frames = []
    for path, _, files in walk(join(*path)):
        for file in files:
            full_path = join(path, file.split('.')[0])
            frames = load_spritesheet(full_path, scale=scale)

    return frames


def load_folder_dict(*path, scale=1):
    frames = {}
    for path, _, files in walk(join(*path)):
        for file in files:
            full_path = join(path, file)
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale_by(image, scale)
            frames[file.split('.')[0]] = image

    return frames


def load_subfolders(*path, scale=1):
    frames = {}
    for path, sub_folders, _ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frames[sub_folder] = load_folder(join(path, sub_folder), scale=scale)

    return frames


def load_spritesheet(path, scale=1):
    frames = []
    width = int(path.split(os.sep)[-1])
    sheet = load_image(path)
    height = sheet.get_height()
    cols = sheet.get_width() / width

    for col in range(int(cols)):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), ((col * width), 0, width, height))
        image = pygame.transform.scale_by(image, scale)

        frames.append(image)

    return frames


def load_levels():
    levels = {
        1: load_pygame(join('..', 'assets', 'levels', '01.tmx')),
        2: load_pygame(join('..', 'assets', 'levels', '02.tmx')),
        3: load_pygame(join('..', 'assets', 'levels', '03.tmx')),
    }

    return levels


def load_assets():
    level_images = {
        'player': load_subfolders('..', 'assets', 'images', 'player2', scale=2.5),
        'platforms': load_subfolders('..', 'assets', 'images', 'platforms', scale=2.5),
        'enemies': load_subfolders('..', 'assets', 'images', 'enemies', scale=2.5),
        'flags': load_subfolders('..', 'assets', 'images', 'flags', scale=1.5),
        'clouds': load_folder_dict('..', 'assets', 'images', 'backgrounds', scale=2.5),
        'hearts': load_image('..', 'assets', 'images', 'hearts', 'heart', 'heart', scale=2),
        'vegetation': load_folder_dict('..', 'assets', 'images', 'vegetation', scale=1),
        'castle': load_image('..', 'assets', 'images', 'castle', 'castle', 'castle')
        }
    return level_images


def load_audio():
    audio = {
        'player': {
            'jump': pygame.mixer.Sound(join('..', 'assets', 'audio', 'player', 'jump_sound.mp3')),
            'attack': pygame.mixer.Sound(join('..', 'assets', 'audio', 'player', 'attack.mp3'))
        },
        'background_music': pygame.mixer.Sound(join('..', 'assets', 'audio', 'background', 'background.mp3'))
    }
    return audio
