from utils import *
import random
import math
from timer import Timer

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, frames, collision_sprites, z):
        super().__init__(groups)

        # attributes
        self.start_pos = pos
        self.health = 5
        self.speed = 200
        self.jump = False
        self.jump_height = 500
        self.gravity = 1200
        self.attack = False
        self.idle_animation = False
        self.on_moving_platform = None
        self.direction = pygame.math.Vector2()
        self.z = z

        self.frames = frames
        self.sprite_frame = 0
        self.facing = 'right'
        self.animation_type = 'idle'
        self.image = frames[self.animation_type][self.sprite_frame]

        #rects
        self.rect = self.image.get_frect(center=pos)
        #self.hitbox_rect = self.rect.inflate(-120, -96)
        self.hitbox_rect = self.rect.inflate(-100, -80)
        #self.hitbox_rect = self.rect.copy()
        self.old_rect = self.hitbox_rect



        self.contact = {
            'ground': False,
            'leftwall': False,
            'rigtwall': False,
            'topwall': False
        }

        # collision
        self.collision_sprites = collision_sprites

        self.timers = {
            'damage': Timer(200)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        pos = Vector2()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pos.x -= 1
            self.facing = 'left'

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pos.x += 1
            self.facing = 'right'

        if pos.magnitude() > 0:
            self.direction.x = pos.normalize().x
        else:
            self.direction.x = pos.x

        if keys[pygame.K_SPACE]:
            self.jump = True

        if keys[pygame.K_x] and not self.attack:
            self.attack = True
            self.sprite_frame = 0

    def get_animation_type(self):
        if self.contact['ground']:
            if self.attack:
                self.animation_type = 'attack'
            else: self.animation_type = 'idle' if self.direction.x == 0 else 'walk'
        else:
            if self.direction.y < 0:
                self.animation_type = 'jump'
            else: self.animation_type = 'fall'
    def animate(self, dt):

        self.sprite_frame += ANIMATION_SPEED * dt

        if self.animation_type == 'idle':
            if random.randint(1, 2000) == 1 and not self.idle_animation and self.animation_type == 'idle':
                self.idle_animation = True
        elif self.animation_type != 'idle' and self.idle_animation:
            self.idle_animation = False
            self.sprite_frame = 0

        if self.idle_animation:
            if int(self.sprite_frame) >= len(self.frames[self.animation_type]):
                self.idle_animation = False
        elif self.animation_type == 'idle':
            self.sprite_frame = 0

        if self.animation_type == 'attack' and self.sprite_frame >= len(self.frames[self.animation_type]):
            self.animation_type = 'idle'
            self.attack = False

        if self.sprite_frame >= len(self.frames[self.animation_type]):
            self.sprite_frame = 0

        self.image = self.frames[self.animation_type][int(self.sprite_frame)]

        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, dt):
        #Move
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.rect.center = self.hitbox_rect.center
        self.collision(True)

        if self.jump and self.contact['ground']:
            self.direction.y -= self.jump_height
            #self.sprite_frame = 0
        self.jump = False


        #Gravity
        self.direction.y += self.gravity / 2 * dt
        self.hitbox_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt

        #Collision
        self.collision(False)

    def platfrom_move(self, dt):
        if self.on_moving_platform and self.on_moving_platform.direction[1] != -1:
            self.hitbox_rect.topleft += self.on_moving_platform.direction * self.on_moving_platform.speed * dt

    def check_contact(self):
        #top_rect = pygame.Rect(self.hitbox_rect.topleft, self.hitbox_rect.width, 2)
        #right_rect = pygame.Rect(self.hitbox_rect.topright, 2, self.hitbox_rect.height)
        bottom_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 1))
        #left_rect = pygame.Rect(self.hitbox_rect.topleft, 2, self.hitbox_rect.height)
        #pygame.draw.rect(self.surf, ('red'), bottom_rect)

        bottom_collide = [sprite.rect for sprite in self.collision_sprites if hasattr(sprite, 'visible') and sprite.visible or not hasattr(sprite, 'visible')]

        self.contact['ground'] = True if bottom_rect.collidelist(bottom_collide) >= 0 else False

        self.on_moving_platform = None

        moving_srites = [sprite for sprite in self.collision_sprites if hasattr(sprite, 'moving')]

        for moving_sprite in moving_srites:
            if moving_sprite.rect.colliderect(bottom_rect):
                self.on_moving_platform = moving_sprite

    def collision(self, horizontal):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox_rect):
                if not hasattr(sprite, 'visible') or hasattr(sprite, 'visible') and sprite.visible:
                    if horizontal:
                        # Left side collision
                        if self.hitbox_rect.left <= sprite.hitbox.right and self.old_rect.left >= sprite.old_rect.right:
                            self.hitbox_rect.left = sprite.hitbox.right
                        # Right side collision
                        if self.hitbox_rect.right >= sprite.hitbox.left and self.old_rect.right <= sprite.old_rect.left:
                            self.hitbox_rect.right = sprite.hitbox.left

                    else:
                        #vertical bottom collision
                        if self.hitbox_rect.bottom >= sprite.hitbox.top and self.old_rect.top <= sprite.old_rect.bottom:
                            self.hitbox_rect.bottom = sprite.hitbox.top
                            self.direction.y = 0

                        #top collision
                        if self.hitbox_rect.top <= sprite.hitbox.bottom and self.old_rect.top >= sprite.old_rect.top:
                            self.hitbox_rect.top = sprite.hitbox.bottom
                            if hasattr(sprite, 'moving'):
                                self.hitbox_rect.top += 2
                                self.direction.y = 0

            self.rect.center = self.hitbox_rect.center

    def get_damage(self):
        if not self.timers['damage'].active:
            self.timers['damage'].activate()
            self.health -= 1

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



