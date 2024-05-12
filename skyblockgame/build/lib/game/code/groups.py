import math
import pygame
from .utils import SCREEN_WIDTH, SCREEN_HEIGHT
from .sprites import Heart

# A sprite osztály, ami tartamaz minden spriteot és kezeli a kamerát és a hátteret
class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)

        self.clouds = clouds

        self.width = width
        self.height = height

        self.camera_x_offset = 400
        self.camera_y_offset = 300

        w = self.display_surf.get_width() - 2 * self.camera_x_offset
        h = self.display_surf.get_height() - 2 * self.camera_y_offset
        self.camera_rect = pygame.Rect(self.camera_x_offset, self.camera_y_offset, w, h)

    # Kamera
    def box_camera(self, target):
        # Kamera mozgsatása
        self.camera_rect.left = min(self.camera_rect.left, target.left)
        self.camera_rect.right = max(self.camera_rect.right, target.right)

        self.camera_rect.bottom = target.bottom

        self.offset.x = self.camera_rect.left - self.camera_x_offset
        self.offset.y = self.camera_rect.top - self.camera_y_offset

    # A pélya határai vizsgálata
    def camera_borders(self):
        self.offset.x = 0 if self.offset.x < 0 else self.offset.x
        self.offset.x = self.width-SCREEN_WIDTH if self.offset.x > self.width-SCREEN_WIDTH else self.offset.x
        self.offset.y = self.height-SCREEN_HEIGHT if self.offset.y > self.height-SCREEN_HEIGHT else self.offset.y

    # Felhők rajzolása
    def draw_clouds(self):
        image_height = self.clouds['front'].get_height()
        multiplier = SCREEN_HEIGHT/image_height
        new_width = pygame.transform.scale_by(self.clouds['front'], multiplier).get_width()

        cloud_number = math.ceil(self.width/new_width)

        for i in range(cloud_number):
            self.display_surf.blit(pygame.transform.scale_by(self.clouds['back'], multiplier), (i * new_width - self.offset.x, 0))
            self.display_surf.blit(pygame.transform.scale_by(self.clouds['front'], multiplier), (i * new_width - self.offset.x, 0))

    def draw(self, target):
        self.draw_clouds()
        self.box_camera(target)
        self.camera_borders()

        for sprite in sorted(self.sprites(), key=lambda spr: spr.z):
            if hasattr(sprite, 'visible'):
                if sprite.visible:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surf.blit(sprite.image, offset_pos)
            elif isinstance(sprite, Heart):
                self.display_surf.blit(sprite.image, sprite.rect.topleft)
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surf.blit(sprite.image, offset_pos)
