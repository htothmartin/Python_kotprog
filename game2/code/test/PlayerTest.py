
import unittest
from unittest.mock import patch
from unittest.mock import Mock, MagicMock
from game2.code.src.player import Player
from utils import *



class TestPlayer(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.event.get()
        post_event = pygame.event.Event(pygame.K_SPACE)
        pygame.event.post(post_event)
        event = pygame.event.poll()

        self.groups = MagicMock()
        self.frames = {'idle': [Mock(), Mock(), Mock()],
                       'fall': [Mock(), Mock(), Mock()]}
        self.collision_sprites = []
        self.player = Player((100, 100), self.groups, self.frames, self.collision_sprites, 1)
        self.player.hitbox_rect = pygame.FRect(0,0,50,50)

    def test_initialization(self):
        self.assertEqual(self.player.health, 5)
        self.assertEqual(self.player.speed, 200)
        # Teszteld további inicializációs értékeket

    def test_collision(self):
        # Test collision with another sprite
        mock_sprite = MagicMock()
        mock_sprite.rect = pygame.Rect(110, 100, 20, 20)  # Assuming sprite is 20x20 and next to player
        self.player.collision_sprites.append(mock_sprite)
        self.assertTrue(self.player.collide())

    @patch('pygame.key.get_pressed')
    def test_input(self, mock_get_pressed):
        # Szimuláljuk a jobbra nyíl gomb lenyomását
        mock_get_pressed.return_value = {pygame.K_RIGHT: 1,
                                         pygame.K_LEFT: 0,
                                         pygame.K_SPACE: 1,
                                         pygame.K_x: 0, pygame.K_a: 0, pygame.K_d: 0}
        self.player.input()
        self.assertEqual(self.player.direction.x, 1)
        self.assertEqual(self.player.facing, 'right')
        self.assertTrue(self.player.jump)

        # Szimuláljuk a balra nyíl gomb lenyomását
        mock_get_pressed.return_value = {pygame.K_RIGHT: 0, pygame.K_LEFT: 1, pygame.K_SPACE: 0, pygame.K_x: 0, pygame.K_a: 0, pygame.K_d: 0}
        self.player.input()
        self.assertEqual(self.player.direction.x, -1)
        self.assertEqual(self.player.facing, 'left')

        # Szimuláljuk a space gomb lenyomását
        mock_get_pressed.return_value = {pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE: 1, pygame.K_x: 0, pygame.K_a: 0, pygame.K_d: 0}
        self.player.input()
        self.assertTrue(self.player.jump)

        # Szimuláljuk az x gomb lenyomását
        mock_get_pressed.return_value = {pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_SPACE: 0, pygame.K_x: 1, pygame.K_a: 0, pygame.K_d: 0}
        self.player.attack = False
        self.player.input()
        self.assertTrue(self.player.attack)


    def test_collision(self):
        pass
        # Teszteld a játékos ütközését más játékobjektumokkal
        # Például: hozz létre különböző mock objektumokat, amelyekkel ütközteted a játékost, és ellenőrizd az elvárt viselkedést

    def test_damage(self):
        prev_health = self.player.health
        self.player.get_damage()
        self.assertEqual(self.player.health, prev_health - 1)
        self.player.get_damage()
        self.assertEqual(self.player.health, prev_health - 1)

    def test_attack(self):
        self.player.attack = True
        self.player.attack_timer = 0
        self.player.attack_animation = MagicMock()
        self.player.update(0.1)

if __name__ == '__main__':
    unittest.main()
