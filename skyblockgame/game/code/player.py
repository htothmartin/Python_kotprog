import random
import math
import pygame
from pygame.math import Vector2
from timer import Timer
from utils import ANIMATION_SPEED, PLAYER


# Játékos karakter
class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, frames, collision_sprites, z, audio):
        super().__init__(groups)

        # Adattagos
        self.start_pos = pos
        self.health = PLAYER['health']
        self.speed = PLAYER['speed']
        self.jump = False
        self.jump_height = PLAYER['jump_height']
        self.gravity = PLAYER['gravity']
        self.attack = False
        self.idle_animation = False
        self.on_moving_platform = None
        self.direction = pygame.math.Vector2()
        self.z = z
        self.audio = audio

        self.frames = frames
        self.sprite_frame = 0
        self.facing = 'right'
        self.animation_type = 'idle'
        self.image = frames[self.animation_type][self.sprite_frame]

        # Téglalapok
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-100, -80)
        self.old_rect = self.hitbox_rect

        self.contact = {
            'ground': False,
            'left': False,
            'rigt': False,
            'top': False
        }

        # collision
        self.collision_sprites = collision_sprites

        self.timers = {
            'damage': Timer(200)
        }

    # Beolvassa az inputot a billenytűzetről és a vegrehajtja a megfelelő lépést
    def input(self):
        keys = pygame.key.get_pressed()
        pos = Vector2()

        # Balra mozgás
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pos.x -= 1
            self.facing = 'left'

        # Jobbra mozgás
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pos.x += 1
            self.facing = 'right'

        # Normalizáljuk az irányt, hogy mindig azonos távolságot tegyen meg a karakter
        if pos.magnitude() > 0:
            self.direction.x = pos.normalize().x
        else:
            self.direction.x = pos.x

        # Ugrás
        if keys[pygame.K_SPACE]:
            self.jump = True


        # Támadás
        if keys[pygame.K_x] and not self.attack and self.contact['ground']:
            self.audio['attack'].set_volume(0.4)
            self.audio['attack'].play()
            self.attack = True
            self.sprite_frame = 0

    # Kiválasztjuk a megfelelő aniámáció típusát, a mozágashoz megfelelően
    def get_animation_type(self):
        if self.contact['ground']:
            if self.attack:
                self.animation_type = 'attack'
            else:
                self.animation_type = 'idle' if self.direction.x == 0 else 'walk'
        else:
            if self.direction.y < 0:
                self.animation_type = 'jump'
            else:
                self.animation_type = 'fall'

    # Animáció
    def animate(self, dt):
        self.sprite_frame += ANIMATION_SPEED * dt

        # Alap animáció random lejátszása
        if self.animation_type == 'idle':
            if (random.randint(1, 2000) == 1
                    and not self.idle_animation and self.animation_type == 'idle'):
                self.idle_animation = True
        elif self.animation_type != 'idle' and self.idle_animation:
            self.idle_animation = False
            self.sprite_frame = 0

        if self.idle_animation:
            if int(self.sprite_frame) >= len(self.frames[self.animation_type]):
                self.idle_animation = False
        elif self.animation_type == 'idle':
            self.sprite_frame = 0

        if (self.animation_type == 'attack' and self.sprite_frame >= len(self.frames[self.animation_type])):
            self.animation_type = 'idle'
            self.attack = False

        if self.sprite_frame >= len(self.frames[self.animation_type]):
            self.sprite_frame = 0

        self.image = self.frames[self.animation_type][int(self.sprite_frame)]

        # A balra mozgáshoz a frame tükrözése
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    # Mozgás
    def move(self, dt):
        # Irány alapján sebesség kiszámolása
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        # Frissítjük képet tartalmazó tégalapot
        self.rect.center = self.hitbox_rect.center
        self.collision(True)
        if self.jump and self.contact['ground']:
            self.attack = False
            self.audio['jump'].set_volume(0.4)
            self.audio['jump'].play()
            self.direction.y = 0
            self.direction.y -= self.jump_height
            # self.sprite_frame = 0
        self.jump = False

        # Gravitáció
        self.direction.y += self.gravity / 2 * dt
        self.hitbox_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt

        # Ütközés
        self.collision(False)

    # Platformon mozgás
    def platfrom_move(self, dt):
        if self.on_moving_platform and self.on_moving_platform.direction[1] != -1:
            self.hitbox_rect.topleft += self.on_moving_platform.direction * self.on_moving_platform.speed * dt

    # Kontakt kizsámolása
    def check_contact(self):
        # top_rect = pygame.Rect(self.hitbox_rect.topleft, self.hitbox_rect.width, 2)
        # right_rect = pygame.Rect(self.hitbox_rect.topright, (1, self.hitbox_rect.height))
        bottom_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 1))
        # left_rect = pygame.Rect(self.hitbox_rect.topleft, (1, self.hitbox_rect.height))
        # pygame.draw.rect(self.surf, ('red'), bottom_rect)

        collide_rects = [sprite.rect for sprite in self.collision_sprites if
                         hasattr(sprite, 'visible') and sprite.visible or not hasattr(sprite, 'visible')]

        self.contact['ground'] = bottom_rect.collidelist(collide_rects) >= 0
        # self.contact['left'] = True if left_rect.collidelist(collide_rects) > 0 else False
        # self.contact['right'] = True if right_rect.collidelist(collide_rects) > 0 else False

        self.on_moving_platform = None

        moving_srites = [sprite for sprite in self.collision_sprites if hasattr(sprite, 'moving')]

        for moving_sprite in moving_srites:
            if moving_sprite.rect.colliderect(bottom_rect):
                self.on_moving_platform = moving_sprite

# Ütközés
    def collision(self, horizontal):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox_rect):
                if not hasattr(sprite, 'visible') or hasattr(sprite, 'visible') and sprite.visible:
                    if horizontal:
                        # Bal oldali ütközés
                        if self.hitbox_rect.left <= sprite.hitbox.right and self.old_rect.left >= sprite.old_rect.right:
                            self.hitbox_rect.left = sprite.hitbox.right
                        # Jobb oladli ütközés
                        if self.hitbox_rect.right >= sprite.hitbox.left and self.old_rect.right <= sprite.old_rect.left:
                            self.hitbox_rect.right = sprite.hitbox.left

                    else:
                        # Alsó ütközés
                        if self.hitbox_rect.bottom >= sprite.hitbox.top and self.old_rect.top <= sprite.old_rect.bottom:
                            self.hitbox_rect.bottom = sprite.hitbox.top
                            self.direction.y = 0

                        # Felső ütközés
                        if self.hitbox_rect.top <= sprite.hitbox.bottom and self.old_rect.top >= sprite.old_rect.top:
                            self.hitbox_rect.top = sprite.hitbox.bottom
                            if hasattr(sprite, 'moving'):
                                self.hitbox_rect.top += 2
                                self.direction.y = 0

            self.rect.center = self.hitbox_rect.center

    # Sérülés
    def get_damage(self):
        if not self.timers['damage'].active:
            self.timers['damage'].activate()
            self.health -= 1

    # Sérülés animáció
    def flick(self):
        if self.timers['damage'].active and math.sin(pygame.time.get_ticks() * 200) > 0:
            mask = pygame.mask.from_surface(self.image)
            mask = mask.to_surface()
            mask.set_colorkey((0, 0, 0))
            self.image = mask

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.input()
        self.move(dt)
        self.platfrom_move(dt)
        self.check_contact()
        self.get_animation_type()
        self.animate(dt)
        self.flick()
        for timer in self.timers.values():
            timer.update()
