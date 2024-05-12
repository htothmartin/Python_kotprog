import sys
sys.path.append('../..')


import unittest
from pygame import sprite, Surface
from utils import Z_LAYERS
from timer import Timer
from game.code.enemies import Pig

class TestPig(unittest.TestCase):
    def setUp(self):
        self.groups = sprite.LayeredUpdates()
        self.frames = [Surface((50, 50))]
        self.collision_sprites = []
        self.pig = Pig((100, 100), self.groups, self.frames, self.collision_sprites)

    def test_init(self):
        self.assertTrue(50 <= self.pig.speed <= 60)
        self.assertEqual(self.pig.health, 3)
        if self.pig.direction == 1:
            self.assertEqual(self.pig.facing, 'right')
        else:
            self.assertEqual(self.pig.facing, 'left')
        self.assertEqual(self.pig.z, Z_LAYERS['main'])
        self.assertIsInstance(self.pig.timers['damage'], Timer)

    def test_get_damage(self):
        self.pig.get_damage()
        self.assertEqual(self.pig.health, 2)
        self.pig.get_damage()
        self.assertEqual(self.pig.health, 2)

    def test_move(self):
        old_pos = self.pig.hitbox.x
        self.pig.move(1)
        self.assertEqual(self.pig.hitbox.x, old_pos + self.pig.direction * self.pig.speed)

if __name__ == '__main__':
    unittest.main()
