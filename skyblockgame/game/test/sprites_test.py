import sys


sys.path.append('../..')

import unittest
from unittest.mock import MagicMock
from utils import *
from game.code.sprites import Sprite, MovingSprite, AnimatedSprite, FloatingSprite, Heart


class TestSprite(unittest.TestCase):
    def setUp(self):
        self.groups = MagicMock()
        self.image = pygame.Surface((50,50))
        self.sprite = Sprite((0, 0), self.image, self.groups)

    def test_init(self):
        self.assertEqual(self.sprite.image, self.image)
        self.assertEqual(self.sprite.rect.topleft, (0, 0))

class TestAnimatedSprite(unittest.TestCase):
    def setUp(self):
        self.groups = MagicMock()
        self.frames = [MagicMock(), MagicMock()]
        self.sprite = AnimatedSprite((0, 0), self.groups, self.frames)

    def test_animate(self):
        self.sprite.animate(0.1)
        self.assertEqual(self.sprite.image, self.frames[1])

class TestFloatingSprite(unittest.TestCase):
    def setUp(self):
        self.groups = MagicMock()
        self.image = pygame.Surface((50,50))
        self.sprite = FloatingSprite((0, 0), [self.image], self.groups)

    def test_update(self):
        for i in range(2500):
            self.sprite.update(1)
            if self.sprite.timer.active:
                self.assertTrue(self.sprite.visible)
            else:
                self.assertFalse(self.sprite.visible)

class TestMovingSprite(unittest.TestCase):
    def setUp(self):
        self.groups = MagicMock()
        self.frames = [pygame.Surface((10, 10)), pygame.Surface((10,10))]
        self.sprite = MovingSprite(self.groups, (0, 0), (100, 0), 10, 'horizontal', self.frames)

    def test_move(self):
        self.sprite.move(1)
        self.assertEqual(self.sprite.rect.center, pygame.math.Vector2(self.sprite.speed, 0))

class TestHeart(unittest.TestCase):
    def setUp(self):
        self.groups = MagicMock()
        self.image = pygame.Surface((50,50))
        self.sprite = Heart((0, 0), self.image, self.groups)

    def test_init(self):
        self.assertEqual(self.sprite.image, self.image)
        self.assertEqual(self.sprite.rect.topleft, (0, 0))

if __name__ == '__main__':
    unittest.main()