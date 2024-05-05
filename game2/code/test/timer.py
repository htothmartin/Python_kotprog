from pygame import time

class Timer():
    def __init__(self, interval, repeat=False, autostart=False):
        self.active = False
        self.interval = interval
        self.start_time = time.get_ticks()
        self.repeat = repeat
        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = time.get_ticks()

    def update(self):
        if self.active and time.get_ticks() - self.start_time >= self.interval:
            self.deactivate()
        if not self.active and time.get_ticks() - self.start_time >= self.interval and self.repeat:
            self.activate()