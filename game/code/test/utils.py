import pygame
from pygame.math import Vector2
from os.path import join
from os import walk
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ANIMATION_SPEED = 10
TILE_SIZE = 32

Z_LAYERS = {
    'bg': 0,
    'vegetation': 1,
    'main': 2,
    'player': 3,
    'ui': 4
}

def get_images(path, width, height, frames, flip):
        sheet = pygame.image.load(path).convert_alpha()
        images = []
        for frame in range(frames):
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(sheet, (0,0), ((frame * width), 0, width, height))
            if flip:
                image = pygame.transform.flip(image, True, False)
            images.append(image)
            
        return images


def load_image(*path, alpha = True, format = 'png', scale=1):
    full_path = join(*path) + f'.{format}'
    image = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    image = pygame.transform.scale_by(image, scale)
    return image

def load_folder(*path, scale=1):
    frames = []
    for path, sub_folders, files in walk(join(*path)):
        for file in files:
            full_path = join(path, file.split('.')[0])
            frames = load_spritesheet(full_path, scale=scale)

    return frames

def load_folder_dict(*path, scale=1):
    frames = {}
    for path, sub_folders, files in walk(join(*path)):
        for file in files:
            full_path = join(path, file)
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale_by(image, scale)
            frames[file.split('.')[0]] = image

    return frames

def load_subfolders(*path, scale=1):
    frames = {}
    for path, sub_folders, files in walk(join(*path)):
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
#
# def load_spritesheet(width, *path):
#     frames = []
#
#     sheet = load_image(*path)
#     height = sheet.get_height()
#     cols = sheet.get_width() / width
#
#     for col in range(int(cols)):
#         image = pygame.Surface((width, height), pygame.SRCALPHA)
#
#         image.blit(sheet, (0, 0), ((col * width), 0, width, height))
#         image = pygame.transform.scale(image, (width * 3, height * 3))
#         mask = pygame.mask.from_surface(image)
#         rects = mask.get_bounding_rects()
#
#         if rects:
#             rect = rects[0]
#             cropped_image = pygame.Surface(rect.size, pygame.SRCALPHA)
#             cropped_image.blit(image, (0, 0), rect)
#             image = cropped_image
#
#         frames.append(image)
#
#     return frames


