from utils import load_assets, load_levels


class Data:

    def __init__(self):
        self.level_images = load_assets()
        self.levels = load_levels()
        self.current_level = 1
        self.map = self.levels[self.current_level]
