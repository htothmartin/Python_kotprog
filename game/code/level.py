import pygame
from player import Player
from sprites import Sprite, FloatingSprite, MovingSprite, AnimatedSprite, Heart
from groups import AllSprites
from enemies import Pig
from timer import Timer
from utils import *


class Level:
    def __init__(self, tmx_map, level_images):
        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.level_images = level_images

        self.width = tmx_map.width * TILE_SIZE
        self.height = tmx_map.height * TILE_SIZE

        #Sprite groups
        self.all_sprites = AllSprites(self.width, self.height, level_images['clouds'])
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()

        #Setup
        self.setup(tmx_map)



        self.timers = {
            'damage': Timer(500),
            'attack': Timer(600)
        }
        
    def setup(self, tmx_map):

        for x, y, surf in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x * 32, y * 32), surf, (self.all_sprites, self.collision_sprites))

        for x, y, surf in tmx_map.get_layer_by_name('Floating').tiles():
            Sprite((x * 32, y * 32), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'fan_platform':
                if obj.width > obj.height:
                    start_pos = (obj.x , obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                    direction = 'horizontal'
                else:
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                    direction = 'vertical'
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites, self.collision_sprites), start_pos, end_pos, speed, direction, self.level_images['platforms'][obj.name])
                #Sprite(start_pos, self.level_images['platforms'][obj.name][0], (self.all_sprites, self.collision_sprites))
            elif obj.name == 'platform':
                FloatingSprite((obj.x, obj.y), self.level_images['platforms'][obj.name], (self.all_sprites, self.collision_sprites))
            elif obj.name == 'pig':
                Pig((obj.x, obj.y), (self.all_sprites, self.damage_sprites), self.level_images['enemies'][obj.name], self.collision_sprites)
            elif obj.name == 'finish_flag':
                AnimatedSprite((obj.x, obj.y), (self.all_sprites), self.level_images['flags'][obj.name])
            elif obj.name == 'grass' or obj.name == 'bush' or obj.name == 'big_tree' or obj.name == 'small_tree':
                Sprite((obj.x, obj.y), self.level_images['vegetation'][obj.name], (self.all_sprites), Z_LAYERS['vegetation'])
            elif obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.level_images['player'], self.collision_sprites, Z_LAYERS['player'])
                self.create_hearts()



    def enemy_collison(self):
        collision_list = [sprite.hitbox for sprite in self.damage_sprites]
        if self.player.hitbox_rect.collidelist(collision_list) != -1 and not self.timers['damage'].active:
            self.player.get_damage()
            if self.player.health <= 0:
                self.player.hitbox_rect.topleft = self.player.start_pos
                self.player.health = 5
            self.create_hearts()
            self.timers['damage'].activate()

    def check_borders(self):
        if self.player.hitbox_rect.left < 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right > self.width:
            self.player.hitbox_rect.right = self.width
        if self.player.hitbox_rect.top > self.height:
            self.player.hitbox_rect.topleft = self.player.start_pos
            self.player.direction.y = 0

    def attack(self):
        for sprite in self.damage_sprites:
            if sprite.hitbox.colliderect(self.player.rect) and self.player.attack and not self.timers['attack'].active and sprite.hitbox.centery + 38 > self.player.hitbox_rect.centery and\
                    sprite.hitbox.centery - 38 < self.player.hitbox_rect.centery:
                if(self.player.facing == 'left' and sprite.hitbox.centerx <= self.player.hitbox_rect.centerx) or (self.player.facing == 'right' and sprite.hitbox.centerx >= self.player.hitbox_rect.centerx):
                    self.timers['attack'].activate()
                    sprite.get_damage()
                    print("attck")


    def create_hearts(self):
        for sprite in self.hearts:
            sprite.kill()
        width = self.level_images['hearts'].get_width()
        for heart in range(self.player.health):
            x = 30 + heart * width
            y = 30
            Heart((x, y), self.level_images['hearts'], (self.all_sprites, self.hearts), Z_LAYERS['ui'])


    def run(self, dt):
        self.display_surface.fill('#03cafc')
        self.all_sprites.update(dt)
        self.enemy_collison()
        self.all_sprites.draw(self.player.hitbox_rect)
        self.check_borders()
        self.attack()
        for timer in self.timers.values():
            timer.update()
