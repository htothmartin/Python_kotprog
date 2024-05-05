import unittest
from timer import Timer
from pygame import time

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer(1000)
        self.timer2 = Timer(1000, True, True)

    def test_init(self):
        self.assertFalse(self.timer.active)
        self.assertEqual(self.timer.interval, 1000)
        self.assertFalse(self.timer.repeat)

    def test_activate(self):
        self.timer.activate()
        self.assertTrue(self.timer.active)
        self.assertEqual(self.timer.start_time, time.get_ticks())

    def test_deactivate(self):
        self.timer.activate()
        self.timer.deactivate()
        self.assertFalse(self.timer.active)
        self.assertEqual(self.timer.start_time, time.get_ticks())

    def test_update(self):
        self.timer.activate()
        time.delay(1000)
        self.timer.update()
        self.timer2.update()
        self.assertFalse(self.timer.active)
        self.assertFalse(self.timer2.active)







if __name__ == '__main__':
    unittest.main()
