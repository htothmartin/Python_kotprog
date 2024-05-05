import random
import math
import pygame
from utils import Z_LAYERS, ANIMATION_SPEED, PIG_HEALTH
from timer import Timer


class Pig(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames, collision_sprites, z=Z_LAYERS['main']):
        super().__init__(groups)
        self.frames = frames
        self.sprite_frame = 0
        self.image = self.frames[self.sprite_frame]
        self.direction = random.choice((-1, 1))
        self.speed = random.randint(50, 60)
        self.health = PIG_HEALTH
        self.facing = 'right' if self.direction == 1 else 'left'
        self.z = z

        # rects
        self.rect = self.image.get_frect(center=(pos[0], pos[1] - 30))
        self.hitbox = pygame.FRect(self.rect.topleft[0] + 30, self.rect.topleft[1] + 40, 35, 30)
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.timers = {
            'damage': Timer(200)
        }

    def check_direction(self):
        left = pygame.FRect(self.hitbox.topleft - pygame.math.Vector2(-2, 0), (2, self.hitbox.height))
        right = pygame.FRect(self.hitbox.topright, (2, self.hitbox.height))

        bottom_left = pygame.FRect(self.hitbox.bottomleft - pygame.math.Vector2(-2, 0), (2, 2))
        bottom_right = pygame.FRect(self.hitbox.bottomright, (2, 2))

        # pygame.draw.rect(self.surf, ('yellow'), bottom_left)
        # pygame.draw.rect(self.surf, ('yellow'), bottom_right)
        # pygame.draw.rect(self.surf, ('yellow'), left)
        # pygame.draw.rect(self.surf, ('yellow'), right)

        bottom_left_collision = bottom_left.collidelist(self.collision_rects) == -1 and self.direction < 0
        bottom_right_collision = bottom_right.collidelist(self.collision_rects) == -1 and self.direction > 0
        left_collision = left.collidelist(self.collision_rects) != -1 and self.direction < 0
        right_collision = right.collidelist(self.collision_rects) != -1 and self.direction > 0

        if bottom_left_collision or bottom_right_collision or left_collision or right_collision:
            self.direction *= -1
            self.facing = 'right' if self.direction == 1 else "left"

    def animate(self, dt):
        self.sprite_frame += ANIMATION_SPEED * dt

        if self.sprite_frame >= len(self.frames):
            self.sprite_frame = 0

        self.image = self.frames[int(self.sprite_frame)] if self.direction < 0 else pygame.transform.flip(
            self.frames[int(self.sprite_frame)], True, False)

    def get_damage(self):
        if self.health == 0:
            self.kill()

        if not self.timers['damage'].active:
            self.timers['damage'].activate()
            self.health -= 1

    def flick(self):
        if self.timers['damage'].active and math.sin(pygame.time.get_ticks() * 200) > 0:
            mask = pygame.mask.from_surface(self.image)
            mask = mask.to_surface()
            mask.set_colorkey((0, 0, 0))
            self.image = mask

    def move(self, dt):
        self.hitbox.x += self.direction * self.speed * dt
        self.rect.center = self.hitbox.center
        self.rect.bottom -= 15

    def update(self, dt):
        self.check_direction()
        self.move(dt)
        self.animate(dt)
        self.flick()
        for timer in self.timers.values():
            timer.update()
