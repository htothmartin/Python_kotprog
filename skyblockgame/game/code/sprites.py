import random
import pygame
from timer import Timer
from utils import ANIMATION_SPEED, Z_LAYERS


# Alap sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.old_rect = self.hitbox.copy()
        self.z = z


# Animált sprite
class AnimatedSprite(Sprite):
    def __init__(self, pos, groups, frames, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):

        self.frames = frames
        self.sprite_frame = 0
        super().__init__(pos, self.frames[self.sprite_frame], groups, z)
        self.animation_speed = animation_speed
        self.rect.bottom = pos[1]
        self.hitbox.center = self.rect.center

    def animate(self, dt):
        self.sprite_frame += self.animation_speed * dt
        if self.sprite_frame >= len(self.frames):
            self.sprite_frame = 0
        self.image = self.frames[int(self.sprite_frame)]

    def update(self, dt):
        self.animate(dt)


# Lebegő sprite
class FloatingSprite(Sprite):
    def __init__(self, pos, surf, groups, z=Z_LAYERS['main']):
        super().__init__(pos, surf[0], groups, z)
        self.visible = True
        interval = random.randint(2000, 2500)
        self.timer = Timer(interval, repeat=True, autostart=True)

    def update(self, dt):
        self.timer.update()
        self.visible = self.timer.active


# Mozgó sprite
class MovingSprite(AnimatedSprite):
    def __init__(self, groups, start_pos, end_pos, speed, direction, frames, z=Z_LAYERS['main']):
        super().__init__(start_pos, groups, frames, z)
        self.hitbox.inflate_ip(-25, 0)
        self.frames = frames
        self.rect.center = start_pos
        self.hitbox.center = self.rect.center
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.speed = speed
        self.moving = True
        self.direction = pygame.math.Vector2(1, 0) if direction == 'horizontal' else pygame.math.Vector2(0, 1)

    def move(self, dt):
        if self.direction.x != 0:
            if self.hitbox.right >= self.end_pos[0]:
                self.direction = pygame.math.Vector2(-1, 0)
            if self.hitbox.left <= self.start_pos[0]:
                self.direction = pygame.math.Vector2(1, 0)
        else:
            if self.hitbox.bottom >= self.end_pos[1]:
                self.direction = pygame.math.Vector2(0, -1)
            if self.hitbox.top <= self.start_pos[1]:
                self.direction = pygame.math.Vector2(0, 1)

        self.hitbox.center += self.direction * dt * self.speed
        self.rect.center = self.hitbox.center

    def update(self, dt):

        self.old_rect = self.hitbox.copy()
        self.move(dt)
        self.animate(dt)

# Szivek
class Heart(Sprite):
    def __init__(self, pos, image, groups, z=Z_LAYERS['main']):
        super().__init__(pos, image, groups, z)
